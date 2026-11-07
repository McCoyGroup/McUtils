"""Unit algebra, core-first resolution, and policy-specific energy equivalences."""
from dataclasses import FrozenInstanceError
from fractions import Fraction
import math
import unittest
from unittest.mock import patch

from McUtils.Data import ConversionError, UnitExpression, UnitsDataHandler


class UnitExpressionTests(unittest.TestCase):
    def setUp(self):
        self.registry = UnitsDataHandler()
        self.u = self.registry.units
        self.h = self.registry.constant('PlanckConstant')
        self.c = self.registry.constant('SpeedOfLightInVacuum')
        self.kb = self.registry.constant('BoltzmannConstant')
        self.hartree = self.registry.convert('Hartrees', 'Joules', equivalences=())
        self.bohr = self.registry.convert('BohrRadius', 'Meters', equivalences=())

    def assertFactor(self, actual, expected):
        self.assertTrue(math.isclose(actual, expected, rel_tol=2e-12), (actual, expected))

    def test_namespace_discovery_aliases_and_case_sensitive_symbols(self):
        self.assertIsInstance(self.u.bohr, UnitExpression)
        self.assertIn('bohr', dir(self.u))
        self.assertIn('Hartrees', dir(self.u))
        self.assertEqual(self.u.wavenumber, self.u.cm**-1)
        self.assertEqual(self.registry.unit('Eₕ'), self.u.hartree)
        self.assertFactor(self.registry.unit('meV').to(self.u.eV), 1e-3)
        self.assertFactor(self.registry.unit('MeV').to(self.u.eV), 1e6)
        self.assertFactor(self.registry.unit('mK').to(self.u.kelvin, equivalences=()), 1e-3)
        self.assertFactor(self.u.nm.to(self.u.angstrom), 10)
        with self.assertRaises(AttributeError):
            self.u.DoesNotExist

    def test_core_unit_identity_never_uses_energy_equivalences(self):
        self.assertEqual(self.u.N, self.u.J / self.u.m)
        self.assertNotEqual(self.u.kelvin, self.u.hartree)
        self.assertNotEqual(self.u.wavenumber, self.u.hartree)
        self.assertEqual(self.u.kelvin.dimensions, {'K': 1})
        self.assertEqual(self.u.wavenumber.dimensions, {'L': -1})
        with self.assertRaises(FrozenInstanceError):
            self.u.hartree.scale = 2
        with self.assertRaises(TypeError):
            hash(self.u.hartree)
        factors = [('cm', 1)]
        expression = UnitExpression(self.registry, factors)
        factors.append(('Seconds', 1))
        self.assertEqual(expression, self.u.cm)
        with self.assertRaises(ConversionError):
            UnitExpression(self.registry, [('not_a_unit', 1)])

    def test_safe_parser_and_legacy_forms_share_the_algebra(self):
        target = self.u.hartree / self.u.bohr**2
        for specification in ('Hartrees/BohrRadiusSquared', 'hartree / bohr^2',
                              'HartreesPerBohrRadiusSquared', 'Eh a0⁻²',
                              (('Hartrees', 1), ('BohrRadius', -2))):
            with self.subTest(specification=specification):
                self.assertEqual(self.registry.unit(specification), target)
        self.assertEqual(self.registry.unit('(hartree / bohr)**2'), (self.u.hartree / self.u.bohr)**2)
        self.assertEqual(self.registry.unit('m/s/s'), self.u.m / self.u.s**2)
        self.assertEqual(self.registry.unit('m/(s*s)'), self.u.m / self.u.s**2)
        self.assertEqual(self.registry.unit('m**(1/2)'), self.u.m**Fraction(1, 2))
        self.assertFactor((100 * self.u.cm).to(self.u.m), 1)
        self.assertEqual(self.registry.unit('1/cm'), 1 / self.u.cm)
        for specification in ('__import__("os")', 'm.real', '[m]', 'm + s', 'm**s', 'm//s', 'm/', 'm**(1/0)', 'm/0'):
            with self.subTest(specification=specification), self.assertRaises((ValueError, ConversionError)):
                self.registry.unit(specification)

    def test_unknown_units_are_not_energy_equivalence_failures(self):
        with self.assertRaisesRegex(ConversionError, 'Unknown unit') as caught:
            self.registry.convert('not_a_unit', 'Hartrees')
        self.assertNotIn('implicit energy', str(caught.exception))
        with self.assertRaises(ValueError):
            self.u.m**math.inf
        with self.assertRaises(ValueError):
            self.registry.unit('0*m')

    def test_default_is_exactly_wavenumber_and_core_search_wins(self):
        self.assertEqual(self.registry.default_equivalences, ('wavenumber',))
        with patch.object(self.registry, '_bridge_solutions', side_effect=AssertionError('core must win')):
            info = self.registry.explain_conversion(self.u.cm**-1 / self.u.angstrom,
                                                    self.u.angstrom**-2,
                                                    equivalences=tuple(self.registry.equivalences))
        self.assertEqual(info['stage'], 'core')
        self.assertFalse(info['bridges'])
        self.assertFactor(info['factor'], 1e-8)
        with self.assertRaises(ConversionError):
            self.u.kelvin.to(self.u.hartree)
        with self.assertRaises(ConversionError):
            self.u.hartree.to(self.u.Hz)
        self.assertFactor(self.u.wavenumber.to(self.u.hartree), 100 * self.h * self.c / self.hartree)

    def test_force_newtons_and_higher_derivatives_are_core(self):
        force = self.u.hartree / self.u.bohr
        info = self.registry.explain_conversion(force, self.u.N, equivalences=())
        self.assertEqual(info['stage'], 'core')
        self.assertFactor(info['factor'], self.hartree / self.bohr)
        for order in range(7):
            source, target = self.u.hartree / self.u.bohr**order, self.u.eV / self.u.angstrom**order
            self.assertFactor(source.to(target, equivalences=()),
                              self.hartree / 1.602176634e-19 / (self.bohr / 1e-10)**order)

    def test_compound_wavenumber_and_kelvin_energy_derivatives(self):
        for order in range(5):
            target = self.u.hartree / self.u.bohr**order
            for source, energy_factor, policy in [
                    (self.u.wavenumber, 100 * self.h * self.c, None),
                    (self.u.kelvin, self.kb, ('thermal',))]:
                with self.subTest(order=order, policy=policy):
                    result = (source / self.u.angstrom**order).to(target, equivalences=policy)
                    self.assertFactor(result, energy_factor / self.hartree * (self.bohr / 1e-10)**order)

    def test_equivalences_lift_to_signed_and_fractional_powers(self):
        for power in (-3, -1, Fraction(1, 2), 1, 2, 3):
            for source, factor, policy, name in [
                    (self.u.wavenumber, 100 * self.h * self.c / self.hartree, None, 'wavenumber'),
                    (self.u.kelvin, self.kb / self.hartree, ('thermal',), 'thermal')]:
                with self.subTest(power=power, name=name):
                    info = self.registry.explain_conversion(source**power, self.u.hartree**power,
                                                            equivalences=policy)
                    self.assertFactor(info['factor'], factor**float(power))
                    self.assertEqual(info['bridges'][0]['power'], power)

    def test_frequency_and_angular_frequency_have_explicit_conventions(self):
        self.assertFactor(self.u.hartree.to(self.u.Hz, equivalences=('frequency',)), self.hartree / self.h)
        self.assertFactor(self.u.wavenumber.to(self.u.Hz, equivalences=('wavenumber', 'frequency')), 100 * self.c)
        with self.assertRaises(ConversionError):
            self.u.wavenumber.to(self.u.Hz, equivalences=('frequency',))
        self.assertFactor(self.u.hartree.to(self.u.rad / self.u.s, equivalences=('angular_frequency',)),
                          2 * math.pi * self.hartree / self.h)
        with self.assertRaises(ConversionError):
            self.u.hartree.to(self.u.rad / self.u.s, equivalences=('frequency',))
        with self.assertRaises(ConversionError):
            self.u.wavenumber.to(self.u.Hz, equivalences=('mass_energy',))
        self.assertFactor(self.u.kg.to(self.u.J, equivalences=('mass_energy',)), self.c**2)

    def test_cache_keys_and_diagnostic_probes_do_not_enable_policies(self):
        data_before = {key: dict(value) for key, value in self.registry.data.items()}
        self.u.kelvin.to(self.u.hartree, equivalences=('thermal',))
        for policy in ((), None, ('wavenumber',)):
            with self.subTest(policy=policy), self.assertRaises(ConversionError):
                self.u.kelvin.to(self.u.hartree, equivalences=policy)
        self.assertEqual(self.registry.data, data_before)
        self.assertFactor(self.u.kelvin.to(self.u.hartree, equivalences=('thermal',)), self.kb / self.hartree)

    def test_failure_messages_suggest_only_working_disabled_equivalences(self):
        cases = [(self.u.kelvin, self.u.hartree, (), 'thermal'),
                 (self.u.wavenumber, self.u.Hz, (), 'frequency'),
                 (self.u.kelvin / self.u.angstrom, self.u.hartree / self.u.bohr, (), 'thermal')]
        for source, target, policy, expected in cases:
            with self.subTest(expected=expected), self.assertRaises(ConversionError) as caught:
                source.to(target, equivalences=policy)
            message = str(caught.exception)
            self.assertIn('implicit energy equivalence', message)
            self.assertIn(expected, message)
            self.assertIn('equivalences=', message)
        with self.assertRaisesRegex(ValueError, 'unknown equivalences'):
            self.u.m.to(self.u.cm, equivalences=('typo',))

    def test_registry_changes_invalidate_existing_expressions_and_policies(self):
        self.registry.add_conversion('Furlongs', 'Meters', 201.168)
        expression = self.u.Furlongs / self.u.s
        self.assertFactor(expression.to(self.u.m / self.u.s), 201.168)
        self.registry.add_conversion('Furlongs', 'Meters', 200)
        self.assertFactor(expression.to(self.u.m / self.u.s), 200)
        with self.assertRaises(ValueError):
            self.registry.add_conversion('Kelvins', 'Hartrees', 1)
        self.assertFactor(self.u.kelvin.to(self.u.hartree, equivalences=('thermal',)), self.kb / self.hartree)
        self.registry.add_conversion('Meters', 'Meters', 1)
        self.assertFactor(self.u.m.to(self.u.cm), 100)
        self.registry.add_conversion('KiloWidgets', 'Meters', 2)
        self.assertFactor(self.u.KiloWidgets.to(self.u.m), 2)

    def test_custom_special_edges_are_optional_and_ambiguity_is_reported(self):
        factor = self.kb / self.hartree
        self.registry.add_conversion(self.u.kelvin, self.u.hartree, factor, equivalence='custom_thermal')
        with self.assertRaises(ConversionError):
            self.u.kelvin.to(self.u.hartree)
        self.assertFactor(self.u.kelvin.to(self.u.hartree, equivalences=('custom_thermal',)), factor)
        self.registry.add_conversion(self.u.kelvin, self.u.hartree, 2 * factor, equivalence='other_thermal')
        with self.assertRaisesRegex(ConversionError, 'ambiguous'):
            self.u.kelvin.to(self.u.hartree, equivalences=('thermal', 'other_thermal'))

    def test_namespaces_registries_and_constructor_defaults_are_isolated(self):
        thermal = UnitsDataHandler(default_equivalences='thermal')
        self.assertFactor(thermal.units.kelvin.to(thermal.units.hartree), self.kb / self.hartree)
        with self.assertRaises(ValueError):
            self.u.hartree / thermal.units.bohr
        with self.assertRaises(ConversionError):
            self.u.kelvin.to(self.u.hartree)

    def test_labels_follow_algebra_and_display_overrides_do_not_change_aliases(self):
        expression = self.u.hartree / self.u.bohr**2
        self.assertEqual(expression.label(), 'Eₕ·a₀⁻²')
        self.assertIn('1/2', (self.u.m**Fraction(1, 2)).label('latex'))
        factor = self.u.bohr.to(self.u.angstrom)
        self.registry.update_unit_labels({'BohrRadius': {'unicode': 'b'}})
        self.assertEqual(self.u.bohr.label(), 'b')
        self.assertFactor(self.u.bohr.to(self.u.angstrom), factor)

    def test_search_distinguishes_native_and_interpreted_energies(self):
        strict = {row['name']: row for row in self.registry.search('energy', equivalences=())}
        extended = {row['name']: row for row in self.registry.search('energy', equivalences=('wavenumber', 'thermal'))}
        self.assertIn('Hartrees', strict)
        self.assertNotIn('Kelvins', strict)
        self.assertNotIn('Wavenumbers', strict)
        self.assertEqual(extended['Kelvins']['equivalences'], ('thermal',))
        self.assertEqual(extended['Wavenumbers']['equivalences'], ('wavenumber',))


if __name__ == '__main__':
    unittest.main()

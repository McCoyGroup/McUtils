"""Regression checks for UnitsData's existing scalar/compound conversion interface."""
import itertools
import math
import unittest

from McUtils.Data import UnitsDataHandler
from McUtils.Data.ConstantsData import ConversionError, UnitGraph


class UnitsDataTests(unittest.TestCase):
    def setUp(self):
        self.units = UnitsDataHandler()

    def assertFactor(self, source, target, expected, rtol=2e-12, equivalences=None):
        actual = self.units.convert(source, target, equivalences=equivalences)
        self.assertTrue(math.isclose(actual, expected, rel_tol=rtol),
                        f'{source!r} -> {target!r}: {actual!r} != {expected!r}')

    def test_denominator_prefixes_and_powers(self):
        for power in (1, 2, 3, -1, -2, .5):
            with self.subTest(power=power):
                source = (('Hartrees', 1), ('Nanometers', -power))
                target = (('Hartrees', 1), ('Angstroms', -power))
                self.assertFactor(source, target, 10 ** -power)
                self.assertFactor(target, source, 10 ** power)
        self.assertFactor('Hartrees/Angstroms', 'Hartrees/Nanometers', 10)
        self.assertFactor('InverseNanometersSquared', 'InverseAngstromsSquared', .01)

    def test_path_powers_are_independent_of_lookup_order(self):
        scalar = 1 / 0.529177210903
        lookups = [
            ('AngstromsSquared', 'BohrRadiusSquared', scalar ** 2),
            ('AngstromsCubed', 'BohrRadiusCubed', scalar ** 3),
            ('InverseAngstromsSquared', 'InverseBohrRadiusSquared', scalar ** -2),
            ('Angstroms', 'BohrRadius', scalar),
        ]
        for ordered in itertools.permutations(lookups):
            self.units = UnitsDataHandler()
            for source, target, expected in ordered:
                self.assertFactor(source, target, expected)

    def test_explicit_powers_compose_with_name_modifiers(self):
        scalar = 1 / 0.529177210903
        self.assertFactor((('AngstromsSquared', 2),), (('BohrRadius', 4),), scalar ** 4)
        self.assertFactor((('InverseNanometersSquared', -1),),
                          (('Angstroms', 2),), 100)
        for power in (0, .5, -1, -2, 6):
            self.assertFactor((('Angstroms', power),), (('BohrRadius', power),), scalar ** power)
        self.assertFactor([['Angstroms', 2]], [['BohrRadius', 2]], scalar ** 2)

    def test_products_reorder_collect_and_cancel(self):
        energy = 27.211386245988
        length = 0.529177210903
        self.assertFactor('Hartrees BohrRadius', 'Angstroms ElectronVolts', energy * length)
        self.assertFactor('Angstroms Angstroms', 'BohrRadiusSquared', length ** -2)
        self.assertFactor('Angstroms BohrRadius', 'MetersSquared', 1e-10 * 5.29177210903e-11)
        self.assertFactor('Angstroms/BohrRadius', '', 1 / length)
        self.assertFactor('Hartrees BohrRadius/BohrRadius', 'ElectronVolts', energy)

    def test_force_and_higher_derivative_factors(self):
        energy = 27.211386245988
        length = 0.529177210903
        for order in range(7):
            source = (('Hartrees', 1), ('BohrRadius', -order))
            target = (('ElectronVolts', 1), ('Angstroms', -order))
            self.assertFactor(source, target, energy / length ** order)
        self.assertFactor('Hartrees/BohrRadiusSquared', 'ElectronVolts/AngstromsSquared', energy / length ** 2)

    def test_molar_quotients_associate_left_to_right(self):
        # Independent construction from the tabulated calorie, Avogadro, and Hartree values.
        kcal_to_hartree = 4184 / (6.02214076e23 * 4.3597447222071e-18)
        expected = kcal_to_hartree * 0.529177210903
        self.assertFactor('Kilocalories/Mole', 'Hartrees', kcal_to_hartree)
        for name in ('Kilocalories/Mole/Angstroms', 'Kilocalories/Angstroms/Mole',
                     'Kilocalories InverseMole InverseAngstroms'):
            self.assertFactor(name, 'Hartrees/BohrRadius', expected)
        self.assertFactor('Hartrees/BohrRadius', 'Kilocalories/Mole/Angstroms', 1 / expected)
        self.assertFactor((('Kilocalories/Mole', 2),), (('Hartrees', 2),), kcal_to_hartree ** 2)
        self.assertEqual(self.units.unit_label('Kilocalories/Mole/Angstroms'), 'kcal·mol⁻¹·Å⁻¹')

    def test_mass_prefixes_include_the_gram_scale(self):
        self.assertFactor('Grams', 'Kilograms', 1e-3)
        self.assertFactor('Milligrams', 'Kilograms', 1e-6)
        self.assertFactor('MicrogramsSquared', 'KilogramsSquared', 1e-18)
        self.assertFactor('InverseMilligrams', 'InverseKilograms', 1e6)
        self.assertFactor('KiloInverseMeters', 'InverseMeters', 1e3)
        self.assertFactor('MilliInverseMetersSquared', 'InverseMetersSquared', 1e-6)

    def test_spectroscopic_equivalences_and_conveniences_remain(self):
        self.assertFactor('Hartrees', 'Wavenumbers', 219474.6313632)
        self.assertFactor('Centihartrees', 'InverseMeters', 219474.6313632)
        self.assertFactor('Hartrees', 'Kelvins', 315775.02480407, equivalences=('thermal',))
        self.assertFactor('Hartrees', 'Hertz', 6.579683920502e15, equivalences=('frequency',))
        self.assertFactor('InverseHartrees', 'Meters', 1 / 21947463.13632)
        self.assertFactor('HartreesSquared', 'InverseMetersSquared', 21947463.13632 ** 2)
        self.assertFactor('AtomicMassUnits', 'AtomicUnitOfMass', 1822.888486217313)
        self.assertEqual(self.units.bohr_to_angstroms, self.units.convert('BohrRadius', 'Angstroms'))
        self.assertFactor(self.units.KilocaloriesPerMole, 'Hartrees',
                          4184 / (6.02214076e23 * 4.3597447222071e-18))
        self.assertFactor('Kilometers/Mole', 'KilometersPerMole', 1)
        self.assertFactor('OscillatorStrength', 'KilometersPerMole', 3.554206329390961e6)

    def test_registered_compound_definitions_and_their_powers(self):
        dipole = 25000000000000000 / 120080117814256593 / 10
        self.assertFactor('Debyes', ('ElementaryCharge', 'Nanometers'), dipole)
        self.assertFactor(('Nanometers', 'ElementaryCharge'), 'Debyes', 1 / dipole)
        self.assertFactor('DebyesSquared', (('ElementaryCharge', 2), ('Nanometers', 2)), dipole ** 2)
        self.assertFactor('InverseDebyes', ('InverseElementaryCharge', 'InverseNanometers'), 1 / dipole)
        self.assertFactor('Debyes Hartrees', ('ElementaryCharge', 'Nanometers', 'ElectronVolts'),
                          dipole * 27.211386245988)
        self.assertFactor('Debyes/Hartrees', ('ElementaryCharge', 'Nanometers', 'InverseElectronVolts'),
                          dipole / 27.211386245988)

    def test_powers_of_every_declared_conversion(self):
        records = [(key, record['Value'], record.get('Uncertainty', 0)) for key, record in self.units.data.items()
                   if isinstance(key, tuple) and 'Conversion' in record]
        for (source, target), value, uncertainty in records:
            for power in (1, 2, 3, -1, -2, .5):
                # Rounded NIST rows can differ within their stated uncertainty.
                tolerance = max(2e-8, 3 * abs(power) * uncertainty / abs(value)) if isinstance(uncertainty, (int, float)) else 2e-8
                with self.subTest(source=source, target=target, power=power):
                    self.assertFactor(((source, power),), ((target, power),), value ** power, rtol=tolerance, equivalences=tuple(self.units._bridges()))
                    self.assertFactor(((target, power),), ((source, power),), value ** -power, rtol=tolerance, equivalences=tuple(self.units._bridges()))

    def test_lookup_does_not_register_derived_rules(self):
        before_data = {key: dict(value) for key, value in self.units.data.items()}
        before_graph = {key: set(value) for key, value in self.units._unit_graph._graph.items()}
        self.units.convert('Angstroms', 'BohrRadius')
        self.units.convert('Hartrees/Angstroms', 'Hartrees/Nanometers')
        self.assertEqual(self.units.data, before_data)
        self.assertEqual(self.units._unit_graph._graph, before_graph)

    def test_registrations_invalidate_forward_reverse_and_powered_results(self):
        self.units.add_conversion('FixtureA', 'FixtureB', 2)
        self.units.add_conversion('FixtureB', 'FixtureC', 3)
        for source, target, expected in [
                ('FixtureA', 'FixtureC', 6), ('FixtureC', 'FixtureA', 1 / 6),
                ((('FixtureA', 2),), (('FixtureC', 2),), 36)]:
            self.assertFactor(source, target, expected)
        self.units.add_conversion('FixtureB', 'FixtureC', 4)
        self.assertFactor('FixtureA', 'FixtureC', 8)
        self.assertFactor('FixtureC', 'FixtureA', 1 / 8)
        self.assertFactor((('FixtureA', 2),), (('FixtureC', 2),), 64)
        self.units.add_conversion('FixtureB', 'FixtureA', .25)
        self.assertFactor('FixtureA', 'FixtureB', 4)
        self.assertFactor('FixtureA', 'FixtureC', 16)

    def test_handlers_do_not_share_registrations_or_record_mutations(self):
        other = UnitsDataHandler()
        self.assertIsNot(self.units.data, other.data)
        key = ('BohrRadius', 'Meters')
        self.assertIsNot(self.units.data[key], other.data[key])
        self.units.add_conversion('BohrRadius', 'Meters', 2)
        self.assertFactor('BohrRadius', 'Meters', 2)
        self.assertEqual(other.convert('BohrRadius', 'Meters'), 5.29177210903e-11)
        third = UnitsDataHandler()
        self.assertEqual(third.convert('BohrRadius', 'Meters'), 5.29177210903e-11)

    def test_reload_clears_registered_rules_and_cached_results(self):
        self.units.add_conversion('BohrRadius', 'Meters', 2)
        self.assertFactor('BohrRadius', 'Angstroms', 2e10)
        self.units.load()
        self.assertFactor('BohrRadius', 'Angstroms', .529177210903)

    def test_compound_registrations_invalidate_cached_expansions(self):
        self.units.add_conversion('FixtureDipole', ['ElementaryCharge', 'Nanometers'], 2)
        self.assertFactor('FixtureDipole', ('Coulombs', 'Meters'), 2 * 1.602176634e-19 * 1e-9)
        self.units.add_conversion('FixtureDipole', ['ElementaryCharge', 'Nanometers'], 3)
        self.assertFactor('FixtureDipole', ('Coulombs', 'Meters'), 3 * 1.602176634e-19 * 1e-9)

    def test_nested_compound_definitions_and_component_identities(self):
        self.units.add_conversion('FixtureA', (('FixtureB', 2), 'FixtureC'), 3)
        self.units.add_conversion('FixtureB', ('FixtureD', 'FixtureE'), 2)
        target = (('FixtureD', 4), ('FixtureE', 4), ('FixtureC', 2))
        self.assertFactor((('FixtureA', 2),), target, (3 * 2 ** 2) ** 2)

    def test_recursive_compound_rules_terminate_on_failure(self):
        self.units.add_conversion('FixtureA', ('FixtureB', 'FixtureC'), 2)
        self.units.add_conversion('FixtureB', ('FixtureA', 'FixtureD'), 3)
        with self.assertRaises(ConversionError):
            self.units.convert('FixtureA', 'Meters')

    def test_invalid_conversions_and_registration_factors(self):
        for source, target in [('Unknown', 'Unknown'), ('AngstromsSquared', 'BohrRadius'),
                               ('Hartrees/BohrRadius', 'Kelvins')]:
            with self.subTest(source=source, target=target), self.assertRaises(ConversionError):
                self.units.convert(source, target)
        for unit in ('Hartrees//BohrRadius', '/BohrRadius', 'Hartrees/'):
            with self.assertRaises(ValueError):
                self.units.convert(unit, 'Meters')
        for value in (0, math.inf, math.nan):
            with self.assertRaises(ValueError):
                self.units.add_conversion('FixtureA', 'FixtureB', value)
        with self.assertRaises(ValueError):
            self.units.add_conversion('FixtureA', 'FixtureA', 2)
        for power in (math.inf, math.nan):
            with self.assertRaises(ValueError):
                self.units.convert((('Meters', power),), 'Meters')

    def test_conversion_graph_uses_equality_shortest_paths_and_has_no_empty_node(self):
        self.units.data
        self.assertNotIn('', self.units._unit_graph)
        graph = UnitGraph([('start', 'a-long'), ('a-long', 'longer'), ('longer', 'end'),
                           ('start', 'z-short'), ('z-short', 'end')])
        end = ''.join(['e', 'n', 'd'])
        self.assertEqual(graph.find_path_bfs('start', end), ['start', 'z-short', 'end'])
        self.assertEqual(graph.find_path_bfs(end, end), [end])
        self.assertIsNone(graph.find_path_bfs('missing', end))


if __name__ == '__main__':
    unittest.main()

"""
Tests for `McUtils.Devutils` property cascades (`PropertyCascade`, `CascadingPropertyManager`, `cascading_property`,
`cascading_attribute`, `derived_property`).
"""

import unittest

from McUtils.Devutils import (
    PropertyCascade, CascadingPropertyManager, cascading_property, cascading_attribute, derived_property
)

__all__ = ["CascadeTests"]


class _Thing:
    cascade_dependencies = {'summary': {'depends_on': ['a', 'evaluator'], 'reset': '_summary'},
               'external': {'depends_on': ['a'], 'keyed': ['b']}}
    evaluator = cascading_attribute()
    calls = 0

    def __init__(self, a, b=0):
        self._cascade_manager = CascadingPropertyManager(self)
        self._a = a
        self._b = b
        self._evaluator = None

    @cascading_property
    def a(self):
        return self._a

    @a.setter
    def a(self, v):
        self._a = v

    @cascading_property
    def b(self):
        return self._b

    @b.setter
    def b(self, v):
        self._b = v

    @derived_property(depends_on=['a'])
    def double(self):
        self.calls += 1
        return self.a * 2

    @derived_property(depends_on=['double', 'b'])
    def total(self):
        return self.double + self.b + 1

    @derived_property(depends_on=['a'], settable=False)
    def readonly(self):
        return self.a


class CascadeTests(unittest.TestCase):

    def test_GraphQueries(self):
        c = PropertyCascade({'c': ['b'], 'b': ['a'], 'd': {'depends_on': ['a'], 'keyed': ['k']}})
        order = c.dependents('a')
        self.assertLess(order.index('b'), order.index('c'))
        self.assertEqual(set(order), {'b', 'c', 'd'})
        self.assertEqual(c.dependents('a', include_self=True)[0], 'a')
        self.assertEqual(c.ancestors('c'), {'a', 'b'})
        self.assertEqual(c.ancestors('d'), {'a', 'k'})
        self.assertEqual(c.ancestors('d', keyed=False), {'a'})
        # keyed dependencies reset the in-memory value, but don't make persistent entries stale
        self.assertTrue(c.is_stale('d', ['a']))
        self.assertFalse(c.is_stale('d', ['d']))  # overriding the in-memory value leaves what is stored alone
        self.assertFalse(c.is_stale('d', ['k']))
        self.assertTrue(c.is_stale('c', ['a']))
        self.assertFalse(c.is_stale('c', ['d']))
        self.assertTrue(c.is_stale('unknown', ['a']))
        self.assertFalse(c.is_stale('unknown', []))
        # cycles don't loop
        PropertyCascade({'x': ['y'], 'y': ['x']}).dependents('x')

    def test_DerivedValuesAreCachedAndReset(self):
        t = _Thing(2)
        self.assertEqual((t.double, t.double, t.calls), (4, 4, 1))
        self.assertEqual(t.total, 5)
        t.a = 3
        self.assertEqual((t.double, t.total, t.calls), (6, 7, 2))
        # `b` only invalidates what depends on it
        t.b = 10
        self.assertEqual((t.total, t.double, t.calls), (17, 6, 2))

    def test_SeedingAndReadOnly(self):
        t = _Thing(2)
        t.double = 100  # seeds without cascading
        self.assertEqual((t.double, t.calls), (100, 0))
        t.double = None
        self.assertEqual(t.double, 4)
        with self.assertRaises(AttributeError):
            t.readonly = 3

    def test_AttributeCascades(self):
        t = _Thing(2)
        t._summary = 'stale'
        t.evaluator = len
        self.assertEqual(t.evaluator, len)
        # a name with a reset slot clears it when anything it depends on changes
        self.assertIsNone(t._summary)
        t._summary = 'fresh'
        t.a = 9
        self.assertIsNone(t._summary)

    def test_SubclassesMergeCascades(self):
        class Sub(_Thing):
            @derived_property(depends_on=['total'])
            def triple_total(self):
                return 3 * self.total
        self.assertIn('triple_total', CascadingPropertyManager.graph_for(Sub))
        self.assertNotIn('triple_total', CascadingPropertyManager.graph_for(_Thing))
        s = Sub(1)
        self.assertEqual(s.triple_total, 9)
        s.a = 2
        self.assertEqual(s.triple_total, 15)

    def test_ListenersBatchAndSuspend(self):
        t = _Thing(2)
        seen = []
        t._cascade_manager.add_listener(lambda obj, changed, affected: seen.append((changed, affected)))
        t.a = 5
        self.assertEqual(seen[-1][0], ('a',))
        self.assertIn('double', seen[-1][1])
        n = len(seen)
        with t._cascade_manager.batch():
            t.a = 6
            t.b = 1
            self.assertEqual(len(seen), n)
        self.assertEqual(len(seen), n + 1)
        self.assertEqual(set(seen[-1][0]), {'a', 'b'})
        with t._cascade_manager.suspended():
            t.a = 7
        self.assertEqual(len(seen), n + 1)

    def test_MutedCascadesResetButDontNotify(self):
        t = _Thing(2)
        _ = t.double
        seen = []
        t._cascade_manager.add_listener(lambda *a: seen.append(a))
        with t._cascade_manager.muted():
            t.a = 4
        self.assertEqual(seen, [])
        self.assertEqual(t.double, 8)
        t.a = 5
        self.assertEqual(len(seen), 1)

    def test_AssignmentOfEqualValueIsSilent(self):
        t = _Thing(2)
        f = lambda x: x
        t.evaluator = f
        seen = []
        t._cascade_manager.add_listener(lambda *a: seen.append(a))
        t.evaluator = f
        self.assertEqual(seen, [])
        t.evaluator = None
        self.assertEqual(len(seen), 1)

    def test_FiniteDifferenceMatrixCascade(self):
        import numpy as np
        from McUtils.Zachary.Taylor.FiniteDifferenceFunction import RegularGridFiniteDifference
        m = RegularGridFiniteDifference(2, stencil=5, npts=20, mesh_spacing=0.1).mat
        a = m.matrix
        self.assertIs(m.matrix, a)
        m.mesh_spacing = 0.1  # an equal value doesn't invalidate it
        self.assertIs(m.matrix, a)
        m.mesh_spacing = 0.2
        b = m.matrix
        self.assertIsNot(b, a)
        self.assertTrue(np.allclose(b.toarray()[5, 3:8] * 0.2 ** 2, a.toarray()[5, 3:8] * 0.1 ** 2))
        m.npts = 30
        self.assertEqual(m.matrix.shape, (30, 30))

    def test_RegexPatternCascade(self):
        import McUtils.Parsers as P
        child = P.RegexPattern((P.Word, P.Number), joiner=" ")
        parent = P.RegexPattern((child, P.Number), joiner=" ")
        before = parent.compiled.pattern
        child.joiner = r"\s*,\s*"
        self.assertIn(",", child.compiled.pattern)  # the compiled pattern was stale before
        self.assertNotEqual(parent.compiled.pattern, before)  # and so were the parents'

    def test_ManagerIsExplicit(self):
        import copy, pickle, gc, weakref
        import McUtils.Devutils as dev
        from McUtils.Devutils import CascadeManagerError
        self.assertFalse(hasattr(dev, 'Cascading'))      # no mixin: classes inherit nothing
        self.assertEqual(_Thing.__mro__[1], object)
        t = _Thing(1)
        self.assertIsInstance(t._cascade_manager, CascadingPropertyManager)
        self.assertIs(t._cascade_manager.obj, t)

        class Bare:                                      # a manager is required, not created behind your back
            a = cascading_property(lambda self: self._a, lambda self, v: setattr(self, '_a', v))
        b = Bare()
        with self.assertRaises(CascadeManagerError):
            b.a = 1
        self.assertNotIn('_cascade_manager', b.__dict__)

        class Lazy:                                      # ...but it may be a property when construction should be delayed
            a = cascading_property(lambda self: self._a, lambda self, v: setattr(self, '_a', v))
            @property
            def _cascade_manager(self):
                if '_cm' not in self.__dict__:
                    self.__dict__['_cm'] = CascadingPropertyManager(self)
                return self.__dict__['_cm']
        lz = Lazy(); lz.a = 2
        self.assertEqual(lz.a, 2)

        # a copied object still points at the original's manager: that is an error, not silent sharing
        t2 = copy.copy(t)
        with self.assertRaises(CascadeManagerError):
            t2.a = 5
        t2._cascade_manager = CascadingPropertyManager(t2)
        t2.a = 5
        t3 = pickle.loads(pickle.dumps(t))
        with self.assertRaises(CascadeManagerError):
            t3.a = 2
        # the manager doesn't keep its object alive
        ref = weakref.ref(t)
        del t, t2, t3
        gc.collect()
        self.assertIsNone(ref())


if __name__ == '__main__':
    unittest.main()

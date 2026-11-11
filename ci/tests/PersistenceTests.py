"""
Tests for the persistence framework in `McUtils.Scaffolding`
(`Checkpointing`, `Serializers`, `Persistence`) that pin down known gaps.

These are plain `unittest` tests (no Peeves) that only write inside temp directories.
Tests for gaps that haven't been fixed yet are marked `@unittest.expectedFailure` and carry the
phase of the persistence plan (`claude_drafts/persistence/PLAN.md`) that fixes them, e.g.
`# phase 1`. When a phase lands, its tests start passing ("unexpected success") and the marker
should be removed in that same patch.
"""

import os as _test_os
import unittest as _test_unittest
_RUN_EXTRAS = _test_os.environ.get("MCUTILS_TEST_EXTRAS") == "1"


import enum, os, sys, shutil, subprocess, tempfile, textwrap, time, unittest
import numpy as np

import McUtils
from McUtils.Scaffolding import (
    Checkpointer, CheckpointerKeyError, JSONCheckpointer, NumPyCheckpointer, HDF5Checkpointer,
    PseudoPickler, ResourceManager, PersistenceLocation, PersistenceManager
)

__all__ = ["PersistenceTests"]


class _Plain:
    """Simple object the pseudopickler can walk through `__dict__`"""
    def __init__(self, a):
        self.a = a


class _Versioned:
    """Object with `to_state`/`from_state` that versions its state"""
    state_version = 2
    def __init__(self, x, y=None):
        self.x, self.y = x, y
    def to_state(self, serializer=None):
        return {'x': self.x, 'y': self.y}
    @classmethod
    def from_state(cls, state, serializer=None, version=None):
        obj = cls(state['x'], state['y'])
        obj.loaded_version = version
        return obj


class _Legacy:
    """Object whose `from_state` doesn't take a version"""
    def __init__(self, a):
        self.a = a
    def to_state(self, serializer=None):
        return {'a': self.a}
    @classmethod
    def from_state(cls, state, serializer=None):
        return cls(state['a'])


class _Color(enum.Enum):
    RED = 1
    GREEN = 'g'


def _module_level_function(x):
    return x


class _Cyclic:
    def __init__(self):
        self.me = self


def _open(fn, **opts):
    """Open a checkpoint by extension; `.legacy.npz` selects the whole-file NumPy backend, `.npz` the default"""
    if fn.endswith('.legacy.npz'):
        return NumPyCheckpointer(fn, backend='npz', **opts)
    return Checkpointer.from_file(fn, **opts)


def _open_dump(fn, **opts):
    """Like `_open`, but `.npz` always means the whole-file backend (tests of whole-file write semantics)"""
    if fn.endswith('.npz'):
        return NumPyCheckpointer(fn, backend='npz', **opts)
    return Checkpointer.from_file(fn, **opts)


def _subprocess_env():
    """Environment for child interpreters: the McUtils under test must be the one they import"""
    env = dict(os.environ)
    root = os.path.dirname(os.path.dirname(os.path.abspath(McUtils.__file__)))
    env['PYTHONPATH'] = os.pathsep.join([root] + [p for p in env.get('PYTHONPATH', '').split(os.pathsep) if p])
    return env


class PersistenceTests(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="persistence_tests_")
        PseudoPickler._cache = None  # a failing serialization can leave this set; don't let tests chain

    def tearDown(self):
        PseudoPickler._cache = None
        shutil.rmtree(self._tmp, ignore_errors=True)

    def path(self, name):
        return os.path.join(self._tmp, name)

    #region PseudoPickler
    def test_PseudoPickleRoundTrip(self):
        obj = {'x': _Plain(np.arange(3)), 'y': [1, 2.5, "s"]}
        pickler = PseudoPickler(allow_pickle=True)
        loaded = pickler.deserialize(pickler.serialize(obj))
        self.assertEqual(loaded['y'], [1, 2.5, "s"])

    def test_PseudoPickleSameObjectTwice(self):
        obj = {'x': _Plain(np.arange(3))}
        PseudoPickler().serialize(obj)
        PseudoPickler().serialize(obj)

    def test_PseudoPickleSharedReference(self):
        shared = _Plain(1)
        spec = PseudoPickler().serialize([shared, shared])
        loaded = PseudoPickler().deserialize(spec)
        self.assertIs(loaded[0], loaded[1])
    #endregion

    #region Checkpointers
    def test_CheckpointerWritesOnException(self):
        for ext in ['.npz', '.json']:
            fn = self.path('exc' + ext)
            with self.assertRaises(RuntimeError):
                with _open_dump(fn) as chk:
                    chk['a'] = np.arange(3)
                    raise RuntimeError("fail mid-block")
            with _open_dump(fn) as chk:
                self.assertEqual(chk['a'].tolist() if hasattr(chk['a'], 'tolist') else list(chk['a']), [0, 1, 2])

    def _run_child(self, fn, mode):
        """
        mode 'w': write key `a`; mode 'k': add key `b`, then die hard (no exit handlers) inside the block
        """
        child = textwrap.dedent("""
            import sys, os, numpy as np
            from McUtils.Scaffolding import Checkpointer, NumPyCheckpointer
            fn, mode = sys.argv[1:]
            chk = NumPyCheckpointer(fn, backend='npz') if fn.endswith('.npz') else Checkpointer.from_file(fn)
            with chk:
                chk['b' if mode == 'k' else 'a'] = np.arange(5)
                if mode == 'k':
                    os._exit(1)
        """)
        return subprocess.run([sys.executable, '-c', child, fn, mode], env=_subprocess_env(),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def _check_crash_keeps_contents(self, ext):
        fn = self.path('crash' + ext)
        self.assertEqual(self._run_child(fn, 'w').returncode, 0)
        before = os.path.getsize(fn)
        self.assertGreater(before, 0)
        self.assertEqual(self._run_child(fn, 'k').returncode, 1)
        self.assertEqual(os.path.getsize(fn), before)
        with _open_dump(fn) as chk:
            self.assertIn('a', list(chk.keys()))

    def test_NumPyCheckpointerCrashKeepsContents(self):
        self._check_crash_keeps_contents('.npz')

    def test_JSONCheckpointerCrashKeepsContents(self):
        self._check_crash_keeps_contents('.json')

    def _check_unchanged_block_leaves_file(self, ext):
        fn = self.path('same' + ext)
        with _open_dump(fn) as chk:
            chk['a'] = np.arange(3)
        before = os.stat(fn).st_mtime_ns
        time.sleep(0.05)
        with _open_dump(fn) as chk:
            chk['a']  # read only
        self.assertEqual(os.stat(fn).st_mtime_ns, before)

    def test_NumPyCheckpointerReadOnlyBlockDoesNotRewrite(self):
        self._check_unchanged_block_leaves_file('.npz')

    def test_JSONCheckpointerReadOnlyBlockDoesNotRewrite(self):
        self._check_unchanged_block_leaves_file('.json')

    def test_DumpCheckpointerFlushAndAutoflush(self):
        for ext in ['.npz', '.json']:
            fn = self.path('flush' + ext)
            chk = _open_dump(fn)
            with chk:
                chk['a'] = np.arange(3)
                self.assertFalse(os.path.exists(fn))  # nothing is written until the block exits...
                chk.flush()                           # ...or until asked
                self.assertTrue(os.path.exists(fn))
                mtime = os.stat(fn).st_mtime_ns
                time.sleep(0.05)
                chk.flush()                           # nothing new, so nothing rewritten
                self.assertEqual(os.stat(fn).st_mtime_ns, mtime)
            auto = _open_dump(self.path('auto' + ext), autoflush=True)
            with auto:
                auto['a'] = 1
                with _open_dump(self.path('auto' + ext)) as other:  # visible to a second reader mid-block
                    self.assertEqual(int(other['a']), 1)
                del auto['a']
                with _open_dump(self.path('auto' + ext)) as other:
                    self.assertNotIn('a', list(other.keys()))

    def test_DumpCheckpointerKeepsExistingKeysAndLeavesNoTempFiles(self):
        for ext in ['.npz', '.json']:
            fn = self.path('keys' + ext)
            for key in ['a', 'b']:
                with _open_dump(fn) as chk:
                    chk[key] = np.arange(3)
            with _open_dump(fn) as chk:
                self.assertEqual(sorted(chk.keys()), ['a', 'b'])
        self.assertEqual([f for f in os.listdir(self._tmp) if f.endswith('.tmp')], [])

    def test_DumpCheckpointerNestedBlocksWriteOnce(self):
        fn = self.path('nested.json')
        chk = _open_dump(fn)
        with chk:
            with chk:
                chk['a'] = 1
            self.assertFalse(os.path.exists(fn))  # the inner exit doesn't write
        self.assertTrue(os.path.exists(fn))
        with _open_dump(fn) as other:
            self.assertEqual(other['a'], 1)

    def test_DumpCheckpointerFileLikeTarget(self):
        import io
        buf = io.BytesIO()
        with NumPyCheckpointer(buf) as chk:
            chk['a'] = np.arange(3)
        size = buf.getbuffer().nbytes
        self.assertGreater(size, 0)
        with NumPyCheckpointer(buf) as chk:
            chk['a'] = np.arange(3)  # rewritten from the start, not appended
        self.assertEqual(buf.getbuffer().nbytes, size)

    def test_DumpCheckpointerKeepsPermissions(self):
        fn = self.path('perm.json')
        with _open_dump(fn) as chk:
            chk['a'] = 1
        os.chmod(fn, 0o640)
        with _open_dump(fn) as chk:
            chk['b'] = 2
        self.assertEqual(os.stat(fn).st_mode & 0o777, 0o640)

    def test_DumpCheckpointerFollowsSymlink(self):
        real = self.path('real.json')
        link = self.path('link.json')
        with _open_dump(real) as chk:
            chk['a'] = 1
        os.symlink(real, link)
        with _open_dump(link) as chk:
            chk['b'] = 2
        self.assertTrue(os.path.islink(link))
        with _open_dump(real) as chk:
            self.assertEqual(sorted(chk.keys()), ['a', 'b'])

    def test_CheckpointerCachedEval(self):
        for ext in ['.json', '.npz', '.legacy.npz'] + (['.hdf5'] if _RUN_EXTRAS else []):
            calls = []
            def gen():
                calls.append(1)
                return np.ones(3)
            fn = self.path('cached' + ext)
            for _ in range(2):
                with _open(fn) as chk:
                    val = chk.cached_eval('x', gen)
            self.assertEqual(len(calls), 1, ext)
            self.assertEqual(np.asarray(val).tolist(), [1., 1., 1.])

    def test_BuildCanonicalOmittedKeys(self):
        chk = Checkpointer.build_canonical({'file': self.path('omit.json'), 'keys': {'omitted_keys': ['a']}})
        self.assertEqual(chk.omitted_keys, ['a'])

    def test_BuildCanonicalAllowedKeys(self):
        chk = Checkpointer.build_canonical({'file': self.path('allow.json'), 'keys': {'allowed_keys': ['a']}})
        self.assertEqual(chk.allowed_keys, ['a'])
    #endregion

    #region `to_state` objects through each checkpoint format
    def _roundtrip_sparse(self, ext):
        from McUtils.Numputils import SparseArray
        sp = SparseArray.from_diag([1, 2, 3])
        fn = self.path('sparse' + ext)
        with Checkpointer.from_file(fn) as chk:
            chk['sp'] = sp
        with Checkpointer.from_file(fn) as chk:
            loaded = chk['sp']
        self.assertTrue(np.allclose(loaded.asarray(), sp.asarray()))

    def test_ToStateObjectJSON(self):
        self._roundtrip_sparse('.json')

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_ToStateObjectHDF5(self):
        self._roundtrip_sparse('.hdf5')

    def test_ToStateObjectNPZ(self):
        self._roundtrip_sparse('.npz')
    #endregion

    #region PseudoPickler protocol 2 (phase 4)
    def test_PseudoPickleStoresClassesByPath(self):
        spec = PseudoPickler().serialize(_Plain(1))
        self.assertEqual(spec['pseudopickle_protocol'], 2)
        self.assertEqual(spec['class'], {'module': _Plain.__module__, 'qualname': '_Plain'})
        loaded = PseudoPickler().deserialize(spec)  # no pickle needed to read it
        self.assertIsInstance(loaded, _Plain)
        self.assertEqual(loaded.a, 1)

    def test_PseudoPickleTypesBytesDtypes(self):
        pickler = PseudoPickler()
        value = {'t': _Plain, 'b': b'\x00\xff', 'ba': bytearray(b'ab'), 'd': np.dtype('float32')}
        spec = pickler.serialize(value)
        self.assertNotIn('pickle_data', str(spec))
        loaded = pickler.deserialize(spec)
        self.assertIs(loaded['t'], _Plain)
        self.assertEqual(loaded['b'], b'\x00\xff')
        self.assertIsInstance(loaded['ba'], bytearray)
        self.assertEqual(loaded['d'], np.dtype('float32'))

    def test_PseudoPickleUnsafeLoad(self):
        from McUtils.Scaffolding import UnsafeLoadError
        spec = PseudoPickler(allow_pickle=True, b64encode=True).serialize({'f': _module_level_function})
        # functions can only be stored with pickle, which can't be read without `allow_pickle`
        with self.assertRaises(UnsafeLoadError):
            PseudoPickler().deserialize(spec)
        with self.assertRaises(ValueError):
            PseudoPickler().serialize({'f': _module_level_function})

    def test_PseudoPickleAlias(self):
        spec = PseudoPickler().serialize(_Plain(3))
        spec['class'] = {'module': 'nowhere_at_all', 'qualname': 'OldName'}
        with self.assertRaises(ImportError):
            PseudoPickler().deserialize(spec)
        try:
            PseudoPickler.register_alias('nowhere_at_all:OldName', _Plain.__module__ + '._Plain')
            self.assertEqual(PseudoPickler().deserialize(spec).a, 3)
        finally:
            PseudoPickler._aliases.pop('nowhere_at_all:OldName', None)

    def test_PseudoPickleStateVersion(self):
        pickler = PseudoPickler()
        spec = pickler.serialize(_Versioned(1))
        self.assertEqual(spec['state_version'], 2)
        self.assertEqual(pickler.deserialize(spec).loaded_version, 2)
        legacy = pickler.serialize(_Legacy(5))  # `from_state` without `version` still loads
        self.assertNotIn('state_version', legacy)
        self.assertEqual(pickler.deserialize(legacy).a, 5)

    def test_PseudoPickleSharedReferenceInFile(self):
        shared = _Versioned(np.arange(3))
        for ext in ['.json', '.npz', '.legacy.npz'] + (['.hdf5'] if _RUN_EXTRAS else []):
            fn = self.path('shared' + ext)
            with _open(fn) as chk:
                chk['pair'] = [shared, {'again': shared}, _Versioned(1, shared)]
            with _open(fn) as chk:
                pair = chk['pair']
            self.assertIs(pair[0], pair[1]['again'], ext)
            self.assertIs(pair[0], pair[2].y, ext)

    def test_PseudoPickleSharedWrittenOnce(self):
        shared = _Plain(np.arange(1000))
        spec = PseudoPickler().serialize([shared, shared, shared])
        self.assertEqual(spec[1], {'pseudopickle_ref': spec[0]['pseudopickle_id']})
        self.assertEqual(spec[2], spec[1])

    def test_PseudoPickleCycles(self):
        with self.assertRaises(ValueError):
            PseudoPickler().serialize(_Cyclic())
        loaded = PseudoPickler(allow_pickle=True).deserialize(PseudoPickler(allow_pickle=True).serialize(_Cyclic()))
        self.assertIs(loaded.me, loaded)  # falls back to pickle, which handles cycles

    def _protocol1_file(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'TestData', 'persistence_tests', 'protocol1_checkpoint.json')

    def test_PseudoPickleProtocol1Fixture(self):
        import json
        from McUtils.Scaffolding import UnsafeLoadError, JSONSerializer
        from McUtils.Numputils import SparseArray
        fn = self._protocol1_file()
        with open(fn) as f:
            old_spec = json.load(f)['sparse']
        with self.assertRaises(UnsafeLoadError):
            PseudoPickler().deserialize(old_spec)  # protocol 1 stored the class as pickle bytes
        with self.assertRaises(UnsafeLoadError):  # and the default is not to load pickle
            with Checkpointer.from_file(fn) as chk:
                chk['sparse']
        with self.assertWarns(DeprecationWarning):
            with Checkpointer.from_file(fn, serializer=JSONSerializer(allow_pickle=True)) as chk:
                sp = chk['sparse']
        self.assertIsInstance(sp, SparseArray)
        self.assertEqual(sp.asarray().tolist(), np.diag([1., 2., 3.]).tolist())
        with Checkpointer.from_file(fn, serializer=JSONSerializer(allow_pickle=True)) as chk:
            self.assertEqual(chk['plain'].data, [1, 2, 3])
            self.assertEqual(np.asarray(chk['array']).tolist(), [0, 1, 2, 3])

    def test_PseudoPickleOldSpecsAreUpgradedOnSave(self):
        import shutil as _sh, warnings
        from McUtils.Scaffolding import JSONSerializer
        fn = self.path('upgrade.json')
        _sh.copy(self._protocol1_file(), fn)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', DeprecationWarning)
            with Checkpointer.from_file(fn, serializer=JSONSerializer(allow_pickle=True)) as chk:
                chk['sparse'] = chk['sparse']
        with warnings.catch_warnings():
            warnings.simplefilter('error', DeprecationWarning)
            with Checkpointer.from_file(fn) as chk:  # protocol 2: loads with the default (no pickle)
                chk['sparse']

    def test_AllowPickleDefaultsToFalse(self):
        from McUtils.Scaffolding import JSONSerializer, NumPySerializer, HDF5Serializer, PicklingSerializer
        self.assertFalse(PseudoPickler().allow_pickle)
        for ser in [JSONSerializer(), NumPySerializer(), PicklingSerializer()] + ([HDF5Serializer()] if _RUN_EXTRAS else []):
            self.assertFalse(ser.pickler.allow_pickle if hasattr(ser, 'pickler') else ser.pseudopickler.allow_pickle
                             if hasattr(ser, 'pseudopickler') else ser.psuedopickler.allow_pickle, type(ser).__name__)
        # unsupported objects are refused rather than silently pickled
        for ext in ['.json', '.npz'] + (['.hdf5'] if _RUN_EXTRAS else []):
            with self.assertRaises(ValueError):
                with Checkpointer.from_file(self.path('nopickle' + ext)) as chk:
                    chk['f'] = _module_level_function
    #endregion

    #region Serializers (phase 4)
    def _roundtrip_all(self, value, check):
        for ext in ['.json', '.npz', '.legacy.npz'] + (['.hdf5'] if _RUN_EXTRAS else []):
            fn = self.path('rt' + ext)
            if os.path.exists(fn):
                os.remove(fn)
            with _open(fn) as chk:
                chk['v'] = value
            with _open(fn) as chk:
                check(chk['v'], ext)

    def test_RoundTripObjectsWithNoneAndNesting(self):
        def check(loaded, ext):
            self.assertIsInstance(loaded, _Versioned, ext)
            self.assertIsNone(loaded.y['none'], ext)
            self.assertEqual(loaded.y['name'], 'abc', ext)
            self.assertEqual(loaded.y['n'], 3, ext)
            self.assertIsInstance(loaded.y['inner'], _Legacy, ext)
            self.assertEqual(np.asarray(loaded.y['inner'].a).tolist(), [1, 2], ext)
        self._roundtrip_all(_Versioned(np.arange(3), {'none': None, 'name': 'abc', 'n': 3, 'inner': _Legacy([1, 2])}), check)

    def test_RoundTripRaggedAndMixedLists(self):
        value = {'ragged': [[1, 2, 3], [4], []], 'mixed': [1, 'a', 2.5], 'empty': {}, 'strs': ['x', 'yy']}
        def check(loaded, ext):
            self.assertEqual([list(np.atleast_1d(v)) for v in loaded['ragged']], [[1, 2, 3], [4], []], ext)
            self.assertEqual([np.asarray(v).tolist() for v in loaded['mixed']], [1, 'a', 2.5], ext)
            self.assertEqual(len(loaded['empty']), 0, ext)
            self.assertEqual([str(v) for v in np.atleast_1d(loaded['strs'])], ['x', 'yy'], ext)
        self._roundtrip_all(value, check)

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_HDF5ReturnsStrings(self):
        fn = self.path('str.hdf5')
        with Checkpointer.from_file(fn) as chk:
            chk['s'] = ['O', 'H', 'H']
            chk['one'] = 'word'
        with Checkpointer.from_file(fn) as chk:
            self.assertEqual([str(x) for x in chk['s']], ['O', 'H', 'H'])
            self.assertTrue(all(isinstance(x, str) for x in chk['s']))
            self.assertEqual(chk['one'], 'word')

    def test_NumPySerializerCoordinateSetKeepsSystem(self):
        from McUtils.Coordinerds import CoordinateSet, CartesianCoordinates3D
        coords = CoordinateSet(np.random.rand(4, 3), CartesianCoordinates3D)
        def check(loaded, ext):
            self.assertIsInstance(loaded, CoordinateSet, ext)
            self.assertTrue(np.allclose(loaded, coords), ext)
            self.assertEqual(type(loaded.system), type(coords.system), ext)
        self._roundtrip_all(coords, check)
    #endregion

    #region Indexed NumPy backend and HDF5 keep_open (phase 5)
    def test_NumPyCheckpointerDefaultsToIndexed(self):
        from McUtils.Scaffolding import IndexedNumPyCheckpointer
        self.assertIsInstance(NumPyCheckpointer(self.path('new.npz')), IndexedNumPyCheckpointer)
        self.assertIsInstance(Checkpointer.from_file(self.path('new2.npz')), IndexedNumPyCheckpointer)
        self.assertIsInstance(Checkpointer.from_file(self.path('new.nptar')), IndexedNumPyCheckpointer)
        legacy = NumPyCheckpointer(self.path('old.npz'), backend='npz')
        self.assertIsInstance(legacy, NumPyCheckpointer)
        self.assertNotIsInstance(legacy, IndexedNumPyCheckpointer)
        with legacy:
            legacy['a'] = np.arange(3)
        # an existing whole-file archive keeps its backend
        again = Checkpointer.from_file(self.path('old.npz'))
        self.assertNotIsInstance(again, IndexedNumPyCheckpointer)
        with again:
            self.assertEqual(again['a'].tolist(), [0, 1, 2])
        with self.assertRaises(ValueError):
            NumPyCheckpointer(self.path('x.npz'), backend='nope')

    def test_IndexedSaveOnlyAppendsOneKey(self):
        import io, tarfile
        from McUtils.Scaffolding.Storage import IndexedTarStore
        fn = self.path('many.npz')
        with Checkpointer.from_file(fn) as chk:
            for i in range(50):
                chk['key%d' % i] = np.full(1000, i, dtype=np.float64)
        with open(fn, 'rb') as f:
            before = f.read()
        with tarfile.open(fileobj=io.BytesIO(before), mode='r:') as archive:
            previous_index = archive.getmember(IndexedTarStore._INDEX_NAME)
            previous_end = previous_index.offset_data + ((previous_index.size + 511) // 512) * 512
        with Checkpointer.from_file(fn) as chk:
            chk['key7'] = np.zeros(1000)
        with open(fn, 'rb') as f:
            after = f.read()
        # Publication updates the fixed locator; all earlier member bytes,
        # including the previous embedded index, remain untouched.
        self.assertEqual(after[1536:previous_end], before[1536:previous_end])
        growth = len(after) - len(before)
        with tarfile.open(fileobj=io.BytesIO(after), mode='r:') as archive:
            index_size = archive.getmember(IndexedTarStore._INDEX_NAME).size
        self.assertLess(growth, 3 * 8000 + 4096 + index_size)  # one key plus the current jump table
        with Checkpointer.from_file(fn) as chk:
            self.assertEqual(chk['key7'].tolist(), [0.] * 1000)
            self.assertEqual(chk['key8'][0], 8.)
            self.assertEqual(len(chk.keys()), 50)

    def test_IndexedBlocksArePublishedTogether(self):
        child = textwrap.dedent("""
            import sys, os, numpy as np
            from McUtils.Scaffolding import Checkpointer
            fn, auto = sys.argv[1:]
            with Checkpointer.from_file(fn, autoflush=(auto == '1')) as chk:
                chk['b'] = np.arange(6)
                chk['c'] = np.arange(7)
                os._exit(1)
        """)
        for auto, expected in [('0', ['a']), ('1', ['a', 'b', 'c'])]:
            fn = self.path('died%s.nptar' % auto)
            with Checkpointer.from_file(fn) as chk:
                chk['a'] = np.arange(5)
            subprocess.run([sys.executable, '-c', child, fn, auto], env=_subprocess_env())
            with Checkpointer.from_file(fn) as chk:
                self.assertEqual(sorted(chk.keys()), expected, auto)

    def test_IndexedReadsOwnPendingWritesAndErrorsStillPublish(self):
        fn = self.path('pending.nptar')
        with Checkpointer.from_file(fn) as chk:
            chk['a'] = np.arange(3)
        with self.assertRaises(RuntimeError):
            with Checkpointer.from_file(fn) as chk:
                chk['b'] = {'x': 1}
                chk['a'] = np.arange(4)
                self.assertEqual(chk['a'].tolist(), [0, 1, 2, 3])  # seen before it's published
                self.assertEqual(int(chk['b']['x']), 1)
                chk['gone'] = np.arange(2)
                del chk['gone']
                self.assertNotIn('gone', chk)
                self.assertEqual(sorted(chk.keys()), ['a', 'b'])
                raise RuntimeError("fail mid-block")
        with Checkpointer.from_file(fn) as chk:  # like the whole-file backends, the block's changes are kept
            self.assertEqual(sorted(chk.keys()), ['a', 'b'])
            self.assertEqual(chk['a'].tolist(), [0, 1, 2, 3])

    def test_IndexedUnchangedBlockLeavesFile(self):
        fn = self.path('same.nptar')
        with Checkpointer.from_file(fn) as chk:
            chk['a'] = np.arange(3)
        before = os.stat(fn).st_mtime_ns
        time.sleep(0.05)
        with Checkpointer.from_file(fn) as chk:
            chk['a']
        self.assertEqual(os.stat(fn).st_mtime_ns, before)

    def test_IndexedConcurrentWriters(self):
        fn = self.path('shared.nptar')
        child = textwrap.dedent("""
            import sys, numpy as np
            from McUtils.Scaffolding import Checkpointer
            fn, tag = sys.argv[1:]
            chk = Checkpointer.from_file(fn)
            for i in range(15):
                chk[tag + str(i)] = np.arange(i + 1)
        """)
        procs = [subprocess.Popen([sys.executable, '-c', child, fn, tag], env=_subprocess_env()) for tag in 'xy']
        for p in procs:
            self.assertEqual(p.wait(), 0)
        with Checkpointer.from_file(fn) as chk:
            self.assertEqual(len(chk.keys()), 30)
            self.assertEqual(chk['y14'].tolist(), list(range(15)))

    def test_IndexedMemmapDeleteCompactAndOddKeys(self):
        fn = self.path('ops.nptar')
        keys = ['plain', 'with/slash', '..', 'a.b', 'ünï']
        with Checkpointer.from_file(fn, mmap=True) as chk:
            for i, k in enumerate(keys):
                chk[k] = np.arange(100) + i
            chk['obj'] = {'x': 1, 'y': [1, 2]}
            chk['plain'] = np.arange(100000.)  # the old one is now dead weight
            chk.flush()
            self.assertEqual(sorted(chk.keys()), sorted(keys + ['obj']))
            self.assertIsInstance(chk['plain'], np.memmap)
            self.assertEqual(chk['with/slash'][5], 6)
            self.assertEqual(chk['..'][0], 2)
            self.assertEqual(int(chk['obj']['x']), 1)
            self.assertIn('a.b', chk)
            self.assertNotIn('missing', chk)
            del chk['a.b']
            self.assertNotIn('a.b', chk)
            with self.assertRaises(KeyError):
                chk['a.b']
            with self.assertRaises(KeyError):
                del chk['a.b']
            chk.flush()
            size = os.path.getsize(fn)
            chk.compact()
        with Checkpointer.from_file(fn) as chk:
            self.assertEqual(sorted(chk.keys()), sorted(set(keys) - {'a.b'} | {'obj'}))
            self.assertEqual(len(chk['plain']), 100000)
        self.assertLessEqual(os.path.getsize(fn), size)

    def test_IndexedAllowedKeysAndInitialCache(self):
        fn = self.path('allowed.nptar')
        chk = NumPyCheckpointer(fn, cache={'seed': np.arange(2)}, allowed_keys=['seed', 'ok'])
        with chk:
            self.assertEqual(chk['seed'].tolist(), [0, 1])
            chk['ok'] = np.arange(3)
            with self.assertRaises(CheckpointerKeyError):
                chk['nope'] = np.arange(3)

    def test_ConvertNumPyCheckpointFormats(self):
        from McUtils.Scaffolding import IndexedNumPyCheckpointer
        fn = self.path('conv.npz')
        data = {'a': np.arange(4.), 'b': {'x': np.eye(2), 'name': 'hi'}, 'c': [1, 2, 3]}
        with NumPyCheckpointer(fn, backend='npz') as chk:
            for k, v in data.items():
                chk[k] = v
        NumPyCheckpointer.convert_file(fn, to='indexed')
        self.assertEqual(NumPyCheckpointer.sniff_backend(fn), 'indexed')
        self.assertFalse([f for f in os.listdir(self._tmp) if '.tmp' in f])
        with Checkpointer.from_file(fn) as chk:
            self.assertIsInstance(chk, IndexedNumPyCheckpointer)
            self.assertEqual(chk['a'].tolist(), [0., 1., 2., 3.])
            self.assertTrue(np.allclose(chk['b']['x'], np.eye(2)))
            self.assertEqual(np.asarray(chk['c']).tolist(), [1, 2, 3])
        NumPyCheckpointer.convert_file(fn, to='npz')
        self.assertEqual(NumPyCheckpointer.sniff_backend(fn), 'npz')
        with Checkpointer.from_file(fn) as chk:
            self.assertEqual(chk['a'].tolist(), [0., 1., 2., 3.])
            self.assertEqual(np.asarray(chk['c']).tolist(), [1, 2, 3])
        NumPyCheckpointer.convert_file(fn, to='npz')  # already there: nothing to do

    @_test_unittest.skipUnless(_RUN_EXTRAS, "optional dependencies; set MCUTILS_TEST_EXTRAS=1")
    def test_HDF5KeepOpen(self):
        fn = self.path('kept.hdf5')
        chk = HDF5Checkpointer(fn, keep_open=True)
        for i in range(3):
            with chk:
                chk['k%d' % i] = np.arange(i + 1)
        self.assertFalse(chk._kept.closed)  # still open between blocks
        with chk:
            self.assertEqual(chk['k2'].tolist(), [0, 1, 2])
        chk.close()
        self.assertIsNone(chk._kept)
        with HDF5Checkpointer(fn) as other:
            self.assertEqual(sorted(other.keys()), ['k0', 'k1', 'k2'])
        plain = HDF5Checkpointer(self.path('plain.hdf5'))
        with plain:
            plain['a'] = np.arange(2)
        self.assertIsNone(plain._kept)
    #endregion

    #region ResourceManager / PersistenceLocation / PersistenceManager
    def test_ResourceManagerJSON(self):
        class JSONResources(ResourceManager):
            json_resource = True
            binary_resource = False
        manager = JSONResources(location=self.path('res'))
        self.assertEqual(manager.get_resource('a', resource_function=lambda n: {'n': n}), {'n': 'a'})

    def test_ResourceManagerBinary(self):
        class Resources(ResourceManager):
            pass
        manager = Resources(location=self.path('res'))
        self.assertIsNone(manager.get_resource('a'))
        self.assertEqual(manager.get_resource('a', resource_function=lambda n: n.encode()), b'a')
        self.assertEqual(list(manager.list_resources()), ['a'])

    def test_ResourceManagerMetadata(self):
        class Resources(ResourceManager):
            def get_resource_metadata(self, loc):
                return {'tag': 1}
        manager = Resources(location=self.path('res'), write_metadata=True)
        manager.get_resource('a', resource_function=lambda n: n.encode())
        self.assertTrue(os.path.exists(manager.get_resource_path(manager.get_metadata_filename('a'))))

    def test_PersistenceLocationRelativeName(self):
        loc = PersistenceLocation("persistence_tests_relative_store")
        self.assertTrue(os.path.isdir(os.path.dirname(loc.loc)))

    def test_PersistenceLocationExistingDirectory(self):
        loc = PersistenceLocation(self._tmp)
        self.assertEqual(loc.loc, os.path.abspath(self._tmp))
        self.assertFalse(loc.delete)

    def test_ConfigPersistenceFrameworkIsDeprecated(self):
        import warnings
        from McUtils.Devutils import Deprecation
        from McUtils.Scaffolding import JobManager
        for name, build in [
            ("McUtils.Scaffolding.PersistenceManager", lambda: PersistenceManager(_Plain, self._tmp)),
            ("McUtils.Scaffolding.JobManager", lambda: JobManager(self._tmp)),
        ]:
            Deprecation._WARNED.discard(name)
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                build()
            self.assertTrue(
                any(issubclass(w.category, Deprecation.McUtilsDeprecationWarning) and name.split('.')[-1] in str(w.message)
                    for w in caught),
                name
            )

    def test_ObjectBackers(self):
        import McUtils.Scaffolding as scaffolding
        self.assertFalse(hasattr(scaffolding, 'FileBackedObjectManager'))  # removed, nothing used it
        self.assertFalse(hasattr(scaffolding, 'BaseObjectManager'))  # merged into `SharedObjectManager`
        from McUtils.Parallelizers.SharedMemory import SharedObjectManager
        self.assertTrue(hasattr(SharedObjectManager, 'get_basename'))
        self.assertTrue(isinstance(SharedObjectManager.basename, property))

    def test_PseudoPickleInstancesDontShareMemo(self):
        shared = _Plain(1)
        PseudoPickler().serialize({'a': shared})
        PseudoPickler().serialize({'a': shared}) # a second instance (and a second call) starts clean
        pickler = PseudoPickler()
        pickler.serialize({'a': shared})
        pickler.serialize({'a': shared})

    #endregion

    #region Shared file primitives and fingerprints (phase 3)
    def test_AtomicFileKeepsOldContentsOnError(self):
        from McUtils.Devutils import atomic_file
        fn = self.path('a.txt')
        with atomic_file(fn, 'w') as f:
            f.write('old')
        with self.assertRaises(RuntimeError):
            with atomic_file(fn, 'w') as f:
                f.write('new')
                raise RuntimeError
        self.assertEqual(open(fn).read(), 'old')
        self.assertEqual(os.listdir(self._tmp), ['a.txt'])

    def test_AtomicFileNoOverwrite(self):
        from McUtils.Devutils import atomic_write
        fn = self.path('b.txt')
        atomic_write(fn, 'one', overwrite=False)
        with self.assertRaises(FileExistsError):
            atomic_write(fn, 'two', overwrite=False)
        self.assertEqual(open(fn).read(), 'one')
        self.assertEqual(os.listdir(self._tmp), ['b.txt'])

    def test_AtomicFileFollowsSymlinkAndKeepsMode(self):
        from McUtils.Devutils import atomic_write
        real = self.path('real.txt')
        link = self.path('link.txt')
        atomic_write(real, 'x')
        os.chmod(real, 0o600)
        try:
            os.symlink(real, link)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable")
        atomic_write(link, 'y')
        self.assertTrue(os.path.islink(link))
        self.assertEqual(open(real).read(), 'y')
        self.assertEqual(os.stat(real).st_mode & 0o777, 0o600)

    def test_AtomicDir(self):
        from McUtils.Devutils import atomic_dir
        target = self.path('d')
        with atomic_dir(target) as tmp:
            open(os.path.join(tmp, 'f'), 'w').write('1')
        with self.assertRaises(RuntimeError):
            with atomic_dir(target) as tmp:
                open(os.path.join(tmp, 'g'), 'w').write('2')
                raise RuntimeError
        self.assertEqual(os.listdir(target), ['f'])
        with atomic_dir(target) as tmp:
            open(os.path.join(tmp, 'g'), 'w').write('2')
        self.assertEqual(os.listdir(target), ['g'])
        self.assertEqual(sorted(os.listdir(self._tmp)), ['d'])

    def test_FileStoreLockIsReentrant(self):
        from McUtils.Devutils import FileStoreLock
        lock = FileStoreLock(self.path('x.lock'))
        with lock():
            with lock():
                pass

    def test_FileStoreLockExcludesProcesses(self):
        child = textwrap.dedent("""
            import sys, time
            from McUtils.Devutils import FileStoreLock
            with FileStoreLock(sys.argv[1])():
                print('locked', flush=True)
                time.sleep(1.0)
        """)
        from McUtils.Devutils import FileStoreLock
        lockfile = self.path('p.lock')
        proc = subprocess.Popen([sys.executable, '-c', child, lockfile], env=_subprocess_env(), stdout=subprocess.PIPE)
        try:
            self.assertEqual(proc.stdout.readline().strip(), b'locked')
            start = time.time()
            with FileStoreLock(lockfile)():
                waited = time.time() - start
            self.assertGreater(waited, 0.3)
        finally:
            proc.wait()

    def test_FingerprintStableAndSensitive(self):
        from McUtils.Devutils import fingerprint
        a = {'x': np.arange(4.), 'y': [1, 'a'], 'z': {3, 1, 2}}
        b = {'z': {1, 2, 3}, 'y': [1, 'a'], 'x': np.arange(4.)}
        self.assertEqual(fingerprint(a), fingerprint(b))
        b['x'] = np.arange(4.) + 1e-9
        self.assertNotEqual(fingerprint(a), fingerprint(b))
        self.assertEqual(len(fingerprint(a)), 64)

    def test_FingerprintImmutableBytesByContent(self):
        from McUtils.Devutils import fingerprint, freeze
        value = b'\\x00condition\\xff'
        copy = bytes(bytearray(value))
        self.assertEqual(fingerprint(value), fingerprint(copy))
        self.assertNotEqual(fingerprint(value), fingerprint(value + b'!'))
        self.assertNotEqual(fingerprint(value), fingerprint(value.hex()))
        self.assertNotEqual(fingerprint(value), fingerprint(np.frombuffer(value, dtype=np.uint8)))
        self.assertEqual(fingerprint({value: [copy]}), fingerprint({copy: [value]}))
        frozen = freeze(value)
        self.assertEqual(frozen[:2], ['bytes', len(value)])
        self.assertEqual(len(frozen[2]), 64)
        self.assertEqual(fingerprint(b''), fingerprint(bytes()))
        class BinaryTag(bytes, enum.Enum):
            ONE = b'one'
        self.assertEqual(freeze(BinaryTag.ONE)[0], 'enum')
        self.assertNotEqual(fingerprint(BinaryTag.ONE), fingerprint(b'one'))
        custom = [(lambda v: type(v) is bytes,
                   lambda v, kind, rec: ['custom-bytes', v.hex()])]
        self.assertEqual(freeze(value, handlers=custom)[0], 'custom-bytes')
        class Payload(bytes):
            pass
        a, b = Payload(b'x'), Payload(b'x')
        a.mode, b.mode = 1, 2
        self.assertNotEqual(fingerprint(a), fingerprint(b))

    def test_FingerprintHookExcludeAndSharedRefs(self):
        from McUtils.Devutils import fingerprint

        class Hooked:
            def __init__(self, a, runtime): self.a, self.runtime = a, runtime
            def __fingerprint__(self): return {'a': self.a}

        class Excluding:
            __fingerprint_exclude__ = ('cache',)
            def __init__(self, a, cache): self.a, self.cache = a, cache

        self.assertEqual(fingerprint(Hooked(1, object())), fingerprint(Hooked(1, object())))
        self.assertNotEqual(fingerprint(Hooked(1, 0)), fingerprint(Hooked(2, 0)))
        self.assertEqual(fingerprint(Excluding(1, {'x': 1})), fingerprint(Excluding(1, {'y': 2})))
        self.assertEqual(fingerprint(_Plain(3), exclude_attrs=('a',)), fingerprint(_Plain(4), exclude_attrs=('a',)))
        shared = _Plain(1)
        self.assertNotEqual(fingerprint([shared, shared]), fingerprint([_Plain(1), _Plain(1)]))
        with self.assertRaises(TypeError):
            fingerprint(object())

    def test_EnumMembersRoundTrip(self):
        from McUtils.Scaffolding import ObjectStore
        pp = PseudoPickler()
        self.assertIs(pp.deserialize(pp.serialize(_Color.GREEN)), _Color.GREEN)
        holder = _Plain([_Color.RED, {'c': _Color.GREEN}])
        again = pp.deserialize(pp.serialize(holder))
        self.assertEqual(again.a, [_Color.RED, {'c': _Color.GREEN}])
        for fn in ('enum.json', 'enum.nptar'):
            with Checkpointer.from_file(self.path(fn)) as chk:
                chk['holder'] = holder
            with Checkpointer.from_file(self.path(fn)) as chk:
                self.assertEqual(chk['holder'].a, [_Color.RED, {'c': _Color.GREEN}])
        store = ObjectStore(self.path('enum_store'))
        self.assertIs(store.get(store.put(_Color.RED)), _Color.RED)
    #endregion

    #region Entry store and object store (phase 6)
    def test_EntryStoreWriteStageAliasAndKeys(self):
        import hashlib, json
        from McUtils.Devutils import EntryStore

        k1, k2 = (hashlib.sha256(s).hexdigest() for s in (b'1', b'2'))
        for shard in (2, 0):
            class Store(EntryStore):
                pass
            Store.shard = shard
            store = Store(self.path('entries%d' % shard))
            store.write(k1, {'a': 1}, files={'x/y.txt': 'hi', 'b.bin': b'\x00\x01'})
            self.assertTrue(store.has(k1) and not store.has(k2))
            self.assertEqual(store.read_meta(k1)['a'], 1)
            self.assertEqual(store.read_meta(k1)['key'], k1)
            self.assertEqual(store.read_file(k1, 'x/y.txt'), 'hi')
            self.assertEqual(store.read_file(k1, 'b.bin', binary=True), b'\x00\x01')
            with store.stage(k2, {'b': 2}) as staged:
                with open(staged.file('p.txt'), 'w') as f:
                    f.write('payload')
                self.assertFalse(store.has(k2))
            self.assertEqual(store.keys(), sorted([k1, k2]))
            self.assertEqual(store.read_file(k2, 'p.txt'), 'payload')
            # a staged copy loses against an existing entry (a concurrent writer got there first)
            with store.stage(k2, {'b': 3}):
                pass
            self.assertEqual(store.read_meta(k2)['b'], 2)
            with store.stage(k2, {'b': 3}, replace=True):
                pass
            self.assertEqual(store.read_meta(k2)['b'], 3)
            # an error in the block publishes nothing and leaves no temporary directory
            with self.assertRaises(RuntimeError):
                with store.stage(hashlib.sha256(b'3').hexdigest(), {}):
                    raise RuntimeError
            self.assertEqual(len(store.keys()), 2)
            self.assertEqual([n for n in os.listdir(store.root) if n.startswith('.')], [])
            # aliases
            store.set_alias('latest', k1)
            self.assertEqual(store.resolve_alias('latest'), k1)
            self.assertIsNone(store.resolve_alias('missing'))
            self.assertEqual(store.prune([k2]), [k1])
            self.assertIsNone(store.resolve_alias('latest'))  # target is gone
            self.assertEqual(store.keys(), [k2])

    def test_EntryStoreRejectsBadKeysAndNames(self):
        from McUtils.Devutils import EntryStore
        store = EntryStore(self.path('bad'))
        for key in ('../x', 'abc', '', None, 'G' * 64):
            with self.assertRaises(ValueError):
                store.entry_path(key)
        key = 'a' * 64
        for name in ('../x', '/abs', 'a//b', ''):
            with self.assertRaises(ValueError):
                store.write(key, {}, files={name: 'x'})
        with self.assertRaises(ValueError):
            store.write(key, {}, files={'meta.json': 'x'})
        with self.assertRaises(ValueError):
            store.set_alias('../up', key)

    def test_EntryStoreGcLeastRecentlyUsedAndAge(self):
        import hashlib
        from McUtils.Devutils import EntryStore
        store = EntryStore(self.path('gc'))
        keys = [hashlib.sha256(bytes([i])).hexdigest() for i in range(4)]
        for i, k in enumerate(keys):
            store.write(k, {}, files={'d': b'x' * 1000})
            os.utime(store.entry_path(k, 'meta.json'), (1000 + i, 1000 + i))
        store.touch(keys[0])  # now the most recently used
        size = store.entry_size(keys[0])
        self.assertEqual(store.gc(max_bytes=2 * size, dry_run=True), [keys[1], keys[2]])
        self.assertEqual(len(store.keys()), 4)
        self.assertEqual(store.gc(max_bytes=2 * size, protect=[keys[1]]), [keys[2], keys[3]])
        self.assertEqual(sorted(store.keys()), sorted([keys[0], keys[1]]))
        os.utime(store.entry_path(keys[1], 'meta.json'), (1, 1))
        self.assertEqual(store.gc(max_age=3600), [keys[1]])
        self.assertEqual(store.keys(), [keys[0]])

    def test_ObjectStoreExactRoundTrip(self):
        from McUtils.Scaffolding import ObjectStore
        from McUtils.Coordinerds import CoordinateSet
        store = ObjectStore(self.path('os1'))
        coords = CoordinateSet(np.random.rand(3, 3))
        value = {'i': 1, 'f': 2.5, 's': 'text', 'n': None, 'l': [1, [2, 3]], 't': (1, (2, 3)),
                 'a': np.arange(6.).reshape(2, 3), 'a16': np.arange(4, dtype=np.int16), 'cs': coords,
                 'o': _Plain(np.ones(2)), 'v': _Versioned(1, (4, 5))}
        key = store.put(value)
        self.assertEqual(key, store.put(value))  # idempotent
        loaded = store.get(key)
        self.assertEqual(list(loaded), list(value))
        for name in ('i', 'f', 's', 'n', 'l', 't'):
            self.assertEqual(loaded[name], value[name])
            self.assertIs(type(loaded[name]), type(value[name]))
        self.assertEqual(loaded['a16'].dtype, np.int16)
        self.assertTrue(np.array_equal(loaded['a'], value['a']))
        self.assertIsInstance(loaded['cs'], CoordinateSet)
        self.assertTrue(np.allclose(loaded['cs'], coords))
        self.assertIsInstance(loaded['o'], _Plain)
        self.assertTrue(np.array_equal(loaded['o'].a, np.ones(2)))
        self.assertEqual(loaded['v'].y, (4, 5))
        self.assertEqual(loaded['v'].loaded_version, 2)
        # non-mapping values
        for obj in (np.arange(5), coords, _Plain([1, 2]), 'just text', (1, 2)):
            got = store.get(store.put(obj))
            self.assertIs(type(got), type(obj))
        with self.assertRaises(KeyError):
            store.get('0' * 64)
        self.assertIsNone(store.get('0' * 64, default=None))

    def test_ObjectStoreLazyMmapAndMeta(self):
        from McUtils.Scaffolding import ObjectStore
        store = ObjectStore(self.path('os2'), provenance={'source': 'tests'})
        big = np.arange(1000.)
        key = store.put({'big': big, 'small': 3, 'name': 'x'}, meta={'step': 7})
        meta = store.meta(key)
        self.assertEqual(meta['class'], 'builtins:dict')
        self.assertEqual(meta['provenance'], {'source': 'tests', 'step': 7})
        self.assertEqual(meta['fields'], {'big': 'array', 'small': 'tree', 'name': 'tree'})
        self.assertGreater(meta['payload_bytes'], big.nbytes)
        self.assertIn('host', meta['created_by'])
        lazy = store.get(key, lazy=True, mmap=True)
        self.assertEqual(sorted(lazy), ['big', 'name', 'small'])
        self.assertEqual(len(lazy), 3)
        self.assertIsInstance(lazy['big'], np.memmap)
        self.assertEqual(lazy['small'], 3)
        with self.assertRaises(KeyError):
            lazy['nope']
        self.assertEqual(lazy.load()['name'], 'x')
        vkey = store.put(_Versioned(1))
        self.assertEqual(store.meta(vkey)['state_version'], 2)
        self.assertTrue(store.meta(vkey)['class'].endswith(':_Versioned'))
        with self.assertRaises(TypeError):
            list(store.get(vkey, lazy=True))

    def test_ObjectStoreKeysFindAndReplace(self):
        from McUtils.Scaffolding import ObjectStore
        from McUtils.Devutils import fingerprint
        store = ObjectStore(self.path('os3'))
        a = store.put({'x': 1}, meta={'kind': 'a', 'n': 1})
        b = store.put({'x': 2}, meta={'kind': 'b', 'n': 2})
        c = store.put(_Plain(1), meta={'kind': 'a', 'n': 3})
        self.assertEqual(a, fingerprint({'x': 1}))
        self.assertEqual(sorted(store.keys()), sorted([a, b, c]))
        self.assertEqual(sorted(store.find(provenance__kind='a')), sorted([a, c]))
        self.assertEqual(store.find(**{'provenance.n': lambda n: n == 2}), [b])
        self.assertEqual(store.find(**{'class': 'builtins:dict', 'provenance__kind': 'b'}), [b])
        self.assertEqual(store.put({'x': 99}, key=a), a)  # existing entries are kept
        self.assertEqual(store.get(a)['x'], 1)
        store.put({'x': 99}, key=a, replace=True)
        self.assertEqual(store.get(a)['x'], 99)
        self.assertEqual(store.prune([a]), sorted([b, c]))
        self.assertEqual(store.keys(), [a])
        with store.transaction():  # reentrant
            with store.lock():
                store.put([1, 2])
        self.assertEqual(len(store.keys()), 2)

    def test_ObjectStoreCachedEval(self):
        from McUtils.Scaffolding import ObjectStore
        store = ObjectStore(self.path('os4'))
        calls = []
        def generate():
            calls.append(1)
            return {'v': np.arange(4.), 'tag': 'made'}
        first = store.cached_eval(('energy', 1, {'order': 2}), generate)
        again = store.cached_eval(('energy', 1, {'order': 2}), generate)
        self.assertEqual(len(calls), 1)
        self.assertTrue(np.array_equal(first['v'], again['v']))
        store.cached_eval(('energy', 1, {'order': 3}), generate)  # a changed part misses
        store.cached_eval((1, 'energy', {'order': 2}), generate)  # so does a changed order
        self.assertEqual(len(calls), 3)
        self.assertEqual(store.cached_eval('single', generate, lazy=True)['tag'], 'made')
        # a fresh store on the same directory (another process) hits too
        self.assertEqual(len(ObjectStore(self.path('os4')).keys()), 4)
        ObjectStore(self.path('os4')).cached_eval(('energy', 1, {'order': 2}), generate)
        self.assertEqual(len(calls), 4)  # the fresh store hit the entry made earlier

    def test_ObjectStoreSizePolicyAndSafety(self):
        from McUtils.Scaffolding import ObjectStore
        from McUtils.Scaffolding.ObjectStore import ObjectTooLarge
        small = ObjectStore(self.path('os5'), max_entry_bytes=20000)
        with self.assertRaises(ObjectTooLarge):
            small.put(np.zeros(100000))
        self.assertEqual(small.keys(), [])  # nothing half-written
        self.assertEqual([n for n in os.listdir(small.root) if n.startswith('.stage')], [])
        calls = []
        value = small.cached_eval('big', lambda: calls.append(1) or np.zeros(100000))
        self.assertEqual(value.shape, (100000,))
        small.cached_eval('big', lambda: calls.append(1) or np.zeros(100000))
        self.assertEqual(len(calls), 2)  # too large to cache, so it's recomputed
        bounded = ObjectStore(self.path('os6'), max_bytes=25000)
        keys = [bounded.put(np.full(100, i, dtype=float), key=ObjectStore.key_for(bounded, i)) for i in range(5)]
        self.assertIn(keys[-1], bounded.keys())  # the newest entry is protected
        self.assertLess(len(bounded.keys()), 5)
        self.assertLessEqual(sum(bounded.entry_size(k) for k in bounded.keys()), 25000 + bounded.entry_size(keys[-1]))
        with self.assertRaises(ValueError):  # the pseudopickler can't express a set, and pickle is off
            ObjectStore(self.path('os7')).put({'bad': {1, 2}})

    def test_ObjectStoreDefaultRoot(self):
        from McUtils.Scaffolding import ObjectStore
        old = os.environ.get('MCUTILS_STORE')
        try:
            os.environ['MCUTILS_STORE'] = self.path('envstore')
            self.assertEqual(ObjectStore.default_root(), self.path('envstore'))
            self.assertIs(ObjectStore.default(), ObjectStore.default())
            key = ObjectStore.default().put([1, 2, 3])
            self.assertTrue(os.path.isdir(os.path.join(self.path('envstore'), key[:2], key)))
            del os.environ['MCUTILS_STORE']
            self.assertTrue(ObjectStore.default_root().endswith(os.path.join('McUtils', 'store')))
        finally:
            if old is None:
                os.environ.pop('MCUTILS_STORE', None)
            else:
                os.environ['MCUTILS_STORE'] = old

    def test_ObjectStoreConcurrentWriters(self):
        child = textwrap.dedent("""
            import sys, numpy as np
            from McUtils.Scaffolding import ObjectStore
            root, tag = sys.argv[1:]
            store = ObjectStore(root)
            for i in range(10):
                store.put({'v': np.arange(i + 1.)}, key=store.key_for('shared', i))   # same keys from both
                store.put({'v': np.arange(i + 1.)}, key=store.key_for(tag, i))
        """)
        root = self.path('shared_store')
        procs = [subprocess.Popen([sys.executable, '-c', child, root, tag], env=_subprocess_env()) for tag in 'xy']
        for p in procs:
            self.assertEqual(p.wait(), 0)
        from McUtils.Scaffolding import ObjectStore
        store = ObjectStore(root)
        self.assertEqual(len(store.keys()), 30)
        self.assertEqual(store.get(store.key_for('shared', 9))['v'].tolist(), list(range(10)))
        self.assertEqual([n for n in os.listdir(root) if n.startswith('.stage')], [])

    def test_ReadoutStoreSharesEntryStore(self):
        from McUtils.Devutils import EntryStore
        from McUtils.Docs.Examples import ReadoutStore
        self.assertTrue(issubclass(ReadoutStore, EntryStore))
        store = ReadoutStore(self.path('readouts'))
        key = 'ab' * 32
        store.write(key, {'status': 'ok'}, files={'fragment.html': '<p/>'})
        self.assertTrue(os.path.isfile(os.path.join(store.root, 'ab', key, 'meta.json')))
        self.assertEqual(sorted(store.read_meta(key)), ['key', 'status', 'store_version', 'written'])
        with self.assertRaises(ValueError):
            store.entry_path('short')

    def test_ResourceManagerWritesAtomically(self):
        manager = ResourceManager(name='res', location=self.path('resources'), write_metadata=True)
        manager.json_resource, manager.binary_resource = True, False
        loc = manager.get_resource_path('a.json')
        manager.save_resource(loc, {'a': 1})
        self.assertEqual(manager.load_resource(loc), {'a': 1})
        class Unserializable:
            pass
        with self.assertRaises(TypeError):
            manager.save_resource(loc, {'a': Unserializable()})
        self.assertEqual(manager.load_resource(loc), {'a': 1})  # the failed write left the old content
        self.assertEqual(os.listdir(os.path.dirname(loc)), ['a.json'])
    #endregion

    #region 7e: ConformerLibrary object store backend
    def test_ConformerLibraryObjectStoreBackend(self):
        from McUtils.ExternalPrograms.ConformerLibrary import ConformerLibrary, ObjectStoreBackend
        rng = np.random.default_rng(3)
        tree = {
            '33': {'smi': 'CCO', 'coord': [rng.normal(size=(9, 3)) for _ in range(3)]},
            '68': {'smi': 'CC=O', 'coord': [rng.normal(size=(7, 3))]},
        }
        source = ConformerLibrary(tree)
        root = self.path('conformer_store')
        lib = source.to_object_store(root)
        self.assertEqual(len(lib), 2)
        self.assertIn('33', lib)
        self.assertNotIn('99', lib)
        self.assertEqual(sorted(lib.keys()), ['33', '68'])
        self.assertEqual(lib.get_smiles('68'), 'CC=O')
        record = lib['33']
        self.assertEqual(record['smi'], 'CCO')
        for a, b in zip(record['coord'], tree['33']['coord']):
            self.assertTrue(np.array_equal(a, b))
        # a fresh handle (another process) sees the same library; other namespaces are separate
        again = ConformerLibrary.from_object_store(root)
        self.assertEqual(sorted(again.keys()), ['33', '68'])
        self.assertEqual(len(ConformerLibrary.from_object_store(root, namespace='other')), 0)
        # adding a record is one atomic put, and identical records share an entry
        backend = ObjectStoreBackend(root)
        entry = backend.put_record('copy', lib['33'])
        self.assertEqual(entry, backend.store.resolve_alias('conformers.33'))
        with self.assertRaises(KeyError):
            backend.put_record('copy', tree['68'], replace=False)
        with self.assertRaises(KeyError):
            lib['99']
    #endregion


if __name__ == '__main__':
    unittest.main()

"""
Tests for the persistence framework in `McUtils.Scaffolding`
(`Checkpointing`, `Serializers`, `Persistence`) that pin down known gaps.

These are plain `unittest` tests (no Peeves) that only write inside temp directories.
Tests for gaps that haven't been fixed yet are marked `@unittest.expectedFailure` and carry the
phase of the persistence plan (`claude_drafts/persistence/PLAN.md`) that fixes them, e.g.
`# phase 1`. When a phase lands, its tests start passing ("unexpected success") and the marker
should be removed in that same patch.
"""

import os, sys, shutil, subprocess, tempfile, textwrap, time, unittest
import numpy as np

import McUtils
from McUtils.Scaffolding import (
    Checkpointer, JSONCheckpointer, NumPyCheckpointer, HDF5Checkpointer,
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


def _module_level_function(x):
    return x


class _Cyclic:
    def __init__(self):
        self.me = self


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
                with Checkpointer.from_file(fn) as chk:
                    chk['a'] = np.arange(3)
                    raise RuntimeError("fail mid-block")
            with Checkpointer.from_file(fn) as chk:
                self.assertEqual(chk['a'].tolist() if hasattr(chk['a'], 'tolist') else list(chk['a']), [0, 1, 2])

    def _run_child(self, fn, mode):
        """
        mode 'w': write key `a`; mode 'k': add key `b`, then die hard (no exit handlers) inside the block
        """
        child = textwrap.dedent("""
            import sys, os, numpy as np
            from McUtils.Scaffolding import Checkpointer
            fn, mode = sys.argv[1:]
            with Checkpointer.from_file(fn) as chk:
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
        with Checkpointer.from_file(fn) as chk:
            self.assertIn('a', list(chk.keys()))

    def test_NumPyCheckpointerCrashKeepsContents(self):
        self._check_crash_keeps_contents('.npz')

    def test_JSONCheckpointerCrashKeepsContents(self):
        self._check_crash_keeps_contents('.json')

    def _check_unchanged_block_leaves_file(self, ext):
        fn = self.path('same' + ext)
        with Checkpointer.from_file(fn) as chk:
            chk['a'] = np.arange(3)
        before = os.stat(fn).st_mtime_ns
        time.sleep(0.05)
        with Checkpointer.from_file(fn) as chk:
            chk['a']  # read only
        self.assertEqual(os.stat(fn).st_mtime_ns, before)

    def test_NumPyCheckpointerReadOnlyBlockDoesNotRewrite(self):
        self._check_unchanged_block_leaves_file('.npz')

    def test_JSONCheckpointerReadOnlyBlockDoesNotRewrite(self):
        self._check_unchanged_block_leaves_file('.json')

    def test_DumpCheckpointerFlushAndAutoflush(self):
        for ext in ['.npz', '.json']:
            fn = self.path('flush' + ext)
            chk = Checkpointer.from_file(fn)
            with chk:
                chk['a'] = np.arange(3)
                self.assertFalse(os.path.exists(fn))  # nothing is written until the block exits...
                chk.flush()                           # ...or until asked
                self.assertTrue(os.path.exists(fn))
                mtime = os.stat(fn).st_mtime_ns
                time.sleep(0.05)
                chk.flush()                           # nothing new, so nothing rewritten
                self.assertEqual(os.stat(fn).st_mtime_ns, mtime)
            auto = Checkpointer.from_file(self.path('auto' + ext), autoflush=True)
            with auto:
                auto['a'] = 1
                with Checkpointer.from_file(self.path('auto' + ext)) as other:  # visible to a second reader mid-block
                    self.assertEqual(int(other['a']), 1)
                del auto['a']
                with Checkpointer.from_file(self.path('auto' + ext)) as other:
                    self.assertNotIn('a', list(other.keys()))

    def test_DumpCheckpointerKeepsExistingKeysAndLeavesNoTempFiles(self):
        for ext in ['.npz', '.json']:
            fn = self.path('keys' + ext)
            for key in ['a', 'b']:
                with Checkpointer.from_file(fn) as chk:
                    chk[key] = np.arange(3)
            with Checkpointer.from_file(fn) as chk:
                self.assertEqual(sorted(chk.keys()), ['a', 'b'])
        self.assertEqual([f for f in os.listdir(self._tmp) if f.endswith('.tmp')], [])

    def test_DumpCheckpointerNestedBlocksWriteOnce(self):
        fn = self.path('nested.json')
        chk = Checkpointer.from_file(fn)
        with chk:
            with chk:
                chk['a'] = 1
            self.assertFalse(os.path.exists(fn))  # the inner exit doesn't write
        self.assertTrue(os.path.exists(fn))
        with Checkpointer.from_file(fn) as other:
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
        with Checkpointer.from_file(fn) as chk:
            chk['a'] = 1
        os.chmod(fn, 0o640)
        with Checkpointer.from_file(fn) as chk:
            chk['b'] = 2
        self.assertEqual(os.stat(fn).st_mode & 0o777, 0o640)

    def test_DumpCheckpointerFollowsSymlink(self):
        real = self.path('real.json')
        link = self.path('link.json')
        with Checkpointer.from_file(real) as chk:
            chk['a'] = 1
        os.symlink(real, link)
        with Checkpointer.from_file(link) as chk:
            chk['b'] = 2
        self.assertTrue(os.path.islink(link))
        with Checkpointer.from_file(real) as chk:
            self.assertEqual(sorted(chk.keys()), ['a', 'b'])

    def test_CheckpointerCachedEval(self):
        for ext in ['.json', '.npz', '.hdf5']:
            calls = []
            def gen():
                calls.append(1)
                return np.ones(3)
            fn = self.path('cached' + ext)
            for _ in range(2):
                with Checkpointer.from_file(fn) as chk:
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
        for ext in ['.json', '.npz', '.hdf5']:
            fn = self.path('shared' + ext)
            with Checkpointer.from_file(fn) as chk:
                chk['pair'] = [shared, {'again': shared}, _Versioned(1, shared)]
            with Checkpointer.from_file(fn) as chk:
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
        for ser in [JSONSerializer(), NumPySerializer(), HDF5Serializer(), PicklingSerializer()]:
            self.assertFalse(ser.pickler.allow_pickle if hasattr(ser, 'pickler') else ser.pseudopickler.allow_pickle
                             if hasattr(ser, 'pseudopickler') else ser.psuedopickler.allow_pickle, type(ser).__name__)
        # unsupported objects are refused rather than silently pickled
        for ext in ['.json', '.npz', '.hdf5']:
            with self.assertRaises(ValueError):
                with Checkpointer.from_file(self.path('nopickle' + ext)) as chk:
                    chk['f'] = _module_level_function
    #endregion

    #region Serializers (phase 4)
    def _roundtrip_all(self, value, check):
        for ext in ['.json', '.npz', '.hdf5']:
            fn = self.path('rt' + ext)
            if os.path.exists(fn):
                os.remove(fn)
            with Checkpointer.from_file(fn) as chk:
                chk['v'] = value
            with Checkpointer.from_file(fn) as chk:
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
    #endregion


if __name__ == '__main__':
    unittest.main()

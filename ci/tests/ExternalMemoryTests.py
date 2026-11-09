import unittest
import numpy as np
from McUtils.Numputils import external_unique

class EmptyStreamTests(unittest.TestCase):
    def test_empty_chunks_in_real_integer_stream(self):
        blocks=[np.empty(0),np.array([5,2,5]),[],np.array([2,7]),np.empty(0)]
        for sorting in [True,False]:
            values,first=external_unique(blocks,sort=sorting,return_index=True,chunk_size=2)
            np.testing.assert_array_equal(values,[2,5,7] if sorting else [5,2,7])
            np.testing.assert_array_equal(first,[1,0,4] if sorting else [0,1,4])

    def test_empty_default_dtype_rows_preserve_shape(self):
        blocks=[np.empty((0,2)),np.array([[4,3],[1,2],[4,3]]),np.empty((0,2))]
        values,first=external_unique(blocks,sort=False,return_index=True,chunk_size=1)
        np.testing.assert_array_equal(values,[[4,3],[1,2]])
        np.testing.assert_array_equal(first,[0,1])
        self.assertEqual(external_unique([np.empty((0,2))]).shape,(0,2))

    def test_all_empty_default_dtype(self):
        values,first=external_unique([[],np.empty(0)],sort=False,return_index=True)
        self.assertEqual(values.shape,(0,))
        self.assertEqual(values.dtype,np.dtype('int64'))
        self.assertEqual(first.size,0)

    def test_nonempty_noninteger_keys_still_rejected(self):
        with self.assertRaises(TypeError):
            external_unique([np.empty(0),np.array([1.0,2.0])])

class MappedArrayFlushBufferTests(unittest.TestCase):
    """Writeback contracts using actual HNO3 correction support, including bands."""
    @classmethod
    def setUpClass(cls):
        import json
        from pathlib import Path
        fixture=json.loads((Path(__file__).parent/'TestData/hno3_vpt2_rows.json').read_text())
        cls.blocks=[np.flatnonzero(row['values']).astype(np.int64) for row in fixture['rows']]
        cls.values=np.asarray(fixture['rows'][1]['values'],dtype=float)
        cls.pairs=[np.column_stack((np.full(len(b),i,dtype=np.int64),b)) for i,b in enumerate(cls.blocks)]

    def test_real_scalar_and_pair_streams_preserve_order_indices_and_final_flush(self):
        import tempfile
        from pathlib import Path
        from unittest.mock import patch
        from McUtils.Numputils import MappedArrayFlushBuffer
        for blocks in [self.blocks,self.pairs]:
            for sorting in [True,False]:
                for index in [True,False]:
                    with self.subTest(width=blocks[0].ndim,sorting=sorting,index=index),tempfile.TemporaryDirectory() as directory:
                        expected=external_unique(blocks,sort=sorting,return_index=index,chunk_size=127)
                        buffer=MappedArrayFlushBuffer(max_bytes=16*1024**2)
                        calls=[];original=np.memmap.flush
                        def flush(array):calls.append(str(array.filename));return original(array)
                        path=Path(directory)/'final.npy'
                        with patch.object(np.memmap,'flush',flush):
                            actual=external_unique(blocks,sort=sorting,return_index=index,chunk_size=127,
                                                   directory=directory,output_file=path,flush_buffer=buffer)
                        if index:
                            actual,first=actual
                            np.testing.assert_array_equal(first,expected[1]);expected=expected[0]
                        np.testing.assert_array_equal(actual,expected)
                        self.assertEqual(calls,[str(path)])
                        stats=buffer.snapshot()
                        self.assertGreater(stats['discarded_files'],0)
                        self.assertEqual(stats['pending_files'],0)
                        self.assertEqual(stats['flushed_files'],0)
                        self.assertEqual(set(Path(directory).iterdir()),{path})
                        actual._mmap.close();buffer.close()

    def test_default_still_flushes_intermediate_runs(self):
        from unittest.mock import patch
        calls=[];original=np.memmap.flush
        def flush(array):calls.append(str(array.filename));return original(array)
        with patch.object(np.memmap,'flush',flush):
            actual=external_unique(self.blocks,chunk_size=127)
        np.testing.assert_array_equal(actual,np.unique(np.concatenate(self.blocks)))
        self.assertGreater(len(calls),0)

    def test_limits_and_closed_mappings_do_not_retain_arrays(self):
        import gc,tempfile,weakref
        from pathlib import Path
        from McUtils.Numputils import MappedArrayFlushBuffer
        with tempfile.TemporaryDirectory() as directory:
            buffer=MappedArrayFlushBuffer(max_bytes=None,max_files=1)
            for i in range(2):
                path=Path(directory)/('row_{}.npy'.format(i))
                array=np.lib.format.open_memmap(path,mode='w+',dtype=float,shape=self.values.shape)
                array[:]=self.values
                buffer.defer(array);reference=weakref.ref(array)
                array._mmap.close();del array;gc.collect()
                self.assertIsNone(reference())
            self.assertEqual(buffer.snapshot()['flushed_files'],1)
            self.assertEqual(buffer.snapshot()['pending_files'],1)
            buffer.flush()
            self.assertEqual(buffer.snapshot()['flushed_files'],2)
            for path in Path(directory).iterdir():np.testing.assert_array_equal(np.load(path),self.values)
            array=np.lib.format.open_memmap(Path(directory)/'oversized.npy',mode='w+',dtype=float,shape=self.values.shape)
            tiny=MappedArrayFlushBuffer(max_bytes=1)
            tiny.defer(array);array._mmap.close()
            self.assertEqual(tiny.snapshot()['pending_bytes'],0)
            self.assertEqual(tiny.snapshot()['flushed_files'],1)
            tiny.close();buffer.close()

    def test_unique_error_retires_only_its_own_files(self):
        import tempfile
        from pathlib import Path
        from McUtils.Numputils import MappedArrayFlushBuffer
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'unrelated.npy'
            array=np.lib.format.open_memmap(path,mode='w+',dtype=float,shape=self.values.shape)
            array[:]=self.values
            buffer=MappedArrayFlushBuffer(max_bytes=None)
            buffer.defer(array);array._mmap.close()
            def bad_stream():
                yield from self.blocks
                raise RuntimeError('producer failed')
            with self.assertRaisesRegex(RuntimeError,'producer failed'):
                external_unique(bad_stream(),chunk_size=127,directory=directory,flush_buffer=buffer)
            self.assertEqual(buffer.snapshot()['pending_files'],1)
            self.assertEqual(set(Path(directory).iterdir()),{path})
            buffer.close()
            np.testing.assert_array_equal(np.load(path),self.values)

    def test_writeback_errors_propagate_and_file_replacement_is_detected(self):
        import importlib,tempfile
        from pathlib import Path
        from unittest.mock import patch
        from McUtils.Numputils import MappedArrayFlushBuffer
        module=importlib.import_module('McUtils.Numputils.ExternalMemory')
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'row.npy'
            array=np.lib.format.open_memmap(path,mode='w+',dtype=float,shape=self.values.shape)
            array[:]=self.values
            buffer=MappedArrayFlushBuffer();buffer.defer(array);array._mmap.close()
            with patch.object(module.os,'fdatasync',create=True,side_effect=OSError('writeback failed')):
                with self.assertRaisesRegex(OSError,'writeback failed'):buffer.flush()
            self.assertEqual(buffer.snapshot()['pending_files'],1)
            replacement=Path(directory)/'replacement.npy';np.save(replacement,self.values)
            replacement.replace(path)
            with self.assertRaisesRegex(RuntimeError,'replaced'):buffer.flush()
            buffer.discard(path);buffer.close()

    def test_configuration_serialization_and_copy_on_write_rejection(self):
        import pickle,tempfile
        from pathlib import Path
        from McUtils.Numputils import MappedArrayFlushBuffer
        for opts in [dict(max_bytes=0),dict(max_files=0),dict(max_files=None),dict(max_bytes=True)]:
            with self.assertRaises(ValueError):MappedArrayFlushBuffer(**opts)
        buffer=MappedArrayFlushBuffer(max_bytes=1024,max_files=3)
        restored=pickle.loads(pickle.dumps(buffer));self.assertEqual(restored.snapshot(),buffer.snapshot())
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'row.npy';np.save(path,self.values)
            array=np.load(path,mmap_mode='c')
            with self.assertRaises(TypeError):buffer.defer(array)
            array._mmap.close();array=np.load(path,mmap_mode='r+')
            buffer.defer(array)
            if buffer.snapshot()['pending_files']:
                with self.assertRaises(TypeError):pickle.dumps(buffer)
            buffer.discard(path);buffer.close()
            with self.assertRaisesRegex(RuntimeError,'closed'):buffer.defer(array)
            array._mmap.close()

if __name__=='__main__':unittest.main()

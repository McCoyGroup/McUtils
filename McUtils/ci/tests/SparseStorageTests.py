"""Row backend regression tests using actual molecular VPT correction rows."""
import json
import unittest
from pathlib import Path
import numpy as np
import scipy.sparse as sp
from McUtils.Numputils import CompactSparseRow, PackedIndexArray, RowSparseArray, SparseArray

class RowSparseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data=Path(__file__).parent/"TestData"/"hno3_vpt2_rows.json"
        fixture=json.loads(data.read_text())
        cls.provenance=fixture["provenance"]
        cls.values=np.asarray([r["values"] for r in fixture["rows"]],dtype=float)
        cls.rows=[CompactSparseRow.from_dense(v,None,4096) for v in cls.values]
        cls.matrix=RowSparseArray(cls.rows,cls.values.shape[1],block_size=4096)

    def test_real_ground_fundamental_overtone_combination_rows(self):
        self.assertEqual(self.provenance["molecule"],"HNO3")
        self.assertTrue(any(row.dense for row in self.rows))
        self.assertTrue(any(not row.dense for row in self.rows))
        np.testing.assert_array_equal(self.matrix.asarray(),self.values)
        for row,values in zip(self.rows,self.values):
            expected=np.flatnonzero(values)
            np.testing.assert_array_equal(np.asarray(row.columns),expected)
            self.assertEqual(row.nnz,len(expected))
            if isinstance(row.columns,PackedIndexArray):
                queries=np.r_[-1,0,expected[:5],expected[-5:],len(values)-1,len(values)]
                np.testing.assert_array_equal(row.columns.searchsorted(queries),np.searchsorted(expected,queries))
                np.testing.assert_array_equal(row.columns.searchsorted(queries,side="right"),np.searchsorted(expected,queries,side="right"))
                np.testing.assert_array_equal(row.columns[[2,0,2]],expected[[2,0,2]])

    def test_real_row_products_and_views(self):
        selected=[3,0,3,4,5]
        a=self.matrix[selected,:]
        dense=self.values[selected,:]
        np.testing.assert_array_equal(a.asarray(),dense)
        np.testing.assert_array_equal(a.T.asarray(),dense.T)
        np.testing.assert_array_equal(a[:,[3,0,3]].asarray(),dense[:,[3,0,3]])
        reference=SparseArray.from_data(sp.csr_matrix(dense))
        expected=reference.dot(reference.T).asarray()
        np.testing.assert_allclose(a.dot(a.T).asarray(),expected,rtol=2e-13,atol=2e-14)
        np.testing.assert_allclose(reference.dot(a.T).asarray(),expected,rtol=2e-13,atol=2e-14)
        np.testing.assert_array_equal(RowSparseArray.from_state(a.to_state()).asarray(),dense)

    def test_real_nonzero_filter_and_export_guard(self):
        blocks=list(self.matrix.iter_nonzero_blocks(block_size=127,value_filter=lambda v:np.abs(v)>.1))
        actual_rows=np.concatenate([indices[0] for values,indices in blocks])
        actual_cols=np.concatenate([indices[1] for values,indices in blocks])
        rows,cols=np.nonzero(np.abs(self.values)>.1)
        np.testing.assert_array_equal(actual_rows,rows)
        np.testing.assert_array_equal(actual_cols,cols)
        guarded=RowSparseArray(self.rows,self.values.shape[1],block_bytes=1)
        with self.assertRaises(MemoryError):guarded.ascsr()


"""Disk-backing API checks using actual HNO3 correction rows."""
import gc
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from McUtils.Numputils import RowSparseArray, RowSpillStore, CompactSparseRow

class RowSpillTests(unittest.TestCase):
    def test_actual_rows_and_borrowed_views(self):
        fixture=Path(__file__).parent/'TestData'/'hno3_vpt2_rows.json'
        data=json.loads(fixture.read_text())
        values=np.asarray([r['values'] for r in data['rows']])
        native=RowSparseArray([CompactSparseRow.from_dense(v,None,4096) for v in values],values.shape[1])
        with tempfile.TemporaryDirectory() as directory:
            store=RowSpillStore(directory,0,64*1024**2,segment_bytes=1024**2)
            mapped=RowSparseArray([CompactSparseRow.from_dense(v,None,4096) for v in values],values.shape[1],storage=store)
            self.assertGreater(store.snapshot()['file_backed_payload_bytes'],0)
            np.testing.assert_array_equal(mapped.asarray(),values)
            np.testing.assert_array_equal(mapped.dot(mapped.T).asarray(),native.dot(native.T).asarray())
            selected=mapped[[3,0,3],:]
            np.testing.assert_array_equal(selected.asarray(),values[[3,0,3]])
            np.testing.assert_array_equal((mapped+mapped).asarray(),values+values)
            np.testing.assert_array_equal((-mapped).asarray(),-values)
            np.testing.assert_array_equal(RowSparseArray.from_state(mapped.to_state()).asarray(),values)
            borrowed=mapped.rows[3].columns
            expected=np.asarray(borrowed).copy()
            del selected,mapped,store
            gc.collect()
            np.testing.assert_array_equal(np.asarray(borrowed),expected)
            del borrowed
            gc.collect()
            self.assertFalse(list(Path(directory).rglob('*.bin')))

    def test_disk_quota_keeps_exact_resident_rows(self):
        fixture=Path(__file__).parent/'TestData'/'hno3_vpt2_rows.json'
        values=np.asarray(json.loads(fixture.read_text())['rows'][1]['values'])
        with tempfile.TemporaryDirectory() as directory:
            store=RowSpillStore(directory,0,1,segment_bytes=1024**2)
            row=store.retain(CompactSparseRow.from_dense(values,None,4096))
            matrix=RowSparseArray([row],len(values),storage=store)
            np.testing.assert_array_equal(matrix.asarray()[0],values)
            self.assertEqual(store.file_backed_bytes,0)
            self.assertGreater(store.budget_refusals,0)



class SparseIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data=Path(__file__).parent/'TestData'/'hno3_vpt2_rows.json'
        cls.values=np.asarray([r['values'] for r in json.loads(data.read_text())['rows']],dtype=float)

    def test_sparse_module_owns_rows_and_file_backing(self):
        import McUtils.Numputils.Sparse as sparse
        from McUtils.Numputils import ScipySparseArray
        for kind in [RowSparseArray,CompactSparseRow,PackedIndexArray,RowSpillStore]:
            self.assertEqual(kind.__module__,sparse.__name__)
            self.assertIs(getattr(sparse,kind.__name__),kind)
        for name in ['RowSparse.py','RowSpill.py']:
            self.assertFalse((Path(sparse.__file__).parent/name).exists())
        for kind in [ScipySparseArray,RowSparseArray]:
            for name in ['T','__matmul__','__add__','__iadd__','__radd__','__neg__']:
                self.assertIs(getattr(kind,name),getattr(SparseArray,name))

    def test_native_product_is_evaluated_once(self):
        from unittest import mock
        from McUtils.Numputils import ScipySparseArray
        a=SparseArray.from_data(sp.csr_matrix(self.values))
        b=SparseArray.from_data(sp.csr_matrix(self.values.T))
        expected=a.data.dot(b.data)
        with mock.patch.object(a.data,'dot',wraps=a.data.dot) as product:
            result=a.dot(b)
            self.assertEqual(product.call_count,1)
        np.testing.assert_array_equal(result.asarray(),expected.toarray())
        # The row backend uses the same native multiplication/error routine.
        rows=RowSparseArray.from_native(a,block_bytes=1024**2,block_size=4096)
        with mock.patch.object(ScipySparseArray,'_matrix_dot',wraps=ScipySparseArray._matrix_dot) as product:
            actual=rows.dot(rows.T)
            self.assertGreater(product.call_count,0)
        np.testing.assert_array_equal(actual.asarray(),expected.toarray())

    def test_common_operators_and_dtype_on_real_rows(self):
        from McUtils.Numputils import ScipySparseArray
        for matrix in [ScipySparseArray(sp.csr_matrix(self.values)),RowSparseArray.from_native(self.values)]:
            np.testing.assert_array_equal((+matrix).asarray(),self.values)
            np.testing.assert_array_equal((-matrix).asarray(),-self.values)
            np.testing.assert_array_equal((matrix+matrix).asarray(),self.values+self.values)
            np.testing.assert_array_equal((0+matrix).asarray(),self.values)
            np.testing.assert_array_equal((matrix@matrix.T).asarray(),sp.csr_matrix(self.values).dot(sp.csr_matrix(self.values.T)).toarray())
        # Range checks allocate no enormous arrays.
        self.assertEqual(SparseArray._index_dtype(19757815),np.dtype(np.int32))
        self.assertEqual(SparseArray._index_dtype(np.iinfo(np.int32).max+1),np.dtype(np.int64))

    def test_pinned_file_backing_and_borrowed_support(self):
        values=self.values[1]
        with tempfile.TemporaryDirectory() as directory:
            store=RowSpillStore(directory,0,64*1024**2,segment_bytes=1024**2)
            row=store.retain(CompactSparseRow.from_dense(values,None,4096))
            self.assertGreater(store.file_backed_bytes,0)
            prior=store.drop_calls
            with store.pin_rows([row]):
                store._drop(row._spill_segment)
                self.assertEqual(store.drop_calls,prior)
                matrix=RowSparseArray([row],len(values),storage=store)
                np.testing.assert_array_equal(matrix.asarray()[0],values)
            self.assertGreaterEqual(store.drop_calls,prior)
            # Either the platform supports dropping, or the original counters
            # record its failure; this never bypasses the existing RSS guard.
            self.assertGreater(store.drop_calls+store.drop_failures,0)
            support=row.columns;expected=np.asarray(support).copy()
            del matrix,row,store
            gc.collect()
            np.testing.assert_array_equal(np.asarray(support),expected)
            del support
            gc.collect()
            self.assertFalse(list(Path(directory).rglob('*.bin')))


if __name__=='__main__':unittest.main()

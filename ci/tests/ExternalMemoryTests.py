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

if __name__=='__main__':unittest.main()

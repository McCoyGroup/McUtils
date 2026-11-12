"""Exact pivot selection must scan all columns of rectangular matrices."""
from McUtils.Numputils import rational_matrix_pivots, rational_matrix_inverse


def test_wide_matrix_late_independent_columns():
    assert rational_matrix_pivots([[0,0,1,0],[0,0,0,1]]) == [2,3]
    assert rational_matrix_pivots([]) == []
    assert rational_matrix_pivots([[1],[0]]) == [0]
    assert rational_matrix_inverse([[1,2],[3,5]]) == ((-5,2),(3,-1))

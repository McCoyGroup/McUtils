"""Independent checks of the tensor-derivative and permutation infrastructure."""
import itertools
import math
import unittest
import numpy as np
from scipy.linalg import solve_sylvester
from McUtils import Numputils as nput
from McUtils.Numputils.TensorDerivatives import (
    get_nca_perm_iter, nca_partition_terms, nca_partition_prod, kron_prod_derivs, kron_sum_derivs, sylv_derivs, scalarfunc_deriv)
from McUtils.Combinatorics import IntegerPartitioner
from TensorDerivativeRegressionTests import expansion, multiply, random_poly, power, indices


def inverse_stack(expansion, order, base_expansion=None):
    """Independent inverse recurrence from differentiating -B A' B."""
    shared = expansion[0].ndim-2
    inverse = ([np.linalg.inv(expansion[0])] if base_expansion is None
               else list(base_expansion))
    derivative = expansion[1:] or [0]
    for o in range(len(inverse), order+1):
        term = nput.tensorops_deriv(
            inverse, [-1, shared+1], derivative, [-1, shared], inverse,
            order=[o-1], shared=shared)[0]
        inverse.append(0 if nput.is_zero(term) else -np.moveaxis(term, -2, shared))
    return inverse


def canonical_blocks(perms, partition):
    keys = []
    for perm in perms:
        slots = np.argsort(perm)
        blocks = []
        offset = 0
        for size in partition:
            blocks.append((int(size), tuple(sorted(slots[offset:offset+size]))))
            offset += size
        keys.append(tuple(sorted(blocks)))
    return keys


def block_assignments(partition):
    # Precompute possible slots, then extend explicit assignment lists.
    slots = {s:list(itertools.combinations(range(sum(partition)), s)) for s in set(partition)}
    states = [((), frozenset())]
    for size in partition:
        next_states = []
        for blocks, used in states:
            for group in slots[size]:
                if used.isdisjoint(group):
                    next_states.append((blocks+((size, group),), used.union(group)))
        states = next_states
    return {tuple(sorted(blocks)) for blocks, _ in states}


class DerivativeInfrastructureTests(unittest.TestCase):
    def setUp(self):
        self.rng = np.random.default_rng(818)

    def assertExpansion(self, actual, expected, atol=5e-10):
        self.assertEqual(len(actual), len(expected))
        for a,b in zip(actual,expected):
            np.testing.assert_allclose(a,b,atol=atol,rtol=2e-11)

    def test_partition_permutations_exhaustive(self):
        for order in range(1,9):
            for group in IntegerPartitioner.partitions(order):
                for partition in group:
                    expected = block_assignments(tuple(partition))
                    for variant in set(itertools.permutations(partition)):
                        with self.subTest(partition=variant):
                            permutations = np.concatenate(list(get_nca_perm_iter(variant)))
                            keys = canonical_blocks(permutations, variant)
                            self.assertEqual(len(keys), int(nca_partition_terms(variant)))
                            self.assertEqual(len(keys),len(set(keys)))
                            self.assertEqual(set(keys),expected)

    def test_inverse_stack_and_recurrence(self):
        for order in (1,2,4,6):
            for matrix_size in (2,3):
                a = random_poly(self.rng,(matrix_size,matrix_size),order)
                a[(0,0)] += 2*np.eye(matrix_size)
                ae = expansion(a,order)
                polynomial = {(0,0):np.linalg.inv(a[(0,0)])}
                for alpha in sorted(indices(2,order),key=sum)[1:]:
                    total = sum(value@polynomial[tuple(u-v for u,v in zip(alpha,beta))]
                        for beta,value in a.items()
                        if sum(beta)>0 and all(v<=u for u,v in zip(alpha,beta)))
                    polynomial[alpha] = -polynomial[(0,0)]@total
                expected = expansion(polynomial,order)
                for operation in (nput.matinv_deriv,inverse_stack):
                    self.assertExpansion(operation(ae,order),expected)
                    self.assertExpansion(operation(ae,order,base_expansion=expected[:2]),expected)
                    for batch_shape in ((2,),(2,2)):
                        # Independent nonsymmetric matrices per batch.
                        samples = [expansion(random_poly(self.rng,(matrix_size,matrix_size),order),order)
                                   for _ in range(math.prod(batch_shape))]
                        for sample in samples:
                            sample[0] += 3*np.eye(matrix_size)
                        ab = [np.stack([s[o] for s in samples]).reshape(batch_shape+ae[o].shape)
                              for o in range(order+1)]
                        reference = [operation(s,order) for s in samples]
                        expected_batch = [np.stack([s[o] for s in reference]).reshape(batch_shape+ae[o].shape)
                                          for o in range(order+1)]
                        self.assertExpansion(operation(ab,order),expected_batch)

    def test_partition_products_against_full_symmetrization(self):
        derivatives = []
        for order in range(1,7):
            raw = self.rng.normal(size=(2,)*order)
            symmetric = sum(raw.transpose(p) for p in itertools.permutations(range(order)))/math.factorial(order)
            derivatives.append(symmetric)
        for order in range(1,7):
            for group in IntegerPartitioner.partitions(order):
                for partition in group:
                    product = np.ones(())
                    for size in partition:
                        product = np.tensordot(product,derivatives[size-1],axes=0)
                    expected = sum(product.transpose(p) for p in itertools.permutations(range(order)))
                    expected *= nca_partition_terms(partition)/math.factorial(order)
                    np.testing.assert_allclose(nca_partition_prod(partition,derivatives),expected,atol=5e-12)

    def test_inverse_differentiated_identity(self):
        for order in (2,4,6):
            ae = expansion(random_poly(self.rng,(3,3),order),order)
            ae[0] += 2*np.eye(3)
            for inverse in (nput.matinv_deriv(ae,order),inverse_stack(ae,order)):
                identity = nput.tensordot_deriv(ae,inverse,order)
                np.testing.assert_allclose(identity[0],np.eye(3),atol=1e-12)
                for derivative in identity[1:]:
                    np.testing.assert_allclose(derivative,0,atol=5e-10)
        base = np.array([[2.,.3],[-.2,1.4]])
        for terms in ([base], [base,0,0,0,0],
                      [base,np.ones((2,2,2))*.02],
                      [base,0,np.ones((2,2,2,2))*.02]):
            self.assertExpansion(inverse_stack(terms,4),nput.matinv_deriv(terms,4))

    def test_kronecker_products_and_sums(self):
        for order in (2,4):
            a = random_poly(self.rng,(2,2),order)
            b = random_poly(self.rng,(3,3),order)
            ae,be = expansion(a,order),expansion(b,order)
            expected = expansion(multiply(a,b,np.kron,order),order)
            self.assertExpansion(kron_prod_derivs(ae,be,order),expected)
            summed = {key:np.kron(a[key],np.eye(3))+np.kron(np.eye(2),b[key]) for key in a}
            self.assertExpansion(kron_sum_derivs(ae,be,order),expansion(summed,order))

    def test_sylvester_solution(self):
        for order in (1,2,4):
            a,b,c = [random_poly(self.rng,shape,order) for shape in ((2,2),(3,3),(2,3))]
            a[(0,0)] += np.diag([2.,3.])
            b[(0,0)] += np.diag([1.,2.,4.])
            answer = {}
            for alpha in sorted(indices(2,order),key=sum):
                rhs = c[alpha].copy()
                for beta in a:
                    if sum(beta)>0 and all(v<=u for u,v in zip(alpha,beta)):
                        rest = answer[tuple(u-v for u,v in zip(alpha,beta))]
                        rhs -= a[beta]@rest + rest@b[beta]
                answer[alpha] = solve_sylvester(a[(0,0)],b[(0,0)],rhs)
            actual,_ = sylv_derivs(expansion(a,order),expansion(b,order),expansion(c,order),order)
            self.assertExpansion(actual,expansion(answer,order))
            requested = [0,order]
            actual,_ = sylv_derivs(expansion(a,order),expansion(b,order),expansion(c,order),requested)
            self.assertExpansion(actual,[expansion(answer,order)[o] for o in requested])
            if order == 4:
                ae,be,ce = [expansion(p,order) for p in (a,b,c)]
                _,cached = sylv_derivs(ae,be,ce,2)
                extended,_ = sylv_derivs(ae,be,ce,4,ks_expansion=cached[0],inv_expansion=cached[1])
                self.assertExpansion(extended,expansion(answer,order))

    def test_matrix_square_root(self):
        order = 4
        b = random_poly(self.rng,(3,3),order)
        b = {key:(value+value.T)/2 for key,value in b.items()}
        b[(0,0)] += np.diag([2.,3.,4.])
        a = multiply(b,b,lambda x,y:x@y,order)
        self.assertExpansion(nput.matsqrt_deriv(expansion(a,order),order),expansion(b,order))
        ae,expected = expansion(a,order),expansion(b,order)
        for shape in ((2,),(2,2)):
            self.assertExpansion(nput.matsqrt_deriv([np.broadcast_to(t,shape+t.shape) for t in ae],order),
                                 [np.broadcast_to(t,shape+t.shape) for t in expected])

    def test_constant_matrix_operations(self):
        matrix = np.diag([2.,3.])
        self.assertExpansion(nput.matsqrt_deriv([matrix],4),[np.sqrt(matrix),0,0,0,0])
        self.assertExpansion(nput.matdet_deriv([matrix],4),[np.linalg.det(matrix),0,0,0,0])

    def test_fractional_power_batched_hermitian(self):
        matrix = np.array([[2., .2j],[-.2j,3.]])
        for shape in ((),(2,),(2,2)):
            a = np.broadcast_to(matrix,shape+matrix.shape)
            root = nput.frac_powh(a,.5)
            np.testing.assert_allclose(root@root,a,atol=2e-13)
            np.testing.assert_allclose(root,root.swapaxes(-1,-2).conj(),atol=2e-13)

    def test_scalar_function_chain_rule(self):
        order = 4
        a = random_poly(self.rng,(),order)
        a[(0,0)] += 1.
        cubed = multiply(multiply(a,a,lambda x,y:x*y,order),a,lambda x,y:x*y,order)
        def cube_derivative(x,o):
            return 0 if o>3 else math.factorial(3)/math.factorial(3-o)*x**(3-o)
        self.assertExpansion(scalarfunc_deriv(cube_derivative,expansion(a,order),order),
                             expansion(cubed,order))
        ae,expected = expansion(a,order),expansion(cubed,order)
        for shape in ((2,),(2,2)):
            scale = np.arange(math.prod(shape)).reshape(shape)+1
            batch = [scale.reshape(shape+(1,)*t.ndim)*t for t in ae]
            reference = [scale.reshape(shape+(1,)*t.ndim)**3*t for t in expected]
            self.assertExpansion(scalarfunc_deriv(cube_derivative,batch,order),reference)

    def test_inverse_coordinate_transformation(self):
        order = 6
        a = random_poly(self.rng,(2,),order)
        a[(0,0)] = np.zeros(2)
        forward = expansion(a,order)[1:]
        forward[0] += np.array([[1.,.2],[-.3,1.2]])
        inverse = nput.inverse_transformation(forward,order)
        composition = nput.tensor_reexpand(inverse,forward,order)
        np.testing.assert_allclose(composition[0],np.eye(2),atol=1e-12)
        for derivative in composition[1:]:
            np.testing.assert_allclose(derivative,0,atol=1e-9)
        extended = nput.inverse_transformation(forward,order,reverse_expansion=inverse[:3])
        self.assertExpansion(extended,inverse)

    def test_matrix_determinant(self):
        order = 4
        a = random_poly(self.rng,(3,3),order)
        a[(0,0)] += 2*np.eye(3)
        determinant = {}
        for perm in itertools.permutations(range(3)):
            inversions = sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
            term = {(0,0):np.ones(())}
            for i,j in enumerate(perm):
                term = multiply(term,{key:value[i,j] for key,value in a.items()},lambda x,y:x*y,order)
            for key,value in term.items():
                determinant[key] = determinant.get(key,0)+(-1)**inversions*value
        self.assertExpansion(nput.matdet_deriv(expansion(a,order),order),expansion(determinant,order))

    def test_vector_cross_and_cosine(self):
        order = 4
        a,b = [random_poly(self.rng,(3,),order) for _ in range(2)]
        a[(0,0)] += np.array([1.,2.,-.5])
        b[(0,0)] += np.array([-.4,1.,2.])
        self.assertExpansion(nput.vec_cross_deriv(expansion(a,order),expansion(b,order),order),
                             expansion(multiply(a,b,np.cross,order),order))
        ab = multiply(a,b,np.dot,order)
        for vector in (a,b):
            squared = multiply(vector,vector,np.dot,order)
            ab = multiply(ab,power(squared,-.5,order),lambda x,y:x*y,order)
        self.assertExpansion(nput.vec_anglecos_deriv(expansion(a,order),expansion(b,order),order),
                             expansion(ab,order))

    def test_batched_dihedral_including_planar_geometry(self):
        general = np.array([[1.,0.,0.],[1.,-1.,0.],[-1.,1.,.4],[-1.,0.,.8]])
        planar = general.copy()
        planar[:,2] = 0
        geometries = np.stack([general,planar,general+.1,planar+.2]).reshape(2,2,4,3)
        actual = nput.dihed_deriv(geometries,0,1,2,3,order=2)
        singles = [nput.dihed_deriv(g,0,1,2,3,order=2) for g in geometries.reshape(-1,4,3)]
        expected = [np.stack([s[o] for s in singles]).reshape((2,2)+np.shape(singles[0][o])) for o in range(3)]
        self.assertExpansion(actual,expected)


if __name__ == '__main__':
    unittest.main()

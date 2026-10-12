"""All exported derivative operations, checked against independent identities."""
import itertools
import math
import unittest
import numpy as np
from scipy.linalg import solve_sylvester
from McUtils import Numputils as nput
from McUtils.Numputils import TensorDerivatives as td
from TensorDerivativeRegressionTests import expansion, random_poly, multiply, power, indices


def add(a,b):
    return {key:a.get(key,0)+b.get(key,0) for key in a.keys()|b.keys()}


def log_poly(a,order):
    zero = (0,)*len(next(iter(a)))
    base = a[zero]
    delta = {key:value/base for key,value in a.items() if key != zero}
    result = {zero:np.log(base)}
    term = {zero:np.ones_like(base)}
    for k in range(1,order+1):
        term = multiply(term,delta,lambda x,y:x*y,order)
        result = add(result,{key:(-1)**(k+1)*value/k for key,value in term.items()})
    return result


def angle_poly(a,b,order):
    cosine = multiply(a,b,np.dot,order)
    cross = multiply(a,b,np.cross,order)
    sine = power(multiply(cross,cross,np.dot,order),.5,order)
    return {key:value.imag for key,value in log_poly(add(cosine,
        {key:1j*value for key,value in sine.items()}),order).items()}


def polynomial(exp,has_value=True):
    base = exp[0]
    n = exp[1].shape[0] if has_value else base.shape[0]
    answer = {}
    for o,term in enumerate(exp,start=0 if has_value else 1):
        if np.isscalar(term) and term == 0:
            continue
        for slots in itertools.product(range(n),repeat=o):
            key = tuple(slots.count(i) for i in range(n))
            answer[key] = term[slots]/math.prod(math.factorial(i) for i in key)
    if not has_value:
        answer[(0,)*n] = np.zeros(base.shape[-1])
    return answer


def compose(inner,outer,order):
    zero = (0,)*len(next(iter(inner)))
    result = {}
    for powers,value in outer.items():
        term = {zero:np.ones(())}
        for i,p in enumerate(powers):
            component = {key:v[i] for key,v in inner.items()}
            for _ in range(p):
                term = multiply(term,component,lambda x,y:x*y,order)
        result = add(result,{key:v*value for key,v in term.items()})
    return result


class TensorDerivativeOperationTests(unittest.TestCase):
    covered = {
        'nca_op_deriv':'test_binary_operations', 'tensordot_deriv':'test_binary_operations',
        'tensorprod_deriv':'test_binary_operations', 'scalarprod_deriv':'test_scalar_products',
        'inverse_transformation':'test_coordinate_inverse',
        'optimizing_transformation':'test_optimizing_transformation',
        'matinv_deriv':'test_matrix_inverse', 'matdet_deriv':'test_matrix_determinant',
        'matsqrt_deriv':'test_matrix_square_root', 'mateigh_deriv':'test_eigendecomposition',
        'scalarinv_deriv':'test_scalar_functions', 'scalarpow_deriv':'test_scalar_functions',
        'tensor_reexpand':'test_coordinate_inverse', 'tensorops_deriv':'test_operation_stack',
        'vec_norm_unit_deriv':'test_vector_norm', 'vec_angle_deriv':'test_vector_geometry',
        'vec_cross_deriv':'test_vector_geometry', 'vec_anglecos_deriv':'test_vector_geometry',
        'vec_anglesin_deriv':'test_vector_geometry', 'vec_normal_deriv':'test_vector_geometry',
        'vec_dihed_deriv':'test_dihedral', 'vec_plane_angle_deriv':'test_plane_angle',
        'shift_expansion':'test_expansion_arithmetic', 'scale_expansion':'test_expansion_arithmetic',
        'add_expansions':'test_expansion_arithmetic', 'subtract_expansions':'test_expansion_arithmetic',
        'concatenate_expansions':'test_concatenation',
        'renormalize_transformation':'test_renormalization',
        'orthogonalize_transformations':'test_orthogonalization'
    }

    def setUp(self):
        self.rng = np.random.default_rng(23091)

    def assertExpansion(self,a,b,atol=3e-11):
        self.assertEqual(len(a),len(b))
        for o,(x,y) in enumerate(zip(a,b)):
            with self.subTest(order=o):
                np.testing.assert_allclose(x,y,atol=atol,rtol=2e-10)

    def test_exported_operation_coverage(self):
        self.assertEqual(set(td.__all__),set(self.covered))
        for name,test in self.covered.items():
            self.assertTrue(callable(getattr(td,name)))
            self.assertTrue(callable(getattr(self,test)))

    def test_binary_operations(self):
        a,b = random_poly(self.rng,(2,3),4),random_poly(self.rng,(3,4),4)
        ae,be = expansion(a,4),expansion(b,4)
        expected = expansion(multiply(a,b,lambda x,y:x@y,4),4)
        self.assertExpansion(nput.tensordot_deriv(ae,be,4),expected)
        self.assertExpansion(nput.tensordot_deriv(ae,be,[4,0,2]),[expected[o] for o in (4,0,2)])
        def dot(x,y,axes,shared=None):
            return np.tensordot(x,y,axes=axes)
        self.assertExpansion(td.nca_op_deriv(dot,ae,be,4,[-1,0],True),expected[1:])
        expected = expansion(multiply(a,b,lambda x,y:np.tensordot(x,y,axes=0),4),4)
        self.assertExpansion(nput.tensorprod_deriv(ae,be,4,axes='all'),expected)
        for operation in (nput.tensordot_deriv,nput.tensorprod_deriv):
            self.assertExpansion(operation([],be,[4,0,2]),[0,0,0])

    def test_scalar_products(self):
        a,b = random_poly(self.rng,(),4),random_poly(self.rng,(2,3),4)
        ae,be = expansion(a,4),expansion(b,4)
        expected = expansion(multiply(a,b,lambda x,y:x*y,4),4)
        self.assertExpansion(nput.scalarprod_deriv(ae,be,4),expected)
        self.assertExpansion(nput.scalarprod_deriv([],be,4),[0]*5)

    def test_operation_stack(self):
        a,b,c = [random_poly(self.rng,s,4) for s in ((2,3),(3,4),(4,2))]
        expected = expansion(multiply(multiply(a,b,lambda x,y:x@y,4),c,lambda x,y:x@y,4),4)
        self.assertExpansion(nput.tensorops_deriv(expansion(a,4),[-1,0],expansion(b,4),
                             [-1,0],expansion(c,4),order=[4,0,2]),[expected[o] for o in (4,0,2)])

    def test_scalar_functions(self):
        a = random_poly(self.rng,(),4)
        a[(0,0)] += 2
        for p in (-1,.5,-.5,2,3):
            expected = expansion(power(a,p,4),4)
            self.assertExpansion(nput.scalarpow_deriv(expansion(a,4),p,[4,0,2]),
                                 [expected[o] for o in (4,0,2)])
        self.assertExpansion(nput.scalarinv_deriv(expansion(a,4),[4,0,2]),
            [expansion(power(a,-1,4),4)[o] for o in (4,0,2)])

    def test_expansion_arithmetic(self):
        a,b = [expansion(random_poly(self.rng,(2,),4),4) for _ in range(2)]
        self.assertExpansion(nput.shift_expansion(a,2),[a[0]+2]+a[1:])
        for factor in (0,-1,3):
            self.assertExpansion(nput.scale_expansion(a,factor),[t*factor for t in a])
        self.assertExpansion(nput.add_expansions(a,b,order=2),[x+y for x,y in zip(a[:3],b[:3])])
        self.assertExpansion(nput.subtract_expansions(a,b,order=2),[x-y for x,y in zip(a[:3],b[:3])])
        self.assertExpansion(nput.add_expansions(a[:1],b,order=4),[a[0]+b[0]]+b[1:])
        self.assertExpansion(nput.subtract_expansions(a[:1],b,order=4),[a[0]-b[0]]+[-t for t in b[1:]])

    def test_matrix_inverse(self):
        a = random_poly(self.rng,(2,2),4)
        a[(0,0)] += 3*np.eye(2)
        ae = expansion(a,4)
        inverse = nput.matinv_deriv(ae,4)
        self.assertExpansion(nput.tensordot_deriv(ae,inverse,4),[np.eye(2)]+[0]*4)
        self.assertExpansion(nput.matinv_deriv(ae,2,base_expansion=inverse),inverse[:3])

    def test_matrix_determinant(self):
        a = random_poly(self.rng,(2,2),4)
        determinant = add(multiply({k:v[0,0] for k,v in a.items()},
                                  {k:v[1,1] for k,v in a.items()},lambda x,y:x*y,4),
                          {k:-v for k,v in multiply({k:v[0,1] for k,v in a.items()},
                                  {k:v[1,0] for k,v in a.items()},lambda x,y:x*y,4).items()})
        self.assertExpansion(nput.matdet_deriv(expansion(a,4),4),expansion(determinant,4))

    def test_matrix_square_root(self):
        b = random_poly(self.rng,(2,2),4)
        b = {k:(v+v.T)/2 for k,v in b.items()}
        b[(0,0)] += 3*np.eye(2)
        a = multiply(b,b,lambda x,y:x@y,4)
        self.assertExpansion(nput.matsqrt_deriv(expansion(a,4),4),expansion(b,4))

    def test_eigendecomposition(self):
        for complex_ in (False,True):
            with self.subTest(complex=complex_):
                rotation = {(0,0):np.zeros((3,3),dtype=complex if complex_ else float),
                    (1,0):np.array([[0.,.2,0.],[-.2,0.,.1],[0.,-.1,0.]]),
                    (0,1):np.array([[0.,0.,.15],[0.,0.,0.],[-.15,0.,0.]])}
                if complex_:
                    # A complex two-dimensional rotation has real diagonal
                    # overlaps with the base vectors, fixing their phase gauge.
                    rotation[(1,0)] = np.array([[0.,.2,0.],[-.2,0.,0.],[0.,0.,0.]],dtype=complex)
                    rotation[(0,1)] = np.array([[0.,.15j,0.],[.15j,0.,0.],[0.,0.,0.]])
                q = {(0,0):np.eye(3,dtype=complex if complex_ else float)}
                term = q.copy()
                for o in range(1,5):
                    term = multiply(term,rotation,lambda x,y:x@y,4)
                    q = add(q,{k:v/math.factorial(o) for k,v in term.items()})
                values = {(0,0):np.diag([1.,3.,5.]),(1,0):np.diag([.1,.2,-.1]),
                          (0,1):np.diag([-.1,.05,.15]),(1,1):np.diag([.02,-.03,.01])}
                a = multiply(multiply(q,values,lambda x,y:x@y,4),
                    {k:v.T.conj() for k,v in q.items()},lambda x,y:x@y,4)
                ae,ve,qe = expansion(a,4),expansion(values,4),expansion(q,4)
                for diagonal in (True,False):
                    val,vec = nput.mateigh_deriv(ae,4,diagonal_only=diagonal)
                    self.assertExpansion(val,ve)
                    self.assertExpansion(vec,qe)
                    extended = nput.mateigh_deriv(ae,4,diagonal_only=diagonal,
                                                 base_expansion=(val[:2],vec[:2]))
                    self.assertExpansion(extended[0],ve)
                    self.assertExpansion(extended[1],qe)
                for shape in ((2,),(2,2)):
                    batch = [np.broadcast_to(t,shape+t.shape) for t in ae]
                    val,vec = nput.mateigh_deriv(batch,4)
                    self.assertExpansion(val,[np.broadcast_to(t,shape+t.shape) for t in ve])
                    self.assertExpansion(vec,[np.broadcast_to(t,shape+t.shape) for t in qe])

    def vector_polynomials(self):
        vectors = [random_poly(self.rng,(3,),4) for _ in range(4)]
        for v,base in zip(vectors,([1.,.2,.3],[-.3,1.,.4],[.5,-.4,1.],[1.,.5,-.2])):
            v[(0,0)] = np.array(base)
        return vectors

    def test_vector_norm(self):
        a = self.vector_polynomials()[0]
        squared = multiply(a,a,np.dot,4)
        expected = expansion(power(squared,.5,4),4)
        unit = expansion(multiply(power(squared,-.5,4),a,lambda x,y:x*y,4),4)
        actual = nput.vec_norm_unit_deriv(expansion(a,4),4)
        self.assertExpansion(actual[0],expected)
        self.assertExpansion(actual[1],unit)
        selected = nput.vec_norm_unit_deriv(expansion(a,4),[4,0,2])
        self.assertExpansion(selected[0],[expected[o] for o in (4,0,2)])
        self.assertExpansion(selected[1],[unit[o] for o in (4,0,2)])
        cache = nput.vec_norm_unit_deriv([a[(0,0)],np.eye(3)],5)[0]
        original_length = len(cache)
        cached = nput.vec_norm_unit_deriv(expansion(a,4),4,base_expansion=cache)
        self.assertEqual(len(cache),original_length)
        self.assertExpansion(cached[0],expected)
        self.assertExpansion(cached[1],unit)
        partial = nput.vec_norm_unit_deriv(expansion(a,4),4,base_expansion=cache[:2])
        self.assertExpansion(partial[0],expected)
        self.assertExpansion(partial[1],unit)

    def test_vector_geometry(self):
        a,b,*_ = self.vector_polynomials()
        ae,be = expansion(a,4),expansion(b,4)
        cross = multiply(a,b,np.cross,4)
        cross_squared = multiply(cross,cross,np.dot,4)
        norm = power(cross_squared,.5,4)
        normal = multiply(power(cross_squared,-.5,4),cross,lambda x,y:x*y,4)
        cosine = multiply(a,b,np.dot,4)
        sine = norm
        for vector in (a,b):
            inverse = power(multiply(vector,vector,np.dot,4),-.5,4)
            cosine = multiply(cosine,inverse,lambda x,y:x*y,4)
            sine = multiply(sine,inverse,lambda x,y:x*y,4)
        self.assertExpansion(nput.vec_cross_deriv(ae,be,4),expansion(cross,4))
        self.assertExpansion(nput.vec_anglecos_deriv(ae,be,4),expansion(cosine,4))
        self.assertExpansion(nput.vec_anglesin_deriv(ae,be,4,return_unit_vectors=False),expansion(sine,4))
        self.assertExpansion(nput.vec_normal_deriv(ae,be,4),expansion(normal,4))
        self.assertExpansion(nput.vec_angle_deriv(ae,be,4),expansion(angle_poly(a,b,4),4))
        for operation in (nput.vec_angle_deriv,nput.vec_normal_deriv):
            full = operation(ae,be,4)
            self.assertExpansion(operation(ae,be,[4,0,2]),[full[o] for o in (4,0,2)])

    def test_dihedral(self):
        a,b,c,_ = self.vector_polynomials()
        ae,be,ce = [expansion(v,4) for v in (a,b,c)]
        n1,n2 = multiply(b,a,np.cross,4),multiply(b,c,np.cross,4)
        cosine = multiply(n1,n2,np.dot,4)
        cross = multiply(n1,n2,np.cross,4)
        sine = multiply(multiply(cross,b,np.dot,4),
                        power(multiply(b,b,np.dot,4),-.5,4),lambda x,y:x*y,4)
        phase = {k:v.imag for k,v in log_poly(add(cosine,{k:1j*v for k,v in sine.items()}),4).items()}
        phase[(0,0)] = (phase[(0,0)]%(2*np.pi))-np.pi
        full = nput.vec_dihed_deriv(ae,be,ce,4)
        self.assertExpansion(full,expansion(phase,4))
        self.assertExpansion(nput.vec_dihed_deriv(ae,be,ce,[4,0,2]),[full[o] for o in (4,0,2)])

    def test_plane_angle(self):
        a,b,c,d = self.vector_polynomials()
        expected = expansion(angle_poly(multiply(a,b,np.cross,4),multiply(c,d,np.cross,4),4),4)
        self.assertExpansion(nput.vec_plane_angle_deriv(*[expansion(v,4) for v in (a,b,c,d)],4),expected)

    def test_coordinate_inverse(self):
        a = random_poly(self.rng,(2,),4)
        a[(0,0)] = np.zeros(2)
        a[(1,0)] += np.array([1.,0.])
        a[(0,1)] += np.array([0.,1.])
        forward = expansion(a,4)[1:]
        reverse = nput.inverse_transformation(forward,4)
        independent = compose(polynomial(reverse,False),a,4)
        expected = {(0,0):np.zeros(2),(1,0):np.array([1.,0.]),(0,1):np.array([0.,1.])}
        self.assertExpansion(expansion(independent,4),expansion(expected,4))

    def test_optimizing_transformation(self):
        for stationary in (False,True):
            v = random_poly(self.rng,(),6)
            v[(0,0)] = np.zeros(())
            if stationary:
                v[(1,0)] = v[(0,1)] = np.zeros(())
                v[(2,0)],v[(1,1)],v[(0,2)] = np.array(1.),np.array(.2),np.array(1.5)
            else:
                v[(1,0)],v[(0,1)] = np.array(.6),np.array(.8)
            derivatives = expansion(v,6)[1:]
            transform = nput.optimizing_transformation(derivatives,4)
            result = expansion(compose(polynomial(transform,False),v,6 if stationary else 5),
                               6 if stationary else 5)
            for term in result[3 if stationary else 2:]:
                np.testing.assert_allclose(term,0,atol=2e-10)

    def test_concatenation(self):
        a,b = [expansion(random_poly(self.rng,(2,),3),3)[1:] for _ in range(2)]
        self.assertExpansion(nput.concatenate_expansions(a,b),[np.concatenate([x,y],axis=-1) for x,y in zip(a,b)])
        actual = nput.concatenate_expansions(a,b,concatenate_values=False)
        expected = []
        for o,(x,y) in enumerate(zip(a,b),start=1):
            value = np.zeros((4,)*o+(2,))
            value[(slice(0,2),)*o+(slice(None),)] = x
            value[(slice(2,4),)*o+(slice(None),)] = y
            expected.append(value)
        self.assertExpansion(actual,expected)

    def test_renormalization(self):
        forward = [np.diag([2.,3.]),np.ones((2,2,2))*.03]
        reverse = [np.eye(2),np.ones((2,2,2))*.02]
        for cutoff in (None,.01):
            f,r = nput.renormalize_transformation(forward,reverse,nonzero_cutoff=cutoff)
            np.testing.assert_allclose(f[0]@r[0],np.eye(2),atol=1e-12)

    def test_orthogonalization(self):
        a = np.array([[1.,0.,0.]])
        b = np.array([[.3,1.,0.]])
        pairs = [([a],[a.T]),([b],[b.T])]
        f,r = nput.orthogonalize_transformations(pairs,assume_prenormalized=False,concatenate=False)
        np.testing.assert_allclose(f[0][0]@r[1][0],0,atol=1e-12)
        np.testing.assert_allclose(f[1][0]@r[0][0],0,atol=1e-12)
        combined = nput.orthogonalize_transformations(pairs,assume_prenormalized=False)
        self.assertEqual(combined[0][0].shape,(2,3))
        self.assertEqual(combined[1][0].shape,(3,2))
        np.testing.assert_allclose(combined[0][0]@combined[1][0],np.eye(2),atol=1e-12)

    def test_identical_operands_and_multiple_contraction_axes(self):
        for shape in ((3,),(2,2)):
            a = random_poly(self.rng,shape,4)
            ae = expansion(a,4)
            dot = np.dot if len(shape)==1 else lambda x,y:x@y
            expected = expansion(multiply(a,a,dot,4),4)
            self.assertExpansion(nput.tensordot_deriv(ae,ae,4,identical=True),expected)
            expected = expansion(multiply(a,a,lambda x,y:np.tensordot(x,y,axes=0),4),4)
            self.assertExpansion(nput.tensorprod_deriv(ae,ae,4,axes='all',identical=True),expected)
        a,b = random_poly(self.rng,(2,3,4),4),random_poly(self.rng,(3,4,5),4)
        expected = expansion(multiply(a,b,lambda x,y:np.tensordot(x,y,axes=[[1,2],[0,1]]),4),4)
        self.assertExpansion(nput.tensordot_deriv(expansion(a,4),expansion(b,4),4,
                             axes=[[1,2],[0,1]]),expected)

    def test_geometry_batches_and_explicit_planar_masks(self):
        for shape in ((2,),(2,2)):
            samples = [self.vector_polynomials() for _ in range(math.prod(shape))]
            for i,vectors in enumerate(samples):
                for vector in vectors:
                    vector[(0,0)] += i*np.array([.02,-.03,.01])
            inputs = [[np.stack([expansion(vectors[k],4)[o] for vectors in samples]).reshape(
                shape+(2,)*o+(3,)) for o in range(5)] for k in range(4)]
            operations = (
                ('cross',nput.vec_cross_deriv,lambda a,b:multiply(a,b,np.cross,4)),
                ('angle',nput.vec_angle_deriv,lambda a,b:angle_poly(a,b,4)),
                ('normal',nput.vec_normal_deriv,lambda a,b:multiply(
                    power(multiply(multiply(a,b,np.cross,4),multiply(a,b,np.cross,4),np.dot,4),-.5,4),
                    multiply(a,b,np.cross,4),lambda x,y:x*y,4)))
            for name,operation,oracle in operations:
                expected = [expansion(oracle(v[0],v[1]),4) for v in samples]
                expected = [np.stack([e[o] for e in expected]).reshape(shape+expected[0][o].shape)
                            for o in range(5)]
                self.assertExpansion(operation(inputs[0],inputs[1],4),expected)
            norms,units = nput.vec_norm_unit_deriv(inputs[0],4)
            references = [
                (expansion(power(multiply(v[0],v[0],np.dot,4),.5,4),4),
                 expansion(multiply(power(multiply(v[0],v[0],np.dot,4),-.5,4),
                                    v[0],lambda x,y:x*y,4),4)) for v in samples]
            for actual,component in ((norms,0),(units,1)):
                expected = [np.stack([e[component][o] for e in references]).reshape(
                            shape+references[0][component][o].shape) for o in range(5)]
                self.assertExpansion(actual,expected)
            full = nput.vec_angle_deriv(inputs[0],inputs[1],4)
            self.assertExpansion(nput.vec_angle_deriv(inputs[0],inputs[1],4,
                planar=np.zeros(shape,dtype=bool)),full)

    def test_eigenpair_equations_in_arbitrary_complex_basis(self):
        a = random_poly(self.rng,(3,3),4)
        a = {key:(value+value.T)/2+1j*.1*(value-value.T) for key,value in a.items()}
        a[(0,0)] += np.diag([1.,3.,5.])
        values,vectors = nput.mateigh_deriv(expansion(a,4),4)
        vp,qp = polynomial(values),polynomial(vectors)
        aq = multiply(a,qp,lambda x,y:x@y,4)
        ql = multiply(qp,vp,lambda x,y:x@y,4)
        self.assertExpansion(expansion(aq,4),expansion(ql,4))
        norm = multiply({k:v.T.conj() for k,v in qp.items()},qp,lambda x,y:x@y,4)
        self.assertExpansion(expansion(norm,4),[np.eye(3)]+[0]*4)

    def test_constant_matrix_and_degenerate_eigenvalues(self):
        for base in (np.diag([1.,3.,5.]),np.eye(3)):
            for terms in ([base],[base,np.zeros((2,3,3)),np.zeros((2,2,3,3))]):
                values,vectors = nput.mateigh_deriv(terms,4)
                self.assertExpansion(values,[np.diag(np.linalg.eigvalsh(base))]+[0]*4)
                self.assertExpansion(vectors,[np.eye(3)]+[0]*4)
        with self.assertRaises(ValueError):
            nput.mateigh_deriv([np.eye(3),np.ones((2,3,3))],2)
        with self.assertRaises(np.linalg.LinAlgError):
            nput.matinv_deriv([np.zeros((3,3))],2)

    def test_vector_zero_domain_and_order_lists(self):
        with self.assertRaises(ValueError):
            nput.vec_norm_unit_deriv([np.zeros(3)],2,raise_on_failure=True)
        self.assertEqual(nput.vec_norm_unit_deriv([np.zeros(3)],2),(None,None))
        a,b,*_ = self.vector_polynomials()
        ae,be = expansion(a,4),expansion(b,4)
        cross = expansion(multiply(a,b,np.cross,4),4)
        self.assertExpansion(nput.vec_normal_deriv(ae,be,4,normalize=False),cross)
        for operation in (nput.vec_anglecos_deriv,nput.vec_cross_deriv):
            full = operation(ae,be,4)
            self.assertExpansion(operation(ae,be,[4,0,2]),[full[o] for o in (4,0,2)])
        full = nput.vec_anglesin_deriv(ae,be,4)
        selected = nput.vec_anglesin_deriv(ae,be,[4,0,2])
        for a,b in zip(selected,full):
            self.assertExpansion(a,[b[o] for o in (4,0,2)])

    def test_regularized_normalization_and_higher_zero_orders(self):
        f,r = nput.renormalize_transformation([np.diag([2.,0.])],[np.eye(2)],nonzero_cutoff=.01)
        np.testing.assert_allclose(f[0]@r[0],np.diag([1.,0.]),atol=1e-12)
        a,b = np.array([[1.,0.,0.]]),np.array([[.3,1.,0.]])
        pairs = [([a,0],[a.T,0]),([b,0],[b.T,0])]
        f,r = nput.orthogonalize_transformations(pairs,order=2,
            assume_prenormalized=False,first_order_projector=False)
        np.testing.assert_allclose(f[0]@r[0],np.eye(2),atol=1e-12)
        self.assertExpansion(f[1:],[0])
        self.assertExpansion(r[1:],[0])

    def test_internal_matrix_kernel_batches(self):
        for shape in ((2,),(2,2)):
            examples,expected = [],[]
            for _ in range(math.prod(shape)):
                a,b,c = [random_poly(self.rng,s,3) for s in ((2,2),(3,3),(2,3))]
                a[(0,0)] += np.diag([2.,3.])
                b[(0,0)] += np.diag([1.,4.,5.])
                result = {}
                for alpha in sorted(indices(2,3),key=sum):
                    rhs = c[alpha].copy()
                    for beta in a:
                        if sum(beta)>0 and all(x>=y for x,y in zip(alpha,beta)):
                            rest = result[tuple(x-y for x,y in zip(alpha,beta))]
                            rhs -= a[beta]@rest+rest@b[beta]
                    result[alpha] = solve_sylvester(a[(0,0)],b[(0,0)],rhs)
                examples.append(tuple(expansion(p,3) for p in (a,b,c)))
                expected.append(expansion(result,3))
            batch = [[np.stack([e[k][o] for e in examples]).reshape(shape+examples[0][k][o].shape)
                      for o in range(4)] for k in range(3)]
            reference = [np.stack([e[o] for e in expected]).reshape(shape+expected[0][o].shape) for o in range(4)]
            for shared in (None,len(shape)):
                actual,_ = td.sylv_derivs(*batch,3,shared=shared)
                self.assertExpansion(actual,reference)


if __name__ == '__main__':
    unittest.main(verbosity=2)

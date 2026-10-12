"""A reproducible matrix of input expansion forms, dimensions, and batches."""
import itertools
import math
import unittest
import numpy as np
from scipy.linalg import solve_sylvester
from McUtils import Numputils as nput
from TensorDerivativeRegressionTests import expansion, indices, multiply, power
from TensorDerivativeOperationTests import add, angle_poly, log_poly


class TensorExpansionMatrixTests(unittest.TestCase):
    forms = ('constant', 'linear', 'dense', 'sparse')
    batch_shapes = ((), (2,), (2,2))
    dimensions = (1,2,3)
    seeds = (819,2741)
    cases = []

    def grid(self):
        for seed,n,form,batch in itertools.product(self.seeds,self.dimensions,self.forms,self.batch_shapes):
            yield np.random.default_rng(seed), n, form, batch

    @staticmethod
    def make(rng,n,form,shape,base):
        orders = {'constant':{0},'linear':{0,1},'dense':{0,1,2,3,4},'sparse':{0,1,3,4}}[form]
        result = {key:rng.normal(size=shape)*.015 for key in indices(n,4) if sum(key) in orders}
        result[(0,)*n] = np.asarray(base)+rng.normal(size=shape)*.01
        return result

    @staticmethod
    def pack(samples,n,batch,form=None):
        terms = [expansion(p,4,ncoords=n) for p in samples]
        if batch:
            terms = [np.stack([e[o] for e in terms]).reshape(batch+terms[0][o].shape) for o in range(5)]
        else:
            terms = terms[0]
        if form == 'constant':
            return terms[:1]
        if form == 'linear':
            return terms[:2]
        if form == 'sparse':
            terms[2] = 0
        return terms

    def check(self,actual,expected,label):
        self.assertEqual(len(actual),5)
        for o,(a,b) in enumerate(zip(actual,expected)):
            with self.subTest(order=o,operation=label):
                np.testing.assert_allclose(a,b,atol=2e-10,rtol=3e-10)

    def record(self,group,n,form,batch,seed):
        self.cases.append({'group':group,'coordinates':n,'form':form,
                           'batch_shape':list(batch),'seed':seed})

    def test_matrix_and_scalar_expansion_grid(self):
        for index,(rng,n,form,batch) in enumerate(self.grid()):
            with self.subTest(coordinates=n,form=form,batch=batch,seed=index//36):
                count = math.prod(batch) if batch else 1
                matrices = [self.make(rng,n,form,(2,2),[[2.,.1],[.1,3.]]) for _ in range(count)]
                scalars = [self.make(rng,n,form,(),2.) for _ in range(count)]
                ae,se = self.pack(matrices,n,batch,form),self.pack(scalars,n,batch,form)
                inverses, determinants, roots = [], [], []
                for a in matrices:
                    zero = (0,)*n
                    inverse = {zero:np.linalg.inv(a[zero])}
                    root = {zero:None}
                    # Symmetrize a separate matrix model for the principal root.
                    symmetric = {k:(v+v.T)/2 for k,v in a.items()}
                    vals,vecs = np.linalg.eigh(symmetric[zero])
                    root[zero] = (vecs*np.sqrt(vals))@vecs.T
                    for alpha in sorted(indices(n,4),key=sum)[1:]:
                        residual = sum((v@inverse[tuple(i-j for i,j in zip(alpha,beta))]
                            for beta,v in a.items() if sum(beta)>0 and all(j<=i for i,j in zip(alpha,beta))),
                            np.zeros((2,2)))
                        inverse[alpha] = -inverse[zero]@residual
                        residual = sum((v@root[tuple(i-j for i,j in zip(alpha,beta))]
                            for beta,v in root.items() if beta != zero
                            and all(j<=i for i,j in zip(alpha,beta))),np.zeros((2,2)))
                        root[alpha] = solve_sylvester(root[zero],root[zero],symmetric.get(alpha,0)-residual)
                    inverses.append(inverse)
                    roots.append(root)
                    determinants.append(add(multiply({k:v[0,0] for k,v in a.items()},
                        {k:v[1,1] for k,v in a.items()},lambda x,y:x*y),
                        {k:-v for k,v in multiply({k:v[0,1] for k,v in a.items()},
                            {k:v[1,0] for k,v in a.items()},lambda x,y:x*y).items()}))
                self.check(nput.matinv_deriv(ae,4),self.pack(inverses,n,batch),'inverse')
                self.check(nput.matdet_deriv(ae,4),self.pack(determinants,n,batch),'determinant')
                symmetric = self.pack([{k:(v+v.T)/2 for k,v in a.items()} for a in matrices],n,batch,form)
                self.check(nput.matsqrt_deriv(symmetric,4),self.pack(roots,n,batch),'square root')
                expected = self.pack([multiply(a,a,lambda x,y:x@y) for a in matrices],n,batch)
                self.check(nput.tensordot_deriv(ae,ae,4,axes=[-1,len(batch)],shared=len(batch)),expected,'contraction')
                self.check(nput.tensorops_deriv(ae,[-1,len(batch)],ae,order=4,shared=len(batch)),expected,'operation stack')
                expected = self.pack([multiply(a,a,lambda x,y:np.tensordot(x,y,axes=0)) for a in matrices],n,batch)
                self.check(nput.tensorprod_deriv(ae,ae,4,axes=[[-2,-1],[-2,-1]]),expected,'tensor product')
                self.check(nput.scalarprod_deriv(se,ae,4),
                    self.pack([multiply(s,a,lambda x,y:x*y) for s,a in zip(scalars,matrices)],n,batch),'scalar product')
                for p in (-1.,-.5,.5,2.):
                    self.check(nput.scalarpow_deriv(se,p,4),self.pack([power(s,p) for s in scalars],n,batch),'power '+str(p))
                self.check(nput.scalarinv_deriv(se,4),self.pack([power(s,-1.) for s in scalars],n,batch),'scalar inverse')
                self.record('matrix/scalar',n,form,batch,self.seeds[index//36])

    def test_vector_geometry_expansion_grid(self):
        for index,(rng,n,form,batch) in enumerate(self.grid()):
            with self.subTest(coordinates=n,form=form,batch=batch,seed=index//36):
                count = math.prod(batch) if batch else 1
                samples = [[self.make(rng,n,form,(3,),base) for base in
                    ([1.,.2,.3],[-.3,1.,.4],[.5,-.4,1.],[1.,.5,-.2])] for _ in range(count)]
                packed = [self.pack([sample[k] for sample in samples],n,batch,form) for k in range(4)]
                expected = {name:[] for name in ('norm','unit','cross','normal','cosine','sine','angle','plane','dihedral')}
                for a,b,c,d in samples:
                    aa,bb = multiply(a,a,np.dot),multiply(b,b,np.dot)
                    cross = multiply(a,b,np.cross)
                    cc = multiply(cross,cross,np.dot)
                    invnorms = multiply(power(aa,-.5),power(bb,-.5),lambda x,y:x*y)
                    expected['norm'].append(power(aa,.5))
                    expected['unit'].append(multiply(power(aa,-.5),a,lambda x,y:x*y))
                    expected['cross'].append(cross)
                    expected['normal'].append(multiply(power(cc,-.5),cross,lambda x,y:x*y))
                    expected['cosine'].append(multiply(multiply(a,b,np.dot),invnorms,lambda x,y:x*y))
                    expected['sine'].append(multiply(power(cc,.5),invnorms,lambda x,y:x*y))
                    expected['angle'].append(angle_poly(a,b,4))
                    expected['plane'].append(angle_poly(cross,multiply(c,d,np.cross),4))
                    ab,bc = cross,multiply(b,c,np.cross)
                    cosine = multiply(ab,bc,np.dot)
                    sine = multiply(multiply(multiply(ab,bc,np.cross),b,np.dot),power(bb,-.5),lambda x,y:x*y)
                    phase = {k:v.imag for k,v in log_poly(add(cosine,{k:1j*v for k,v in sine.items()}),4).items()}
                    expected['dihedral'].append(phase)
                norm,unit = nput.vec_norm_unit_deriv(packed[0],4)
                self.check(norm,self.pack(expected['norm'],n,batch),'norm')
                self.check(unit,self.pack(expected['unit'],n,batch),'unit vector')
                for name,func,operands in (
                    ('cross',nput.vec_cross_deriv,packed[:2]),
                    ('normal',nput.vec_normal_deriv,packed[:2]),
                    ('cosine',nput.vec_anglecos_deriv,packed[:2]),
                    ('sine',nput.vec_anglesin_deriv,packed[:2]),
                    ('angle',nput.vec_angle_deriv,packed[:2]),
                    ('plane',nput.vec_plane_angle_deriv,packed),
                    ('dihedral',nput.vec_dihed_deriv,packed[:3])):
                    opts = {'return_unit_vectors':False} if name=='sine' else {}
                    self.check(func(*operands,4,**opts),self.pack(expected[name],n,batch),label=name)
                self.record('geometry',n,form,batch,self.seeds[index//36])

if __name__ == '__main__':
    unittest.main(verbosity=2)

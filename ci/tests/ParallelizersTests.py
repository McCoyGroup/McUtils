import itertools
import time

from Peeves.TestUtils import *
from McUtils.Scaffolding import Logger
from McUtils.Parallelizers import *
from unittest import TestCase
import numpy as np, io, os, sys, tempfile as tmpf

# @Parallelizer.main_restricted
# def main_print(*args, parallelizer=None):
#     print(*args)
# @Parallelizer.worker_restricted
# def worker_print(*args, parallelizer=None):
#     print(*args)
# def run_job(parallelizer=None):
#     if parallelizer.on_main:
#         data = np.arange(1000)
#     else:
#         data = None
#     data = parallelizer.scatter(data)
#     lens = parallelizer.gather(len(data))
#     return lens

class ParallelizerTests(TestCase):

    # we don't really even need to send or get any state for these tests
    def __getstate__(self):
        return {}
    def __setstate__(self, state):
        pass

    def run_job(self, parallelizer:Parallelizer=None):
        time.sleep(3)
        if parallelizer.on_main:
            data = np.arange(1000)
        else:
            data = None
        if parallelizer.on_main:
            flag = "woop"
        else:
            flag = None
        test = parallelizer.broadcast(flag)
        # self.worker_print(test)
        data = parallelizer.scatter(data)
        lens = parallelizer.gather(len(data))
        return sum(lens)
    @validationTest
    def test_BasicMultiprocessing(self):
        par_lens = MultiprocessingParallelizer(processes=5, initialization_timeout=2).run(self.run_job)
        serial_lens = SerialNonParallelizer().run(self.run_job)
        self.assertEquals(par_lens, serial_lens)

    def mapped_func(self, data):
        return [
            sum(1 + d for d in p)
            for c in data
            for p in itertools.permutations(c)
        ]
    def map_applier(self, n=12, r=9, parallelizer=None):
        if parallelizer.on_main:
            data = list(itertools.combinations(range(n), r))
        else:
            data = None
        return parallelizer.map(self.mapped_func, data, vectorized=True)
    @debugTest
    def test_MapMultiprocessing(self):
        from McUtils.Profilers import Timer
        with MultiprocessingParallelizer(initialization_timeout=1) as par:
            with Timer():
               par_lens = par.run(self.map_applier)

        with Timer():
            serial_lens = SerialNonParallelizer().run(self.map_applier)
        self.assertEquals(par_lens, serial_lens)
    @validationTest
    def test_MapMultiprocessingDataSmall(self):
        par_lens = MultiprocessingParallelizer().run(self.map_applier, n=3, comm=[0, 1, 2])
        self.assertEquals(len(par_lens), 3)
        serial_lens = SerialNonParallelizer().run(self.map_applier, n=3)
        self.assertEquals(par_lens, serial_lens)

    def bcast_parallelizer(self, parallelizer=None):
        root_par = parallelizer.broadcast(parallelizer)
    @validationTest
    def test_BroadcastParallelizer(self):
        with MultiprocessingParallelizer() as parallelizer:
            parallelizer.run(self.bcast_parallelizer)
            parallelizer.run(self.bcast_parallelizer)

    def scatter_gather(self, n=1000, parallelizer=None):
        if parallelizer.on_main:
            data = np.arange(n)
        else:
            data = None
        data = parallelizer.scatter(data)
        l = len(data)
        res = parallelizer.gather(l)
        return res
    @validationTest
    def test_ScatterGatherMultiprocessing(self):
        p = MultiprocessingParallelizer()
        par_lens = p.run(self.scatter_gather)
        self.assertEquals(len(par_lens), p.nprocs+1)
        serial_lens = SerialNonParallelizer().run(self.scatter_gather)
        self.assertEquals(sum(par_lens), serial_lens)
    @validationTest
    def test_ScatterGatherMultiprocessingDataSmall(self):
        par_lens = MultiprocessingParallelizer().run(self.scatter_gather, 3, comm=[0, 1, 2])
        self.assertEquals(len(par_lens), 3)
        serial_lens = SerialNonParallelizer().run(self.scatter_gather, 3)
        self.assertEquals(sum(par_lens), serial_lens)

    def simple_scatter_1(self, parallelizer=None):
        data = [
            np.array([[0, 0]]), np.array([[0, 1]]), np.array([[0, 2]]),
            np.array([[1, 0]]), np.array([[1, 1]]), np.array([[1, 2]]),
            np.array([[2, 0]]), np.array([[2, 1]]), np.array([[2, 2]])
        ]
        data = parallelizer.scatter(data)
        l = len(data)
        l = parallelizer.gather(l)
        return l
    def simple_print(self, parallelizer=None):
        parallelizer.print(1)
    @validationTest
    def test_MiscProblems(self):

        l = MultiprocessingParallelizer().run(self.simple_scatter_1, comm=[0, 1, 2, 3, 4, 5, 6, 7, 8])
        MultiprocessingParallelizer().run(self.simple_print, comm=[0, 1, 2])
        # raise Exception(l)

    @validationTest
    def test_MakeSharedMem(self):

        a = np.random.rand(10, 5, 5)
        manager = SharedObjectManager(a)

        saved = manager.share()
        loaded = manager.unshare() #type: np.ndarray
        # print(type(loaded), loaded.shape, loaded.data, loaded.size)

        self.assertTrue(np.allclose(a, loaded))


    def mutate_shared_dict(self, d, parallelizer=None):
        wat = d['d']
        parallelizer.print('{a} {b} {c} {d}', a=id(wat), b=id(d['d']), c=id(d['d']), d=d)
        if not parallelizer.on_main:
            d['a'][1, 0, 0] = 5
            wat['key'] = 5
        parallelizer.print('{v} {g}', v=wat, g=d['d'])

    @validationTest
    def test_DistributedDict(self):

         my_data = {'a':np.random.rand(10, 5, 5), 'b':np.random.rand(10, 3, 8), 'c':np.random.rand(10, 15, 4), 'd':{}}

         par = MultiprocessingParallelizer(processes=2, logger=Logger())
         my_data = par.share(my_data)

         par.run(self.mutate_shared_dict, my_data)

         self.assertEquals(my_data['a'][1, 0, 0], 5.0)

         my_data = my_data.unshare()
         self.assertIsInstance(my_data, dict)
         self.assertIsInstance(my_data['a'], np.ndarray)

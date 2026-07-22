"""Extracted from ParallelizerTests.test_MapMultiprocessingDataSmall via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ParallelizerTests.test_MapMultiprocessingDataSmall"""

import itertools
import time
from Peeves.TestUtils import *
from McUtils.Scaffolding import Logger
from McUtils.Parallelizers import *
from unittest import TestCase
import numpy as np, io, os, sys, tempfile as tmpf

class ParallelizerTests(TestCase):

    def __getstate__(self):
        return {}

    def __setstate__(self, state):
        pass

    def run_job(self, parallelizer: Parallelizer=None):
        time.sleep(3)
        if parallelizer.on_main:
            data = np.arange(1000)
        else:
            data = None
        if parallelizer.on_main:
            flag = 'woop'
        else:
            flag = None
        test = parallelizer.broadcast(flag)
        data = parallelizer.scatter(data)
        lens = parallelizer.gather(len(data))
        return sum(lens)

    def mapped_func(self, data):
        return [sum((1 + d for d in p)) for c in data for p in itertools.permutations(c)]

    def map_applier(self, n=12, r=9, parallelizer=None):
        if parallelizer.on_main:
            data = list(itertools.combinations(range(n), r))
        else:
            data = None
        return parallelizer.map(self.mapped_func, data, vectorized=True)

    def bcast_parallelizer(self, parallelizer=None):
        root_par = parallelizer.broadcast(parallelizer)

    def scatter_gather(self, n=1000, parallelizer=None):
        if parallelizer.on_main:
            data = np.arange(n)
        else:
            data = None
        data = parallelizer.scatter(data)
        l = len(data)
        res = parallelizer.gather(l)
        return res

    def simple_scatter_1(self, parallelizer=None):
        data = [np.array([[0, 0]]), np.array([[0, 1]]), np.array([[0, 2]]), np.array([[1, 0]]), np.array([[1, 1]]), np.array([[1, 2]]), np.array([[2, 0]]), np.array([[2, 1]]), np.array([[2, 2]])]
        data = parallelizer.scatter(data)
        l = len(data)
        l = parallelizer.gather(l)
        return l

    def simple_print(self, parallelizer=None):
        parallelizer.print(1)

    def mutate_shared_dict(self, d, parallelizer=None):
        wat = d['d']
        parallelizer.print('{a} {b} {c} {d}', a=id(wat), b=id(d['d']), c=id(d['d']), d=d)
        if not parallelizer.on_main:
            d['a'][1, 0, 0] = 5
            wat['key'] = 5
        parallelizer.print('{v} {g}', v=wat, g=d['d'])

    @validationTest
    def test_MapMultiprocessingDataSmall(self):
        par_lens = MultiprocessingParallelizer().run(self.map_applier, n=3, comm=[0, 1, 2])
        self.assertEquals(len(par_lens), 3)
        serial_lens = SerialNonParallelizer().run(self.map_applier, n=3)
        self.assertEquals(par_lens, serial_lens)

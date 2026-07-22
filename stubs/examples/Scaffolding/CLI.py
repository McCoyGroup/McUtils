"""Extracted from ScaffoldingTests.test_CLI via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ScaffoldingTests.test_CLI"""

from Peeves.TestUtils import *
import McUtils.Devutils as dev
from McUtils.Scaffolding import *
import McUtils.Parsers as parsers
from unittest import TestCase
import numpy as np, io, os, sys, tempfile as tmpf

class ScaffoldingTests(TestCase):

    class DataHolderClass:

        def __init__(self, **keys):
            self.data = keys

        def to_state(self, serializer=None):
            return self.data

        @classmethod
        def from_state(cls, state, serializer=None):
            return cls(**state)

    @validationTest
    def test_CLI(self):
        import McUtils.Plots as plt

        class PlottingInterface(CommandGroup):
            _tag = 'plot'

            @classmethod
            def random(cls, npts: int=100, file: str=None):
                """Makes a random plot of however many points you want"""
                xy = np.random.rand(npts, npts)
                ploot = plt.ArrayPlot(xy)
                if file is None:
                    ploot.show()
                else:
                    ploot.savefig(file)

            @classmethod
            def contour(cls, npts: int=100, file: str=None):
                """Makes a random contour plot of however many points you want"""
                xy = np.random.rand(npts, npts)
                ploot = plt.ListContourPlot(xy)
                if file is None:
                    ploot.show()
                else:
                    ploot.savefig(file)
        import McUtils.Data as data

        class DataInterface(CommandGroup):
            _tag = 'data'

            @classmethod
            def mass(cls, elem: str):
                """Gets the mass for the passed element spec"""
                print(data.AtomData[elem]['Mass'])
        mccli = CLI('McUtils', 'defines a simple CLI interface to various bits of McUtils', PlottingInterface, DataInterface, cmd_name='mcutils')
        print()
        with tmpf.NamedTemporaryFile() as out:
            argv = sys.argv
            try:
                sys.argv = ['mccli', '--help']
                mccli.run()
                sys.argv = ['mccli', 'plot', 'contour', '--npts=100']
                mccli.run()
                sys.argv = ['mccli', 'data', 'mass', 'T']
                mccli.run()
            finally:
                sys.argv = argv

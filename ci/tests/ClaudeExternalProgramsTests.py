"""
Tests for `McUtils.ExternalPrograms`, drafted from the `McUtils/stubs/McUtils/ExternalPrograms`
docstrings (`ManagedJobQueues.py`, `Jobs/SBatch.py`, `Interface.py`, `RDKit.py`, and
the `ExternalMolecule` contract summarized in `summaries/ExternalPrograms.md`).

This is a 44-module package wrapping a wide variety of external programs, job
schedulers, and file formats; most of it needs either a real HPC scheduler
(SLURM), a real quantum-chemistry binary (Gaussian/Orca/MOLPRO/PSI4), or a
GUI/network dependency (Jupyter widgets, PubChem) to meaningfully exercise, so
this suite is deliberately scoped to what can be validated headlessly:

- `ManagedJobQueueSubmissionHandler`/`SLURMSubmissionHandler`: pure string/command
  formatting -- no scheduler needed.
- `SBatchJob`: pure `#SBATCH` script formatting -- no scheduler needed.
- `ExternalProgramInterface`: a generic lazy-module-dispatch mixin, exercised here
  against a stand-in from the standard library instead of a real chemistry
  package, since the dispatch logic itself doesn't care what the target module is.
- `RDMolecule`/`RDKitInterface`: real chemistry, using `rdkit` (installed via pip
  for this session -- it's a pure-wheel package with no system dependency, unlike
  most of this package's other backends).

Plain `unittest` is used, matching the rest of this batch.
"""

import unittest

import numpy as np

from McUtils.ExternalPrograms import SLURMSubmissionHandler, SBatchJob, RDKitInterface, RDMolecule


class ExternalProgramsTests(unittest.TestCase):
    """
    Exercises the headlessly-testable parts of `McUtils.ExternalPrograms`: SLURM
    job-submission string formatting, `SBatchJob` script generation, the generic
    `ExternalProgramInterface` lazy-dispatch mixin, and the RDKit-backed
    `RDMolecule` chemistry interface.
    """

    # region ManagedJobQueues: SLURMSubmissionHandler

    def test_MapOptionName(self):
        """`map_option_name` converts a Python-style snake_case option into a GNU-style `--kebab-case` flag."""
        self.assertEqual(SLURMSubmissionHandler.map_option_name('job_name'), '--job-name')
        self.assertEqual(SLURMSubmissionHandler.map_option_name('mem'), '--mem')

    def test_FormatJobArgs(self):
        """`format_job_args` emits a bare flag for `True`, omits `False`/`None`, and emits `flag value` otherwise."""
        args = SLURMSubmissionHandler.format_job_args(job_name='test', verbose=True, quiet=False, mem=None)
        self.assertEqual(args, ['--job-name', 'test', '--verbose'])

    def test_GetJobCommand(self):
        """`get_job_command` assembles `[executable, *options, *positional_args]`."""
        cmd = SLURMSubmissionHandler.get_job_command('script.sh', job_name='test')
        self.assertEqual(cmd, ['sbatch', '--job-name', 'test', 'script.sh'])

    def test_ParseJobId(self):
        """`parse_job_id` extracts the numeric id from SLURM's `Submitted batch job N` response."""
        self.assertEqual(SLURMSubmissionHandler.parse_job_id('Submitted batch job 123456\n'), '123456')

    # endregion

    # region Jobs.SBatch: SBatchJob

    def test_SBatchJobFormat(self):
        """`SBatchJob.format` embeds the requested `#SBATCH` options and job steps into a runnable script."""
        job = SBatchJob(
            "A test job",
            job_name="myjob",
            mem="4GB",
            steps=["echo hi", "sleep 1"]
        )
        script = job.format()
        self.assertTrue(script.startswith("#!/bin/bash"))
        self.assertIn("#SBATCH --job-name=myjob", script)
        self.assertIn("#SBATCH --mem=4GB", script)
        self.assertIn("echo hi", script)
        self.assertIn("sleep 1", script)

    # endregion

    # region Interface: ExternalProgramInterface (generic dispatch, using a stdlib stand-in)

    def test_ExternalProgramInterfaceMethodDispatch(self):
        from McUtils.McUtils.ExternalPrograms.Interface import ExternalProgramInterface
        """`ExternalProgramInterface.method` lazily resolves and returns a callable from the target module."""
        class FakeInterface(ExternalProgramInterface):
            name = 'fake'
            module = 'math'

        sqrt_method = FakeInterface.method('sqrt')
        self.assertEqual(sqrt_method(16), 4.0)
        self.assertIsInstance(FakeInterface().lib, type(__import__('math')))


    # endregion

    # region RDKit.py: RDMolecule (a concrete ExternalMolecule)

    def test_RDMoleculeFromSmilesRequiresExplicitHydrogenRequest(self):
        """
        `RDMolecule.from_smiles` defaults to `add_implicit_hydrogens=False`, so a bare
        `from_smiles('O')` returns a single, hydrogen-less oxygen atom rather than a
        full water molecule -- `add_implicit_hydrogens=True` (plus a conformer) is
        required to get the chemically complete molecule (see
        `test_RDMoleculeFromSmilesWithHydrogens` below).
        """
        mol = RDMolecule.from_smiles('O')
        self.assertEqual(list(mol.atoms), ['O'])
        self.assertEqual(list(mol.bonds), [])

    def test_RDMoleculeFromSmilesWithHydrogens(self):
        """`RDMolecule.from_smiles(..., add_implicit_hydrogens=True, num_confs=1)` builds a complete, embedded water molecule."""
        mol = RDMolecule.from_smiles('O', add_implicit_hydrogens=True, num_confs=1, optimize=True)
        self.assertEqual(list(mol.atoms), ['O', 'H', 'H'])
        self.assertEqual(np.asarray(mol.coords).shape, (3, 3))
        self.assertTrue(np.allclose(sorted(mol.masses), sorted([15.99491461957, 1.00782503223, 1.00782503223])))
        # two O-H single bonds, each recorded as [atom_i, atom_j, bond_order]
        self.assertEqual(len(mol.bonds), 2)
        for i, j, order in mol.bonds:
            self.assertEqual({i, j} & {0}, {0})  # every bond touches the oxygen (index 0)
            self.assertAlmostEqual(order, 1.0)

    def test_RDMoleculeForceFieldEnergyAndGradient(self):
        """An MMFF-optimized `RDMolecule` sits at (near) a force-field energy minimum: tiny energy and near-zero gradient."""
        mol = RDMolecule.from_smiles('O', add_implicit_hydrogens=True, num_confs=1, optimize=True)
        energy = mol.calculate_energy()
        gradient = mol.calculate_gradient()
        self.assertLess(abs(energy), 1e-4)
        self.assertEqual(gradient.shape, (9,))  # 3 atoms x 3 Cartesian components, flattened
        self.assertLess(np.max(np.abs(gradient)), 1e-2)

    def test_RDMoleculeForceFieldHessianSymmetric(self):
        """`RDMolecule.calculate_hessian` returns a symmetric `(3N, 3N)` Cartesian Hessian."""
        mol = RDMolecule.from_smiles('O', add_implicit_hydrogens=True, num_confs=1, optimize=True)
        hess = mol.calculate_hessian()
        self.assertEqual(hess.shape, (9, 9))
        self.assertTrue(np.allclose(hess, hess.T, atol=1e-4))

    # endregion


if __name__ == '__main__':
    unittest.main(verbosity=2)

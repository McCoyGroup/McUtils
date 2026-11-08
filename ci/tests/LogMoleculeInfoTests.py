"""Electronic-state metadata uses the standard log readers and job summaries."""
import os
import tempfile
import unittest

from McUtils.ExternalPrograms import (
    GaussianLogReader, QChemLogReader, OrcaLogReader,
    GaussianJob, QChemJob, OrcaJob,
)


def gaussian_state(charge='+1', multiplicity=2):
    return f' Charge = {charge} Multiplicity = {multiplicity}\n NAtoms= 2 NActive= 2 NUniq= 1\n'


def qchem_state(charge='+1', multiplicity=2):
    return f'$molecule\n{charge} {multiplicity}\nH 0 0 0\nH 0 0 1\n$end\n'


def orca_state(charge='+1', multiplicity=2):
    return (f' Total Charge           Charge          ....    {charge}\n'
            f' Multiplicity           Mult            ....    {multiplicity}\n'
            ' Number of Electrons    NEL             ....    1\n\n')


class LogMoleculeInfoTests(unittest.TestCase):
    formats = [(GaussianLogReader, GaussianJob, gaussian_state),
               (QChemLogReader, QChemJob, qchem_state),
               (OrcaLogReader, OrcaJob, orca_state)]

    def read(self, reader_type, text, **opts):
        with tempfile.TemporaryDirectory() as tempdir:
            path = os.path.join(tempdir, 'job.out')
            with open(path, 'w') as stream:
                stream.write(text)
            with reader_type(path) as reader:
                return reader.parse('MoleculeInfo', **opts)['MoleculeInfo']

    def test_signed_charges_and_multiplicities(self):
        for reader, job, state in self.formats:
            for charge, multiplicity in [('+1', 2), ('-1', 2), ('0', 1), ('0', 3)]:
                with self.subTest(reader=reader.__name__, charge=charge, multiplicity=multiplicity):
                    expected = {'charge': int(charge), 'multiplicity': multiplicity}
                    self.assertEqual(self.read(reader, state(charge, multiplicity))[0], expected)
                    result = job.parse_output(state(charge, multiplicity))
                    self.assertEqual({k: result[k] for k in expected}, expected)

    def test_last_record_wins_in_job_summary(self):
        for reader, job, state in self.formats:
            with self.subTest(reader=reader.__name__):
                result = job.parse_output(state('0', 1) + state('-1', 2))
                self.assertEqual((result['charge'], result['multiplicity']), (-1, 2))

    def test_missing_metadata_does_not_invent_state(self):
        for reader, job, state in self.formats:
            with self.subTest(reader=reader.__name__):
                self.assertEqual(self.read(reader, 'No electronic-state header\n'), [])
                result = job.parse_output('No electronic-state header\n')
                self.assertNotIn('charge', result)
                self.assertNotIn('multiplicity', result)
                self.assertNotIn('charge', job.parse_output(''))

    def test_string_and_file_readers_share_components(self):
        for reader_type, job, state in self.formats:
            with self.subTest(reader=reader_type.__name__):
                text = state()
                with reader_type.from_string(text) as reader:
                    self.assertEqual(reader.parse('MoleculeInfo')['MoleculeInfo'], self.read(reader_type, text))

    def test_qchem_comments_uppercase_and_fragments(self):
        text = '$MOLECULE\n! total system\n+1 2 # cation\n--\n0 1\nH 0 0 0\n--\n+1 2\nH 0 0 1\n$END\n'
        self.assertEqual(self.read(QChemLogReader, text), [{'charge': 1, 'multiplicity': 2}])

    def test_gaussian_fragment_states_do_not_replace_total_state(self):
        text = (' Charge = +1 Multiplicity = 2 in supermolecule\n'
                ' Charge = 0 Multiplicity = 1 in fragment 1.\n'
                ' Charge = +1 Multiplicity = 2 in fragment 2.\n'
                ' Charge = -1 Multiplicity = 1 in fragment 3.\n')
        result = GaussianJob.parse_output(text)
        self.assertEqual((result['charge'], result['multiplicity']), (1, 2))
        self.assertEqual(self.read(GaussianLogReader, text)[-1]['fragment'], 3)

    def test_qchem_read_inherits_but_external_file_is_unknown(self):
        text = qchem_state('-1', 2) + '$molecule\nread\n$end\n'
        self.assertEqual(self.read(QChemLogReader, text)[-1], {'charge': -1, 'multiplicity': 2})
        result = QChemJob.parse_output(text + '$molecule\nread other.mol\n$end\n')
        self.assertNotIn('charge', result)
        self.assertNotIn('multiplicity', result)

    def test_orca_partial_and_terminal_header(self):
        text = ' Total Charge           Charge          ....    -1\n'
        self.assertEqual(self.read(OrcaLogReader, text), [{'charge': -1}])
        text += ' Multiplicity           Mult            ....    2\n'
        self.assertEqual(self.read(OrcaLogReader, text), [{'charge': -1, 'multiplicity': 2}])

    def test_population_charges_and_spin_squared_are_not_metadata(self):
        text = ('Mulliken atomic charges\n1 H +1\nSum of atomic charges = 1.0\n'
                'Expectation value of <S**2> : 0.75\n')
        for reader, job, state in self.formats:
            with self.subTest(reader=reader.__name__):
                self.assertEqual(self.read(reader, text), [])

    def test_metadata_does_not_replace_energy_and_status(self):
        endings = [
            ' SCF Done:  E(UHF) = -0.500000 A.U.\n Normal termination of Gaussian\n',
            ' Total energy in the final basis set = -0.500000\nOPTIMIZATION CONVERGED\nThank you very much for using Q-Chem\n',
            'FINAL SINGLE POINT ENERGY -0.500000\nTHE OPTIMIZATION HAS CONVERGED\nORCA TERMINATED NORMALLY\n',
        ]
        for (reader, job, state), ending in zip(self.formats, endings):
            with self.subTest(job=job.__name__):
                result = job.parse_output(state() + ending)
                self.assertEqual(result['energy'], -.5)
                self.assertEqual(result['energies'], [-.5])
                self.assertTrue(result['terminated_normally'])
                if job is not GaussianJob:
                    self.assertTrue(result['optimized'])

    def test_list_parse_limits_and_reset(self):
        for reader_type, job, state in self.formats:
            with self.subTest(reader=reader_type.__name__):
                self.assertEqual(self.read(reader_type, state() + state('-1', 2), num=1)[0]['charge'], 1)
                with reader_type.from_string(state()) as reader:
                    start = reader.tell()
                    reader.parse('MoleculeInfo', reset=True)
                    self.assertEqual(reader.tell(), start)


if __name__ == '__main__':
    unittest.main()

import glob
import os
from .. import Devutils as dev
import io, numpy as np

from .RDKit import RDMolecule
from . import SMILES

__all__ = [
    "QM9"
]

class QM9:

    def __init__(self, qm9_data):
        if isinstance(qm9_data, str):
            qm9_data = self.load_qm9(qm9_data)
        self.qm9_data = qm9_data
        self._offsets = None

    @classmethod
    def build_qm9(cls, qm9_dir, pattern="*.xyz", target='qm9.npz'):
        all_natoms = []
        all_atoms = []
        all_confs = []
        all_smiles = []
        all_properties = []
        all_tags = []
        all_indices = []
        all_freqs = []
        all_charges = []

        for n, f in enumerate(glob.glob(os.path.join(qm9_dir, pattern))):
            xyz_data = dev.read_file(f).strip().replace("*^", "e")
            nlines, comment, xyz_data = xyz_data.split("\n", 2)
            xyz_data, freqs, smi, inchi = xyz_data.rsplit("\n", 3)
            _, smi = smi.split(maxsplit=1)
            all_smiles.append(smi.strip())
            coords = np.loadtxt(io.StringIO(xyz_data), usecols=[1, 2, 3, 4])
            atoms = np.loadtxt(io.StringIO(xyz_data), usecols=[0], dtype=str)
            all_atoms.append(atoms)
            all_natoms.append(len(coords))
            all_confs.append(coords[:, :3])
            all_charges.append(coords[:, 3])
            freqs = np.loadtxt(io.StringIO(freqs))
            all_freqs.append(freqs)
            gdb_idx, index, props = comment.split(maxsplit=2)
            all_tags.append(gdb_idx)
            all_indices.append(int(index))
            props = np.loadtxt(io.StringIO(props))
            all_properties.append(props)
            # if n > 2:
            #     break

        flat_charges = np.concatenate(all_charges)
        flat_coords = np.concatenate(all_confs, axis=0)
        flat_freqs = np.concatenate(all_freqs)
        flat_props = np.array(all_properties)
        flat_tags = np.array(all_tags)
        flat_inds = np.array(all_indices)
        flat_atoms = np.concatenate(all_atoms)
        flat_smiles = np.array(all_smiles)
        # flat_natoms = np.array(all_natoms)
        np.savez(
            target,
            offsets=np.concatenate([[0], np.cumsum(all_natoms[:-1])]),
            sizes=all_natoms,
            tags=flat_tags,
            indices=flat_inds,
            smiles=flat_smiles,
            atoms=flat_atoms,
            coords=flat_coords,
            charges=flat_charges,
            props=flat_props,
            freqs=flat_freqs
        )
        return target

    @classmethod
    def load_qm9(cls, qm9_file):
        # just memmapped numpy loading
        return np.load(qm9_file, mmap_mode="r")

    def smiles_query(self, pattern, start_at=0, upto=None, track_failures=False, quiet=True, **parser_options):
        if quiet:
            from rdkit.rdBase import BlockLogs
            with BlockLogs():
                return self.smiles_query(pattern,
                                         start_at=start_at, upto=upto,
                                         track_failures=track_failures,
                                         quiet=False,
                                         **parser_options)
        smi_data = self.qm9_data['smiles']
        matcher = SMILES.smarts_matcher(pattern, error_value=False, **parser_options)
        if upto is None:
            upto = len(smi_data)
        if track_failures:
            hits = []
            failures = []
            for i in range(start_at, upto):
                m = matcher(smi_data[i])
                if m is False:
                    failures.append(i)
                elif m:
                    hits.append(i)
            return hits, failures
        else:
            hits = []
            for i in range(start_at, upto):
                if matcher(smi_data[i]):
                    hits.append(i)
            return hits

    property_array_keys = ['A', 'B', 'C', 'mu', 'alpha', 'eps_HOMO', 'eps_LUMO', 'eps_gap', 'R2', 'zpve', 'U0', 'U', 'H', 'G', 'Cv']
    def _load_from_offsets(self, index, offset, size, props):
        results = {}
        for key in props:
            if key in ['atoms', 'coords']:
                val = self.qm9_data[key][offset:offset + size]
            elif key == 'freqs':
                o = 3*offset - 6 * index
                val = self.qm9_data[key][o:o + 3*size - 6]
            elif key == 'property_array':
                val = self.qm9_data["props"][index]
                val = dict(zip(self.property_array_keys, val))
            elif key == 'mol':
                val = RDMolecule.parse_smiles(self.qm9_data["smiles"][index])
            else:
                val = self.qm9_data[key][index]
            results[key] = val
        return results
    def load_data(self, index, props=None):
        if props is None:
            props = [
                "smiles",
                "atoms",
                "coords",
                "freqs",
                "property_array"
            ]
        offset = self.qm9_data['offsets'][index]
        size = self.qm9_data['sizes'][index]

        return self._load_from_offsets(index, offset, size, props)
    def data_iter(self, props=None, start_at=None, upto=None):
        if props is None:
            props = [
                "smiles",
                "atoms",
                "coords",
                "freqs",
                "property_array"
            ]
        offset = self.qm9_data['offsets']
        size = self.qm9_data['sizes']
        if start_at is not None:
            if upto is not None:
                offset = offset[start_at:upto]
            else:
                offset = offset[start_at:]
        elif upto is not None:
            offset = offset[start_at:upto]

        if start_at is None:
            start_at = 0

        for i,(o,s) in enumerate(zip(offset,size)):
             i = start_at + i
             yield self._load_from_offsets(i, o, s, props)


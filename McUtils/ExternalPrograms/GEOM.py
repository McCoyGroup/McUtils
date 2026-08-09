from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Iterator, Optional, Union

import shutil
import subprocess
import sys
import tarfile
import zipfile
from urllib.parse import urlencode
import numpy as np
import os

from .. import Devutils as dev
from .. import Iterators as itut
from .. import Numputils as nput
from .RDKit import RDMolecule

__all__ = [
    "GEOMLoader",
    "GEOMDownloader",
    "GEOMInternalsWrapper"
]

_GZIP_MAGIC = b"\x1f\x8b"

def _detect_tar_compression(path: Path) -> Optional[str]:
    """
    Return "gz" if the file is gzip-compressed (checked via magic bytes,
    not extension), "plain" if it's an uncompressed tar, or None if it's
    neither (e.g. a directory, or not a tar at all).
    """
    if not path.is_file():
        return None
    with open(path, "rb") as f:
        magic = f.read(2)
    if magic == _GZIP_MAGIC:
        return "gz"
    if tarfile.is_tarfile(path):
        return "plain"
    return None

class GEOMLoader:

    def __init__(
            self,
            root: Union[str, Path],
            subset: str,
            summary_path: str = "summary_dic.json",
            jump_index_path: Optional[Union[str, Path]] = None,
    ):
        self.root = Path(root)
        self.subset = subset
        self.summary_path = summary_path

        self.summary: Optional[dict] = None
        self._pickle_paths: Optional[list[str]] = None  # index -> relpath, once known
        self._tar_handle: Optional[tarfile.TarFile] = None
        self._member_index: list[tarfile.TarInfo] = []  # fallback tar-order index (lazy)
        self._member_by_relpath: dict[str, tarfile.TarInfo] = {}  # name-keyed cache (lazy)
        self._offset_by_relpath: dict[str, int] = {}  # precompiled name -> header-offset, if loaded
        self._offset_keys = None
        self._tar_exhausted = False  # True once we've hit EOF scanning
        self._summary_search_done = False  # True once we've looked for summary in tar

        self.tar_compression = _detect_tar_compression(self.root)  # "gz" | "plain" | None
        self.is_tar = self.tar_compression is not None

        if self.is_tar:
            if not self.root.exists():
                raise FileNotFoundError(f"Could not find archive {self.root}")
            if self.tar_compression == "plain":
                # Open the handle only — do NOT call getmembers()/getnames(),
                # since those force a full scan. Everything else is built on
                # demand, on first actual use.
                self._tar_handle = tarfile.open(self.root, "r")
                if jump_index_path is not None:
                    self._load_jump_indices(jump_index_path)
            # gz mode: nothing to build eagerly; streaming only.
        else:
            summary_file = self.root / summary_path
            if not summary_file.exists():
                raise FileNotFoundError(f"Could not find {summary_file}")
            with open(summary_file) as f:
                self.summary = json.load(f)  # {smiles: {"pickle_path": ..., ...}}
            self._pickle_paths = [
                meta["pickle_path"]
                for meta in self.summary.values()
                if meta.get("pickle_path")
            ]

    # ------------------------------------------------------------------
    # Tail-path helper: tar entries carry a leading top-level directory
    # (e.g. "rdkit_folder/drugs/x.pickle") that summary pickle_paths don't
    # (e.g. "drugs/x.pickle"). Strip it so the two can be matched by name.
    # ------------------------------------------------------------------

    @staticmethod
    def _tail_relpath(name: str) -> str:
        parts = name.split("/")
        return "/".join(parts[1:]) if len(parts) > 1 else name

    # ------------------------------------------------------------------
    # Preferred lazy path: locate summary_{subset}.json *inside* the tar
    # itself and use its pickle_path list as the index -> file mapping,
    # exactly like directory mode. Any .pickle members passed while
    # scanning for the summary get cached too, so that work isn't wasted
    # even if the summary turns out to be near the end (or absent).
    # ------------------------------------------------------------------
    def _try_load_summary_from_tar(self) -> bool:
        if self._summary_search_done:
            return self.summary is not None

        while not self._tar_exhausted:
            member = self._tar_handle.next()
            if member is None:
                self._tar_exhausted = True
                break
            if not member.isfile():
                continue

            tail = self._tail_relpath(member.name)
            if tail.endswith(".pickle"):
                self._member_by_relpath[tail] = member
                # Also keep the tar-order fallback index warm in case the
                # summary search comes up empty.
                if self._matches_subset(member):
                    self._member_index.append(member)
                continue

            if tail == self.summary_path or member.name.endswith(self.summary_path):
                fileobj = self._tar_handle.extractfile(member)
                self.summary = json.loads(fileobj.read())
                self._pickle_paths = [
                    meta["pickle_path"]
                    for meta in self.summary.values()
                    if meta.get("pickle_path")
                ]
                self._summary_search_done = True
                return True

        self._summary_search_done = True
        return False

    # ------------------------------------------------------------------
    # Precompiled jump index: name -> tar header offset, persisted as a
    # compressed .npz so future runs skip the scan entirely for any path
    # already recorded. See compile_jump_indices() to build one.
    # ------------------------------------------------------------------
    def _load_jump_indices(self, path: Union[str, Path]) -> None:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Jump index file not found: {path}")
        data = np.load(path, allow_pickle=False, mmap_mode='r')
        keys = data["keys"]
        offsets = data["offsets"]
        self._offset_by_relpath = {
            str(k): int(o) for k, o in zip(keys, offsets)
            if k[:len(self.subset)] == self.subset
        }
        self._offset_keys = list(self._offset_by_relpath.keys())
        # print(f"Loaded {len(self._offset_by_relpath)} cached jump offsets from {path}")

    def _read_member_at_offset(self, offset: int) -> Optional[tarfile.TarInfo]:
        """Parse a single tar header at a previously recorded byte offset —
        one seek + one 512-byte header read, no scanning."""
        try:
            self._tar_handle.fileobj.seek(offset)
            self._tar_handle.offset = offset
            return tarfile.TarInfo.fromtarfile(self._tar_handle)
        except tarfile.TarError:
            return None

    def compile_jump_indices(self, out_path: Union[str, Path] = "geom_jump_indices.npz") -> Path:
        """
        Fully scan the archive once (every *.pickle, any subset), recording
        each member's tar header offset, and save the name -> offset
        mapping as a compressed .npz with arrays "keys" and "offsets".
        Pass the resulting file back in as `jump_index_path` on a future
        GEOMLoader(...) call to skip scanning for any path it covers.
        """
        if not (self.is_tar and self.tar_compression == "plain"):
            raise RuntimeError(
                "compile_jump_indices() requires an uncompressed tar archive: "
                "gzip has no reusable random-access offsets, and directory "
                "mode doesn't need an index (files are already addressable "
                "by path)."
            )

        while not self._tar_exhausted:
            member = self._tar_handle.next()
            if member is None:
                self._tar_exhausted = True
                break
            if member.isfile() and member.name.endswith(".pickle"):
                tail = self._tail_relpath(member.name)
                self._member_by_relpath[tail] = member
                if self._matches_subset(member):
                    self._member_index.append(member)

        keys = np.array(list(self._member_by_relpath.keys()))
        offsets = np.array(
            [m.offset for m in self._member_by_relpath.values()], dtype=np.int64
        )

        out_path = Path(out_path)
        np.savez(out_path, keys=keys, offsets=offsets)
        # print(f"Wrote jump index with {len(keys)} entries -> {out_path}")
        return out_path

    def _find_member_by_relpath(self, rel_path: str) -> tarfile.TarInfo:
        """Locate a specific pickle by its summary-relative path.

        Resolution order:
          1. Already-cached TarInfo (from any prior scan or jump lookup).
          2. A precompiled offset from a loaded jump index -> single seek
             + single header parse, no scanning at all.
          3. Fall back to scanning forward, caching everything passed.
        """
        if rel_path in self._member_by_relpath:
            return self._member_by_relpath[rel_path]

        if rel_path in self._offset_by_relpath:
            offset = self._offset_by_relpath[rel_path]
            member = self._read_member_at_offset(offset)
            if member is not None and self._tail_relpath(member.name) == rel_path:
                self._member_by_relpath[rel_path] = member
                return member
            # Stale/mismatched index entry (archive changed since the index
            # was built) — fall through to a normal scan instead of trusting it.

        while not self._tar_exhausted:
            member = self._tar_handle.next()
            if member is None:
                self._tar_exhausted = True
                break
            if not member.isfile():
                continue
            tail = self._tail_relpath(member.name)
            if tail.endswith(".pickle"):
                self._member_by_relpath[tail] = member
                if self._matches_subset(member):
                    self._member_index.append(member)
                if tail == rel_path:
                    return member

        raise KeyError(f"Could not find pickle for '{rel_path}' in archive (exhausted).")

    # ------------------------------------------------------------------
    # Fallback lazy index construction (used only if no summary was found
    # inside the tar): scan by subset-directory naming instead of by exact
    # relative path.
    #
    # tarfile.TarFile.next() reads exactly one header, advances the file
    # position past that member's data (a seek, not a read, for
    # uncompressed tars), and appends the TarInfo to tf.members as a side
    # effect. getmembers()/getnames() just loop next() until EOF — we do
    # the same loop ourselves, but stop as soon as we've found enough
    # matching (*.pickle, right subset) members to satisfy the current
    # request, so a request for index 0 doesn't pay for scanning the
    # whole archive.
    # ------------------------------------------------------------------
    def _matches_subset(self, member: tarfile.TarInfo) -> bool:
        subset_marker = f"/{self.subset}/"
        return member.isfile() and member.name.endswith(".pickle") and (
                subset_marker in f"/{member.name}"
        )

    def _extend_index_until(self, min_count: int) -> None:
        """Scan forward only as far as needed to have >= min_count matches cached."""
        while len(self._member_index) < min_count and not self._tar_exhausted:
            member = self._tar_handle.next()
            if member is None:
                self._tar_exhausted = True
                break
            if self._matches_subset(member):
                self._member_index.append(member)
                self._member_by_relpath[self._tail_relpath(member.name)] = member

    def _ensure_fully_indexed(self) -> None:
        """Finish scanning the archive. Only pay this cost when truly needed."""
        while not self._tar_exhausted:
            member = self._tar_handle.next()
            if member is None:
                self._tar_exhausted = True
                break
            if self._matches_subset(member):
                self._member_index.append(member)
                self._member_by_relpath[self._tail_relpath(member.name)] = member

    def supports_random_access(self) -> bool:
        return not (self.is_tar and self.tar_compression == "gz")

    def __len__(self) -> int:
        if not self.supports_random_access():
            raise RuntimeError(
                "Length is unknown for gzip-compressed tar archives "
                "(no member index available; use iter_geom_records() instead)."
            )
        if self.is_tar:
            if len(self._offset_by_relpath) > 0:
                return len(self._offset_by_relpath)
            self._try_load_summary_from_tar()
            if self._pickle_paths is not None:
                return len(self._pickle_paths)  # known instantly from summary, no scan needed
            # No summary found anywhere in the archive — length isn't
            # knowable without finishing the scan at least once.
            self._ensure_fully_indexed()
            return len(self._member_index)
        return len(self._pickle_paths)

    # ------------------------------------------------------------------
    # Shared per-molecule -> per-conformer expansion with optional bond fixing
    # ------------------------------------------------------------------
    @classmethod
    def _get_tagged_bond_types(cls, mol):
        a = mol.atoms
        b = mol.bonds
        return itut.counts(tuple(sorted((a[i], a[j]))) for i, j, _ in b)

    @classmethod
    def _bond_type_differences(cls, mol1, mol2):
        c1 = cls._get_tagged_bond_types(mol1)
        c2 = cls._get_tagged_bond_types(mol2)
        diffs = {
            k: (c1.get(k, 0) - c2.get(k, 0))
            for k in c1.keys()
        }
        return {k: v for k, v in diffs.items() if v != 0}

    @classmethod
    def _find_bond_fixes(cls, mol1, mol2, allow_bond_formation=False):
        diffs = cls._bond_type_differences(mol1, mol2)
        coords2 = mol2.coords
        atom_map = itut.index_groups(mol2.atoms)
        bonds = [b[:2] for b in mol2.bonds]
        new_bonds = []
        dm = nput.distance_matrix(coords2)
        for ti, tj in bonds:
            dm[ti, tj] = dm[tj, ti] = 1000000
        np.fill_diagonal(dm, 1000000)
        for (t1, t2), deficit in diffs.items():
            if deficit < 0:
                if allow_bond_formation:
                    continue
                else:
                    raise ValueError("need to handle bond formation")
            for _ in range(deficit):
                new_pair = cls._find_replacement_candidates(atom_map, dm, t1, t2)
                new_bonds.append(new_pair)
                ii, jj = new_pair
                dm[ii, jj] = 1000000
                dm[jj, ii] = 1000000
        return new_bonds

    @classmethod
    def _find_replacement_candidates(cls, atom_map, dm, t1, t2):
        i = atom_map[t1]
        j = atom_map[t2]
        dm = dm[np.ix_(i, j)]
        min_pos = np.argmin(dm)
        ri, rj = np.unravel_index(min_pos, dm.shape)
        return i[ri], j[rj]

    @classmethod
    def _patch_bonds(cls, mol1, mol2, allow_bond_formation=False):
        patch_check = mol1.to_smiles(remove_hydrogens=True)
        ref_check = mol2.to_smiles(remove_hydrogens=True)
        if ref_check != patch_check:
            new_bonds = cls._find_bond_fixes(mol1, mol2, allow_bond_formation=allow_bond_formation)
            if len(new_bonds) > 0:
                mol_new = mol2.add_bonds(new_bonds,
                                         sanitize=False,
                                         adjust_charges=True,
                                         reguess_bonds=False)
            else:
                mol_new = mol2
            patch_check = mol_new.to_smiles(remove_hydrogens=True, compute_stereo=True)
            return mol_new, ref_check == patch_check, (ref_check, patch_check)
        else:
            return mol2, True, (ref_check, patch_check)

    class MolStub:
        def __init__(self, rdmol):
            self.mol = rdmol
            self.atoms = [atom.GetSymbol() for atom in rdmol.GetAtoms()]
            self.bonds = RDMolecule.get_bonds(rdmol)
        def to_smiles(self, remove_hydrogens=False, canonical=False):
            import rdkit.Chem.AllChem as Chem
            mol = self.mol
            if remove_hydrogens:
                mol = Chem.Mol(mol)
            return Chem.MolToSmiles(mol, canonical=canonical)

    CHECK_LOADED_BONDS = 'broken'
    PERMUTE_ATOMS = None
    @classmethod
    def _load_rdmol(cls, mol, meta, check=None, permute=None):
        import rdkit.Chem.AllChem as Chem
        mol0 = RDMolecule.parse_smiles(meta['smiles'], add_implicit_hydrogens=False, sanitize=False)
        mol2 = RDMolecule.from_rdmol(mol, charge=Chem.GetFormalCharge(mol0))
        if check is None:
            check = cls.CHECK_LOADED_BONDS
        if permute is None:
            permute = cls.PERMUTE_ATOMS
            if permute is None:
                permute = check
        if check:
            # TODO: handle patches properly
            mol2, _, _ = cls._patch_bonds(cls.MolStub(mol0), mol2,
                                          allow_bond_formation=dev.str_is(check, 'broken'))
        if permute:
            _, canonical_order = mol2.to_smiles(remove_hydrogens=False, return_reordering=True)
            mol2 = mol2.permute(canonical_order)

        return mol2, meta

    @classmethod
    def _expand_molecule(
            cls,
            mol_dict: dict,
            fallback_smiles: str,
            pickle_rel_path: str,
            max_confs_per_mol: Optional[int]
    ) -> Iterator[tuple[RDMolecule, dict]]:
        confs = mol_dict.get("conformers", [])
        if max_confs_per_mol is not None:
            confs = confs[:max_confs_per_mol]

        resolved_smiles = mol_dict.get("smiles", fallback_smiles)

        for conf_idx, conf in enumerate(confs):
            rd_mol = conf["rd_mol"]

            meta = {
                "smiles": resolved_smiles,
                "pickle_path": pickle_rel_path,
                "conformer_index": conf_idx,
                "total_energy": conf.get("totalenergy"),
                "boltzmann_weight": conf.get("boltzmannweight"),
            }

            yield cls._load_rdmol(rd_mol, meta)

    # ------------------------------------------------------------------
    # Random access (directory mode + plain/uncompressed tar mode)
    # ------------------------------------------------------------------
    USE_OFFSET_INDEX = True
    def _load_mol_dict_by_index(self, index: int | str) -> tuple[dict, str]:
        """Return (mol_dict, path_string) for molecule `index`."""
        if not self.supports_random_access():
            raise RuntimeError(
                "Random access isn't supported for gzip-compressed tar "
                "archives (gzip has no member index). Use "
                "iter_geom_records() for a single forward pass instead."
            )

        if self.is_tar:  # plain/uncompressed tar
            if isinstance(index, str):
                rel_path = index
            else:
                rel_path = None
                if self.USE_OFFSET_INDEX and len(self._offset_by_relpath) > 0:
                    if index >= len(self._offset_by_relpath):
                        raise IndexError(
                            f"Index {index} out of range: jump table lists "
                            f"{len(self._offset_by_relpath)} molecule(s)."
                        )
                    rel_path = self._offset_keys[index]

                if rel_path is None:
                    self._try_load_summary_from_tar()
                    if self._pickle_paths is not None:
                        # Summary was found in the archive: index means exactly what
                        # it means in directory mode — position in the summary's
                        # pickle_path list. Look the file up by its known name.
                        if index >= len(self._pickle_paths):
                            raise IndexError(
                                f"Index {index} out of range: summary lists "
                                f"{len(self._pickle_paths)} molecule(s)."
                            )
                        rel_path = self._pickle_paths[index]

            if rel_path is not None:
                member = self._find_member_by_relpath(rel_path)
                fileobj = self._tar_handle.extractfile(member)
                mol_dict = pickle.loads(fileobj.read())
                return mol_dict, rel_path

            # Fallback: no summary in the archive — index means position in
            # tar storage order among files matching the subset directory.
            self._extend_index_until(index + 1)
            if index >= len(self._member_index):
                raise IndexError(
                    f"Index {index} out of range: archive only contains "
                    f"{len(self._member_index)} matching molecule(s)."
                )
            member = self._member_index[index]
            fileobj = self._tar_handle.extractfile(member)
            mol_dict = pickle.loads(fileobj.read())
            return mol_dict, member.name
        else:  # extracted directory
            rel_path = self._pickle_paths[index] if not isinstance(index, str) else index
            with open(self.root / rel_path, "rb") as f:
                mol_dict = pickle.load(f)
            return mol_dict, rel_path

    def get_molecule_records(
            self,
            index: int | str,
            max_confs_per_mol: Optional[int] = None,
            create_mols = True
    ) -> list[tuple[RDMolecule, dict]]:
        """Return every (record, meta) conformer pair for molecule `index`."""
        mol_dict, path_str = self._load_mol_dict_by_index(index)
        if create_mols:
            return list(
                self._expand_molecule(
                    mol_dict,
                    mol_dict.get("smiles", "<unknown>"),
                    path_str,
                    max_confs_per_mol
                )
            )
        else:
            return [(None, mol_dict)]

    def get_record(
            self,
            index: int,
            conformer_index: int = 0,
            create_mols: bool = True
    ) -> tuple[RDMolecule, dict]:
        """Return a single (record, meta) for molecule `index`, conformer `conformer_index`."""
        records = self.get_molecule_records(
            index, max_confs_per_mol=conformer_index + 1,
            create_mols=create_mols
        )
        if conformer_index >= len(records):
            raise IndexError(
                f"Molecule {index} has only {len(records)} conformer(s); "
                f"requested conformer_index={conformer_index}"
            )
        return records[conformer_index]

    def __getitem__(self, index: int) -> tuple:
        return self.get_record(index)

    # ------------------------------------------------------------------
    # Sequential iteration (all modes)
    # ------------------------------------------------------------------
    def _iter_from_directory(
            self,
            max_mols: Optional[int],
            max_confs_per_mol: Optional[int],
            create_mols: bool = True
    ) -> Iterator[tuple[RDMolecule, dict]]:
        n_mols = 0
        for rel_path in self._pickle_paths:
            pickle_path = self.root / rel_path
            if not pickle_path.exists():
                continue
            with open(pickle_path, "rb") as f:
                mol_dict = pickle.load(f)

            if create_mols:
                yield from self._expand_molecule(
                    mol_dict, mol_dict.get("smiles", "<unknown>"), rel_path,
                    max_confs_per_mol,
                )
            else:
                yield (None, mol_dict)

            del mol_dict

            n_mols += 1
            if max_mols is not None and n_mols >= max_mols:
                return

    def _iter_from_plain_tar(
            self,
            max_mols: Optional[int],
            max_confs_per_mol: Optional[int],
            create_mols: bool = True
    ) -> Iterator[tuple[RDMolecule, dict]]:
        if len(self._offset_by_relpath) > 0:
            n_mols = 0
            for rel_path in self._offset_keys:

                try:
                    member = self._find_member_by_relpath(rel_path)
                except KeyError:
                    continue  # listed in summary but not present in this archive
                fileobj = self._tar_handle.extractfile(member)
                mol_dict = pickle.loads(fileobj.read())

                if create_mols:
                    yield from self._expand_molecule(
                        mol_dict, mol_dict.get("smiles", "<unknown>"), rel_path,
                        max_confs_per_mol,
                    )
                else:
                    yield (None, mol_dict)

                del mol_dict

                n_mols += 1
                if max_mols is not None and n_mols >= max_mols:
                    return
            return
        else:
            self._try_load_summary_from_tar()
            if self._pickle_paths is not None:
                # Follow summary order (same as directory mode), looking each
                # relpath up lazily — reuses whatever's cached, extends as needed.
                n_mols = 0
                for rel_path in self._pickle_paths:
                    try:
                        member = self._find_member_by_relpath(rel_path)
                    except KeyError:
                        continue  # listed in summary but not present in this archive
                    fileobj = self._tar_handle.extractfile(member)
                    mol_dict = pickle.loads(fileobj.read())

                    if create_mols:
                        yield from self._expand_molecule(
                            mol_dict, mol_dict.get("smiles", "<unknown>"), rel_path,
                            max_confs_per_mol,
                        )
                    else:
                        yield (None, mol_dict)
                    del mol_dict

                    n_mols += 1
                    if max_mols is not None and n_mols >= max_mols:
                        return
                return

        # Interleave scanning with consumption: extend the cached index one
        # slot at a time rather than requiring it be fully built up front.
        # This reuses whatever's already cached from prior random access,
        # and in turn leaves the cache populated for random access after.
        n_mols = 0
        idx = 0
        while True:
            self._extend_index_until(idx + 1)

            member = self._member_index[idx]
            fileobj = self._tar_handle.extractfile(member)
            mol_dict = pickle.loads(fileobj.read())

            if create_mols:
                yield from self._expand_molecule(
                    mol_dict, mol_dict.get("smiles", "<unknown>"), member.name,
                    max_confs_per_mol,
                )
            else:
                yield (None, mol_dict)
            del mol_dict

            n_mols += 1
            if max_mols is not None and n_mols >= max_mols:
                return

    def _iter_from_gz_tar(
            self,
            max_mols: Optional[int],
            max_confs_per_mol: Optional[int],
            create_mols: bool = True
    ) -> Iterator[tuple[RDMolecule, dict]]:
        subset_marker = f"/{self.subset}/"
        n_mols = 0

        # "r|gz" = streaming mode: forward-only single pass, no member
        # index is built, nothing is written to disk.
        with tarfile.open(self.root, "r|gz") as tf:
            for member in tf:
                if not member.isfile() or not member.name.endswith(".pickle"):
                    continue
                if subset_marker not in f"/{member.name}":
                    continue

                fileobj = tf.extractfile(member)
                if fileobj is None:
                    continue
                mol_dict = pickle.loads(fileobj.read())

                if create_mols:
                    yield from self._expand_molecule(
                        mol_dict, mol_dict.get("smiles", "<unknown>"), member.name,
                        max_confs_per_mol,
                    )
                else:
                    yield (None, mol_dict)
                del mol_dict

                n_mols += 1
                if max_mols is not None and n_mols >= max_mols:
                    return

    def iter_geom_records(
            self,
            max_mols: Optional[int] = None,
            max_confs_per_mol: Optional[int] = None,
            create_mols: bool = True
    ) -> Iterator[tuple[RDMolecule, dict]]:
        """
        Yield (record, meta) pairs, one per conformer, in whatever order the
        underlying storage returns molecules.

        record:
            - if return_mols=False: (smiles, coords), coords an
              (n_atoms, 3) float64 numpy array of Angstrom coordinates.
            - if return_mols=True: the RDKit Chem.Mol for that conformer.

        meta:
            dict with smiles, pickle_path, conformer_index, n_atoms,
            atomic_numbers, total_energy, boltzmann_weight.

        Gzip-tar mode is a strict single forward pass: re-decompresses
        from the start on every call. Directory and plain-tar modes are
        cheap to call repeatedly.
        """
        if self.is_tar and self.tar_compression == "gz":
            yield from self._iter_from_gz_tar(max_mols, max_confs_per_mol, create_mols=create_mols)
        elif self.is_tar:  # plain/uncompressed
            yield from self._iter_from_plain_tar(max_mols, max_confs_per_mol, create_mols=create_mols)
        else:
            yield from self._iter_from_directory(max_mols, max_confs_per_mol, create_mols=create_mols)

    # ------------------------------------------------------------------
    def close(self) -> None:
        if self._tar_handle is not None:
            self._tar_handle.close()
            self._tar_handle = None

    def __enter__(self) -> "GEOMLoader":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

class GEOMDownloader:
    """
    Downloads and extracts the GEOM `rdkit_folder` archive.

    By default, fetches the whole dataset via its Dataverse persistentId
    (returned as a zip wrapping rdkit_folder.tar.gz, which is unwrapped
    automatically). If `file_id` is given, downloads that file directly
    instead (skips the wrapping zip step; known value for
    rdkit_folder.tar.gz is "4327252").

    from geom_downloader import GEOMDownloader

    downloader = GEOMDownloader(out_dir="./geom_data")
    extracted_dir = downloader.download()

    # or via direct file id, skipping the dataset-bundle zip:
    downloader = GEOMDownloader(out_dir="./geom_data", file_id="4327252")
    extracted_dir = downloader.download()
    """

    PERSISTENT_ID = "doi:10.7910/DVN/JNGTDF"
    SERVER_URL = "https://dataverse.harvard.edu"
    CHUNK_SIZE = 1024 * 1024  # 1 MB

    RDKIT_DATA_ID = 4327252

    def __init__(
        self,
        out_dir: str | Path,
        persistent_id: str = None,
        server_url: str = None,
        file_id: Optional[str] = None
    ):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        if persistent_id is None:
            persistent_id = self.PERSISTENT_ID
        self.persistent_id = persistent_id
        if server_url is None:
            server_url = self.SERVER_URL
        self.server_url = server_url
        self.file_id = file_id

    # ------------------------------------------------------------------
    # URL construction
    # ------------------------------------------------------------------
    def _build_download_url(self) -> tuple[str, Path]:
        """Return (full_url, dest_path) for either file-id or dataset mode."""
        if self.file_id:
            url = f"{self.server_url}/api/access/datafile/{self.file_id}"
            dest = self.out_dir / "rdkit_folder.tar.gz"
        else:
            params = urlencode({"persistentId": self.persistent_id})
            url = f"{self.server_url}/api/access/dataset/:persistentId/?{params}"
            dest = self.out_dir / "geom_dataset_bundle.zip"
        return url, dest

    # ------------------------------------------------------------------
    # Download strategies
    # ------------------------------------------------------------------
    def _try_cli_download(self, url: str, dest: Path) -> bool:
        """Attempt download via wget, then curl. Returns True on success."""
        if shutil.which("wget"):
            print(f"Downloading via wget: {url}")
            cmd = ["wget", "--continue", "-O", str(dest), url]
        elif shutil.which("curl"):
            print(f"Downloading via curl: {url}")
            cmd = ["curl", "-L", "-C", "-", "-o", str(dest), url]
        else:
            return False

        try:
            result = subprocess.run(cmd, check=False)
        except OSError as e:
            print(f"  CLI download tool errored: {e}")
            return False

        if result.returncode != 0:
            print(f"  CLI download failed (exit code {result.returncode})")
            return False

        if not dest.exists() or dest.stat().st_size == 0:
            print("  CLI download reported success but produced no data")
            return False

        return True

    def _chunked_download(self, url: str, dest: Path) -> Path:
        """Pure-Python streaming download fallback using requests."""
        import requests

        print(f"Falling back to chunked Python download: {url}")
        with requests.get(url, stream=True, timeout=60) as resp:
            resp.raise_for_status()
            total = int(resp.headers.get("content-length", 0))
            downloaded = 0

            with open(dest, "wb") as f:
                for chunk in resp.iter_content(chunk_size=self.CHUNK_SIZE):
                    if not chunk:
                        continue
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        pct = downloaded / total * 100
                        sys.stdout.write(
                            f"\r  downloading {dest.name}: "
                            f"{downloaded / 1e9:.2f} / {total / 1e9:.2f} GB ({pct:5.1f}%)"
                        )
                    else:
                        sys.stdout.write(
                            f"\r  downloading {dest.name}: {downloaded / 1e9:.2f} GB"
                        )
                    sys.stdout.flush()
        print()
        return dest

    def _fetch(self) -> Path:
        """Download the archive/bundle, trying CLI tools before falling back."""
        url, dest = self._build_download_url()

        if self._try_cli_download(url, dest):
            return dest

        print("Command-line download unavailable or failed; using fallback.")
        return self._chunked_download(url, dest)

    # ------------------------------------------------------------------
    # Post-processing
    # ------------------------------------------------------------------
    def _unwrap_bundle_zip(self, zip_path: Path) -> Path:
        """Extract rdkit_folder.tar.gz out of the dataset-level zip bundle."""
        print("Unwrapping dataset bundle zip...")
        with zipfile.ZipFile(zip_path) as zf:
            names = zf.namelist()
            tar_gz_names = [n for n in names if n.endswith(".tar.gz")]
            if not tar_gz_names:
                raise RuntimeError(
                    f"No .tar.gz found inside dataset bundle. Contents: {names}"
                )
            inner_name = tar_gz_names[0]
            extracted_path = self.out_dir / Path(inner_name).name
            with zf.open(inner_name) as src, open(extracted_path, "wb") as dst:
                shutil.copyfileobj(src, dst)

        zip_path.unlink()
        return extracted_path

    def _extract_tar_gz(self, tar_path: Path) -> Path:
        """Extract rdkit_folder.tar.gz, showing progress by member count."""
        print(f"Extracting {tar_path.name} -> {self.out_dir} ...")
        with tarfile.open(tar_path, "r") as tf:
            members = tf.getmembers()
            total = len(members)
            for i, member in enumerate(members, 1):
                tf.extract(member, path=self.out_dir)
                if i % 500 == 0 or i == total:
                    sys.stdout.write(f"\r  extracted {i}/{total} entries")
                    sys.stdout.flush()
        print()
        return self.out_dir / "rdkit_folder"

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------
    def download(
        self,
        keep_archive: bool = False,
        skip_download: bool = False,
    ) -> Path:
        """
        Download (unless skip_download) and extract the GEOM archive.

        Returns the path to the extracted `rdkit_folder` directory.
        """
        if skip_download:
            tar_path = self.out_dir / "rdkit_folder.tar.gz"
            if not tar_path.exists():
                raise FileNotFoundError(f"No archive found at {tar_path}")
        else:
            fetched = self._fetch()
            tar_path = (
                self._unwrap_bundle_zip(fetched)
                if fetched.suffix == ".zip"
                else fetched
            )

        extracted_dir = self._extract_tar_gz(tar_path)

        if not keep_archive:
            tar_path.unlink()
            print(f"Removed archive {tar_path.name}")

        print(f"\nDone. Data extracted to: {extracted_dir}")
        print("Expected contents: summary_drugs.json, summary_qm9.json, drugs/, qm9/")
        return extracted_dir

class GEOMInternalsWrapper:
    def __init__(self, loader, zdata, managed_store=None):
        self.loader = loader
        self.zdata = zdata
        self.managed_store = managed_store

        # cached, fully in-memory copies of small index/metadata arrays.
        # these are read constantly (once per chunk / per system lookup),
        # so paying for one zarr read up front avoids hundreds of tiny
        # random-access reads against the (zipped) store later.
        self._conformer_offsets = None
        self._system_identifiers = None
        self._conformer_identifiers = None
        self._system_offsets = None

    @classmethod
    def from_files(cls,
                    root=None,
                    geom_file='geom_dataset.tar.gz',
                    jump_index_path='geom_jump_indices.npz',
                    coords_zip='geom_coordinates.zip'):
        import zarr

        if root is not None:
            geom_file = os.path.join(root, geom_file)
            jump_index_path = os.path.join(root, jump_index_path)
            coords_zip = os.path.join(root, coords_zip)
        loader = GEOMLoader(geom_file, 'drugs', jump_index_path=jump_index_path)
        store = zarr.ZipStore(coords_zip, mode='r')
        zdata = zarr.open_group(store=store, path='combined.zarr', mode='r')
        return cls(loader, zdata, managed_store=store)

    def close(self):
        if self.managed_store is not None:
            self.managed_store.close()

    def __enter__(self):
        return self

    def __exit__(self, *exit_args):
        self.close()

    # ---- cached metadata ----------------------------------------------

    @property
    def conformer_offsets(self):
        if self._conformer_offsets is None:
            self._conformer_offsets = self.zdata['conformer_offsets'][:]
        return self._conformer_offsets

    @property
    def system_identifiers(self):
        if self._system_identifiers is None:
            self._system_identifiers = self.zdata['system_identifiers'][:]
        return self._system_identifiers

    @property
    def conformer_identifiers(self):
        if self._conformer_identifiers is None:
            self._conformer_identifiers = self.zdata['conformer_identifiers'][:]
        return self._conformer_identifiers

    def get_system_offsets(self):
        # includes a trailing sentinel (= total conformer count) so that
        # both start and end of any system are plain offs[i]/offs[i+1]
        # lookups, matching how conformer_offsets already works.
        if self._system_offsets is None:
            sysids = self.system_identifiers
            starts = np.concatenate([[0], np.where(np.diff(sysids) != 0)[0] + 1])
            self._system_offsets = np.concatenate([starts, [len(sysids)]])
        return self._system_offsets

    def system_offset(self, i, return_nconfs=True):
        offs = self.get_system_offsets()
        if return_nconfs:
            return offs[i], offs[i + 1] - offs[i]
        else:
            return offs[i]

    @property
    def total_conformers(self):
        return self.zdata['vals'].shape[0]

    @property
    def total_systems(self):
        return len(self.get_system_offsets()) - 1

    # ---- random sampling -------------------------------------------------

    def sample_conformers(self, n, replace=False, rng=None):
        """
        Uniformly sample `n` conformers at random from the whole dataset
        (systems with more conformers are proportionally more likely to
        contribute -- this is uniform over *conformers*, not systems;
        see sample_systems for the other kind of uniformity).

        Draws the indices, sorts them, then does a single vectorized
        fancy-index read across vals/types/tags. Each zarr chunk touched
        is decompressed once no matter how many sampled indices fall in
        it -- one request per chunk touched, not one per sample.
        """
        rng = np.random.default_rng() if rng is None else rng
        idx = rng.choice(self.total_conformers, size=n, replace=replace)
        idx.sort()  # improves chunk locality; doesn't bias the sample

        zdata = self.zdata
        data = {
            'vals': zdata['vals'][idx],
            'types': zdata['types'][idx],
            'tags': zdata['tags'][idx],
        }
        return idx, data

    def sample_systems(self, n, replace=False, rng=None,
                        load_confs=False, load_representative=True):
        """
        Uniformly sample `n` systems (molecules) at random, pulling all
        (or a representative) conformer(s) per system.

        All sampled systems' conformer ranges are flattened into a single
        index array up front, so there is exactly one fancy-index read
        across vals/types/tags for the entire sample -- not one read per
        system.
        """
        rng = np.random.default_rng() if rng is None else rng
        sys_idx = rng.choice(self.total_systems, size=n, replace=replace)
        sys_idx.sort()  # improves chunk locality

        offs = self.get_system_offsets()
        starts = offs[sys_idx]
        ends = offs[sys_idx + 1]
        conf_idx = np.concatenate([np.arange(s, e) for s, e in zip(starts, ends)])

        zdata = self.zdata
        data = {
            'vals': zdata['vals'][conf_idx],
            'types': zdata['types'][conf_idx],
            'tags': zdata['tags'][conf_idx],
        }

        if load_confs:
            mols = [self.load_conformer(k) for k in conf_idx]
            return sys_idx, mols, data
        elif load_representative:
            reps = [self.load_conformer(s) for s in starts]
            return sys_idx, reps, data
        else:
            return sys_idx, data

    # ---- bulk conformer reads -------------------------------------------

    @staticmethod
    def _is_int(i):
        return nput.is_int(i)

    @staticmethod
    def _contiguous_runs(idx):
        """Group a (possibly non-contiguous) list of indices into
        maximal contiguous runs, e.g. [0,1,2,5,6,9] -> [(0,2),(5,6),(9,9)]."""
        idx = list(idx)
        if not idx:
            return []
        runs = []
        run_start = prev = idx[0]
        for x in idx[1:]:
            if x != prev + 1:
                runs.append((run_start, prev))
                run_start = x
            prev = x
        runs.append((run_start, prev))
        return runs

    def _read_conformer_range(self, start, end):
        """Single bulk read of vals/types/tags over a contiguous
        conformer index range [start, end)."""
        offsets = self.conformer_offsets
        lo, hi = offsets[start], offsets[end]
        zdata = self.zdata
        return {
            'vals': zdata['vals'][lo:hi],
            'types': zdata['types'][lo:hi],
            'tags': zdata['tags'][lo:hi],
        }

    def load_chunk(self, i):
        """Load conformer data for a single index, a contiguous range,
        or an arbitrary iterable of indices. Contiguous spans are always
        collapsed into one zarr read instead of one-per-index."""
        if self._is_int(i):
            return self._read_conformer_range(i, i + 1)

        # range objects and sorted contiguous lists both resolve to one read
        if isinstance(i, range) and (i.step == 1 or i.step is None):
            if len(i) == 0:
                return self._read_conformer_range(0, 0)
            return self._read_conformer_range(i.start, i.stop)

        runs = self._contiguous_runs(i)
        if not runs:
            return self._read_conformer_range(0, 0)
        if len(runs) == 1:
            start, end = runs[0]
            return self._read_conformer_range(start, end + 1)

        # non-contiguous: still only one read per contiguous run,
        # not one per index
        parts = [self._read_conformer_range(a, b + 1) for a, b in runs]
        keys = parts[0].keys()
        return {k: np.concatenate([p[k] for p in parts], axis=0) for k in keys}

    def load_conformer(self, i):
        return self.loader.get_record(
            self.system_identifiers[i],
            self.conformer_identifiers[i]
        )

    # ---- system-level access -------------------------------------------

    def load_system_chunks(self, i, load_confs=False, load_representative=True):
        if self._is_int(i):
            offset, nrec = self.system_offset(i, return_nconfs=True)
            data = self.load_chunk(range(offset, offset + nrec))
            if load_confs:
                mols = [self.load_conformer(k) for k in range(offset, offset + nrec)]
                return mols, data
            elif load_representative:
                return self.load_conformer(offset), data
            else:
                return data

        idx = list(i)
        if not idx:
            return ([], {}) if load_confs or load_representative else {}

        runs = self._contiguous_runs(idx)

        # fast path: one contiguous span of systems -> exactly one
        # bulk conformer read for the whole span, regardless of how
        # many systems it covers
        if len(runs) == 1:
            start_sys, end_sys = runs[0]
            conf_start = self.system_offset(start_sys, return_nconfs=False)
            conf_end_start, end_nconfs = self.system_offset(end_sys, return_nconfs=True)
            conf_end = conf_end_start + end_nconfs
            data = self.load_chunk(range(conf_start, conf_end))

            if load_confs:
                mols = [self.load_conformer(k) for k in range(conf_start, conf_end)]
                return mols, data
            elif load_representative:
                reps = [self.load_conformer(self.system_offset(s, return_nconfs=False))
                        for s in range(start_sys, end_sys + 1)]
                return reps, data
            else:
                return data

        # fallback: multiple disjoint spans of systems -> one bulk
        # read per span (still far fewer reads than per-system/per-conformer)
        results = [
            self.load_system_chunks(range(a, b + 1), load_confs=load_confs,
                                     load_representative=load_representative)
            for a, b in runs
        ]
        if load_confs or load_representative:
            systems, datas = zip(*results)
            merged_systems = [s for group in systems for s in group]
        else:
            datas = results
            merged_systems = None

        keys = datas[0].keys()
        merged_data = {k: np.concatenate([d[k] for d in datas], axis=0) for k in keys}
        return (merged_systems, merged_data) if merged_systems is not None else merged_data

    def get_internals(self, mol):
        from Psience.Molecools import Molecule  # get this out of here
        return Molecule.from_rdmol(mol).get_bond_graph_internals(include_fragments=False)

    def block_iter(self):
        tags = self.zdata['tags']
        types = self.zdata['types']
        vals = self.zdata['vals']
        for t, y, v in zip(tags.blocks, types.blocks, vals.blocks):
            yield {'tags': t, 'types': y, 'vals': v}

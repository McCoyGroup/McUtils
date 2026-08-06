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

from .RDKit import RDMolecule

__all__ = [
    "GEOMLoader",
    "GEOMDownloader"
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
    ):
        self.root = Path(root)
        self.subset = subset
        self.summary_path = summary_path

        self.summary: Optional[dict] = None
        self._pickle_paths: Optional[list[str]] = None   # directory mode index
        self._tar_handle: Optional[tarfile.TarFile] = None
        self._member_index: list[tarfile.TarInfo] = []   # plain-tar mode index, built lazily
        self._tar_exhausted = False                        # True once we've hit EOF scanning

        self.tar_compression = _detect_tar_compression(self.root)  # "gz" | "plain" | None
        self.is_tar = self.tar_compression is not None

        if self.is_tar:
            if not self.root.exists():
                raise FileNotFoundError(f"Could not find archive {self.root}")
            if self.tar_compression == "plain":
                # Open the handle only — do NOT call getmembers()/getnames(),
                # since those force a full scan. Index is built on demand
                # by _extend_index_until() / _ensure_fully_indexed().
                self._tar_handle = tarfile.open(self.root, "r")
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
    # Lazy index construction (plain/uncompressed tar only)
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

    def _ensure_fully_indexed(self) -> None:
        """Finish scanning the archive. Only pay this cost when truly needed (e.g. len())."""
        while not self._tar_exhausted:
            member = self._tar_handle.next()
            if member is None:
                self._tar_exhausted = True
                break
            if self._matches_subset(member):
                self._member_index.append(member)

    def supports_random_access(self) -> bool:
        return not (self.is_tar and self.tar_compression == "gz")

    def __len__(self) -> int:
        if not self.supports_random_access():
            raise RuntimeError(
                "Length is unknown for gzip-compressed tar archives "
                "(no member index available; use iter_geom_records() instead)."
            )
        if self.is_tar:
            # Length isn't knowable without finishing the scan at least once.
            # Cheap if already exhausted by prior access; otherwise this is
            # the one place laziness can't help.
            self._ensure_fully_indexed()
            return len(self._member_index)
        return len(self._pickle_paths)

    # ------------------------------------------------------------------
    # Shared per-molecule -> per-conformer expansion
    # ------------------------------------------------------------------
    @staticmethod
    def _expand_molecule(
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

            yield RDMolecule.from_rdmol(rd_mol, conf_id=None), meta

    # ------------------------------------------------------------------
    # Random access (directory mode + plain/uncompressed tar mode)
    # ------------------------------------------------------------------
    def _load_mol_dict_by_index(self, index: int) -> tuple[dict, str]:
        """Return (mol_dict, path_string) for molecule `index`."""
        if not self.supports_random_access():
            raise RuntimeError(
                "Random access isn't supported for gzip-compressed tar "
                "archives (gzip has no member index). Use "
                "iter_geom_records() for a single forward pass instead."
            )

        if self.is_tar:  # plain/uncompressed tar
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
            rel_path = self._pickle_paths[index]
            with open(self.root / rel_path, "rb") as f:
                mol_dict = pickle.load(f)
            return mol_dict, rel_path

    def get_molecule_records(
            self,
            index: int,
            max_confs_per_mol: Optional[int] = None
    ) -> list[tuple[RDMolecule, dict]]:
        """Return every (record, meta) conformer pair for molecule `index`."""
        mol_dict, path_str = self._load_mol_dict_by_index(index)
        return list(
            self._expand_molecule(
                mol_dict,
                mol_dict.get("smiles", "<unknown>"),
                path_str,
                max_confs_per_mol
            )
        )

    def get_record(
            self,
            index: int,
            conformer_index: int = 0
    ) -> tuple[RDMolecule, dict]:
        """Return a single (record, meta) for molecule `index`, conformer `conformer_index`."""
        records = self.get_molecule_records(
            index, max_confs_per_mol=conformer_index + 1
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
            max_confs_per_mol: Optional[int]
    ) -> Iterator[tuple[RDMolecule, dict]]:
        n_mols = 0
        for rel_path in self._pickle_paths:
            pickle_path = self.root / rel_path
            if not pickle_path.exists():
                continue
            with open(pickle_path, "rb") as f:
                mol_dict = pickle.load(f)

            yield from self._expand_molecule(
                mol_dict, mol_dict.get("smiles", "<unknown>"), rel_path,
                max_confs_per_mol,
            )
            del mol_dict

            n_mols += 1
            if max_mols is not None and n_mols >= max_mols:
                return

    def _iter_from_plain_tar(
            self,
            max_mols: Optional[int],
            max_confs_per_mol: Optional[int]
    ) -> Iterator[tuple[RDMolecule, dict]]:
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

            yield from self._expand_molecule(
                mol_dict, mol_dict.get("smiles", "<unknown>"), member.name,
                max_confs_per_mol,
            )
            del mol_dict

            n_mols += 1
            if max_mols is not None and n_mols >= max_mols:
                return

    def _iter_from_gz_tar(
            self,
            max_mols: Optional[int],
            max_confs_per_mol: Optional[int]
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

                yield from self._expand_molecule(
                    mol_dict, mol_dict.get("smiles", "<unknown>"), member.name,
                    max_confs_per_mol,
                )
                del mol_dict

                n_mols += 1
                if max_mols is not None and n_mols >= max_mols:
                    return

    def iter_geom_records(
            self,
            max_mols: Optional[int] = None,
            max_confs_per_mol: Optional[int] = None
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
            yield from self._iter_from_gz_tar(max_mols, max_confs_per_mol)
        elif self.is_tar:  # plain/uncompressed
            yield from self._iter_from_plain_tar(max_mols, max_confs_per_mol)
        else:
            yield from self._iter_from_directory(max_mols, max_confs_per_mol)

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
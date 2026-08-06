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

import requests

from .RDKit import RDMolecule

__all__ = [
    "GEOMLoader",
    "GEOMDownloader"
]

_TAR_SUFFIXES = {".tar.gz", ".tgz"}

def _has_tar_suffix(path: Path) -> bool:
    return path.suffix == ".tgz" or "".join(path.suffixes[-2:]) == ".tar.gz"

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
        self.is_tar = self.root.is_file() and _has_tar_suffix(self.root)

        self.summary: Optional[dict] = None
        if not self.is_tar:
            summary_file = self.root / summary_path
            if not summary_file.exists():
                raise FileNotFoundError(f"Could not find {summary_file}")
            with open(summary_file) as f:
                self.summary = json.load(f)  # {smiles: {"pickle_path": ..., ...}}
        elif not self.root.exists():
            raise FileNotFoundError(f"Could not find archive {self.root}")

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
    # Mode A: extracted directory
    # ------------------------------------------------------------------
    def _iter_from_directory(
            self,
            max_mols: Optional[int],
            max_confs_per_mol: Optional[int]
    ) -> Iterator[tuple[RDMolecule, dict]]:
        n_mols = 0
        for smiles, mol_meta in self.summary.items():
            pickle_rel_path = mol_meta.get("pickle_path")
            if pickle_rel_path is None:
                continue

            pickle_path = self.root / pickle_rel_path
            if not pickle_path.exists():
                continue

            with open(pickle_path, "rb") as f:
                mol_dict = pickle.load(f)

            yield from self._expand_molecule(
                mol_dict, smiles, pickle_rel_path, max_confs_per_mol
            )
            del mol_dict

            n_mols += 1
            if max_mols is not None and n_mols >= max_mols:
                return

    # ------------------------------------------------------------------
    # Mode B: direct tar.gz streaming (no extraction to disk)
    # ------------------------------------------------------------------
    def _iter_from_tar(
            self,
            max_mols: Optional[int],
            max_confs_per_mol: Optional[int]
    ) -> Iterator[tuple[RDMolecule, dict]]:
        subset_marker = f"/{self.subset}/"
        n_mols = 0

        # "r|gz" = streaming mode: forward-only single pass, no member
        # index is built, nothing is written to disk.
        with tarfile.open(self.root, "r") as tf:
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
                    mol_dict, mol_dict.get("smiles", "<unknown>"),
                    member.name, max_confs_per_mol,
                )
                del mol_dict

                n_mols += 1
                if max_mols is not None and n_mols >= max_mols:
                    return

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------
    def iter_geom_records(
            self,
            max_mols: Optional[int] = None,
            max_confs_per_mol: Optional[int] = None
    ) -> Iterator[tuple[RDMolecule, dict]]:
        """
        Yield (record, meta) pairs, one per conformer.

        record:
            - if return_mols=False: (smiles, coords) where coords is an
              (n_atoms, 3) float64 numpy array of Angstrom coordinates.
            - if return_mols=True: the RDKit Chem.Mol for that conformer.

        meta:
            dict with smiles, pickle_path, conformer_index, n_atoms,
            atomic_numbers, total_energy, boltzmann_weight.

        In tar-streaming mode this is a strict single forward pass over
        the archive; calling it twice re-reads the archive from the start.
        """
        if self.is_tar:
            yield from self._iter_from_tar(max_mols, max_confs_per_mol)
        else:
            yield from self._iter_from_directory(max_mols, max_confs_per_mol)

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
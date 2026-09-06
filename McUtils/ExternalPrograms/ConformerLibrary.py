"""
Provides `ConformerLibrary`, a small, backend-agnostic reader for
conformer ensembles stored as `(smi, coord)` pairs, one entry per
molecule.

The actual storage format is delegated to a `ConformerLibraryBackend`
adaptor (`backend`, always the library's first constructor argument).
The default `NumpyTreeArchiveBackend` reads/writes the "everything in
one tree" format built with `NumpyTreeArchive.from_tree` (see that
class's docstring), e.g.

    samp = TestManager.test_data('a2bbb-substances.smi')
    conf_lib = {}
    for i in [33, 68, 77]:
        smi = SMILESSupplier(samp).find_smi(i)
        confs, engs = generate_conformer_ensemble(Molecule.from_string, smi)
        conf_lib[str(i)] = {'smi': smi, 'coord': [c.coords for c in confs]}

    lib = ConformerLibrary(conf_lib)
    lib.save("conformers.npz")
    lib = ConformerLibrary.from_nparchive("conformers.npz")

`SMILESDatabaseBackend`, `QM9Backend`, and `GEOMBackend` adapt the same
`(smi, coord)`-pair interface onto a `SMILESSupplier`-backed `.smi`/
`.lismi` database, a packed `QM9` dataset, or a `GEOMLoader` archive,
respectively -- so the same `ConformerLibrary` interface works whether
conformers live in a purpose-built archive or are read straight out of
one of those external formats.
"""

import abc, os

from .. import Devutils as dev
from ..Scaffolding import NumpyTreeArchive
from .SMILES import SMILESSupplier
from .QM9 import QM9
from .GEOM import GEOMLoader
from .Conformers import generate_conformer_ensemble

__all__ = [
    "ConformerLibrary",
    # "ConformerLibraryBackend",
    # "NumpyTreeArchiveBackend",
    # "SMILESDatabaseBackend",
    # "QM9Backend",
    # "GEOMBackend"
]

class ConformerLibraryBackend(metaclass=abc.ABCMeta):
    """
    The adaptor interface a `ConformerLibrary` needs from its storage: a
    `{key: {'smi':.., 'coord':..}}`-shaped mapping, keyed however the
    underlying storage naturally keys itself (string paths for a
    `NumpyTreeArchive`, integer row indices for `SMILESSupplier`/`QM9`/
    `GEOMLoader`).
    """

    @abc.abstractmethod
    def __len__(self):
        raise NotImplementedError(f"{type(self).__name__} is an abstract base class")

    @abc.abstractmethod
    def __contains__(self, key):
        raise NotImplementedError(f"{type(self).__name__} is an abstract base class")

    @abc.abstractmethod
    def keys(self):
        raise NotImplementedError(f"{type(self).__name__} is an abstract base class")

    @abc.abstractmethod
    def get_record(self, key):
        """Returns the raw `{'smi':.., 'coord':..}` record for `key`."""
        raise NotImplementedError(f"{type(self).__name__} is an abstract base class")

    def get_smiles(self, key):
        """
        Returns just the SMILES string for `key`. The default just pulls
        it out of `get_record`; backends that can answer this without
        touching the (often much larger) coordinate data override it.
        """
        return self.get_record(key)['smi']

    def __getitem__(self, key):
        return self.get_record(key)

    def __iter__(self):
        return iter(self.keys())


class NumpyTreeArchiveBackend(ConformerLibraryBackend):
    """
    Adapts a `NumpyTreeArchive` -- or a raw nested tree/dict, or a path
    to a previously-saved one -- to the `ConformerLibraryBackend`
    interface. Keys are whatever top-level keys the tree was built with
    (e.g. `"33"`, `"68"`, ...); each maps to a `{'smi':.., 'coord':..}`
    record.
    """

    def __init__(self, archive, **load_opts):
        if isinstance(archive, NumpyTreeArchive):
            self.archive = archive
        elif dev.is_dict_like(archive):
            self.archive = NumpyTreeArchive.from_tree(archive, **load_opts)
        else:
            # a path, an open file-like stream (e.g. an `io.BytesIO` a
            # caller `.save(...)`-ed into), or anything else
            # `NumpyTreeArchive.load` itself accepts
            self.archive = NumpyTreeArchive.load(archive, **load_opts)

    @classmethod
    def from_tree(cls, tree, **opts):
        return cls(NumpyTreeArchive.from_tree(tree, **opts))

    @classmethod
    def load(cls, file, **opts):
        return cls(NumpyTreeArchive.load(file, **opts))

    def save(self, file, **opts):
        return self.archive.save(file, **opts)

    def __len__(self):
        return len(self.archive)

    def __contains__(self, key):
        return str(key) in self.archive

    def keys(self):
        return self.archive.keys()

    def get_record(self, key):
        return self.archive[str(key)]


class SMILESDatabaseBackend(ConformerLibraryBackend):
    """
    Adapts a `SMILESSupplier`-backed `.smi`/`.lismi` database ("the
    mostly SMILES paradigm") to the `ConformerLibraryBackend` interface.
    Row indices are used as keys; `coord` comes from a `coord_key`
    entry in the supplier's `metadata_arrays` if it carries one (e.g. a
    database packaged with `metadata_arrays={'coords': ...}`), and is
    `None` for plain SMILES-only databases.
    """

    def __init__(self, smiles_file, coord_key='coord', **supplier_opts):
        self.supplier = (
            smiles_file
                if isinstance(smiles_file, SMILESSupplier) else
            SMILESSupplier.from_line_index_database(smiles_file, **supplier_opts)
        )
        self.coord_key = coord_key
        self._len = None

    def __len__(self):
        if self._len is None:
            with self.supplier:
                self._len = len(self.supplier)
        return self._len

    def __contains__(self, key):
        return 0 <= int(key) < len(self)

    def keys(self):
        return range(len(self))

    def get_smiles(self, key):
        with self.supplier:
            return self.supplier.find_smi(int(key))

    def get_record(self, key):
        n = int(key)
        has_meta = self.supplier.metadata_arrays is not None
        with self.supplier:
            if has_meta:
                smi, meta = self.supplier.find_smi(n, include_metadata=True)
            else:
                smi, meta = self.supplier.find_smi(n), {}
        return {'smi': smi, 'coord': meta.get(self.coord_key)}


class QM9Backend(ConformerLibraryBackend):
    """
    Adapts a packed `QM9` dataset -- a `QM9` wrapper, or a path to its
    `.npz` -- to the `ConformerLibraryBackend` interface. Row indices
    are used as keys.
    """

    def __init__(self, qm9_data):
        self.qm9 = qm9_data if isinstance(qm9_data, QM9) else QM9(qm9_data)

    def __len__(self):
        return len(self.qm9.qm9_data['sizes'])

    def __contains__(self, key):
        return 0 <= int(key) < len(self)

    def keys(self):
        return range(len(self))

    def get_smiles(self, key):
        return str(self.qm9.qm9_data['smiles'][int(key)])

    def get_record(self, key):
        data = self.qm9.load_data(int(key), props=['smiles', 'coords'])
        return {'smi': str(data['smiles']), 'coord': data['coords']}


class GEOMBackend(ConformerLibraryBackend):
    """
    Adapts a GEOM `rdkit_folder` archive/directory (via `GEOMLoader`) to
    the `ConformerLibraryBackend` interface. Random access is backed by
    a one-time materialization of `iter_geom_records` into an in-memory
    `(smi, coord)` list -- fine for exercising the infrastructure, but
    not meant to compete with `GEOMInternalsWrapper`'s zarr-backed
    random access over the full dataset.
    """

    def __init__(self, root, subset='drugs', max_mols=None, max_confs_per_mol=None,
                 include_tag=False, **loader_opts):
        self.loader = root if isinstance(root, GEOMLoader) else GEOMLoader(root, subset, **loader_opts)
        self._max_mols = max_mols
        self._max_confs_per_mol = max_confs_per_mol
        self._include_tag = include_tag
        self._records = None

    def _ensure_loaded(self):
        if self._records is None:
            self._records = [
                {
                    'smi': mol.to_string('smi', remove_hydrogens=True, include_tag=self._include_tag),
                    'coord': mol.coords
                }
                for mol, meta in self.loader.iter_geom_records(
                    max_mols=self._max_mols,
                    max_confs_per_mol=self._max_confs_per_mol,
                    create_mols=True
                )
            ]
        return self._records

    def __len__(self):
        return len(self._ensure_loaded())

    def __contains__(self, key):
        return 0 <= int(key) < len(self)

    def keys(self):
        return range(len(self))

    def get_smiles(self, key):
        return self._ensure_loaded()[int(key)]['smi']

    def get_record(self, key):
        return self._ensure_loaded()[int(key)]


class ConformerLibrary:
    """
    A backend-agnostic reader for conformer ensembles stored as
    `(smi, coord)` pairs, one entry per molecule.

        lib = ConformerLibrary(conf_lib)                     # raw nested dict/tree
        lib = ConformerLibrary.from_nparchive("confs.npz")
        lib = ConformerLibrary.from_smidb("substances.lismi")
        lib = ConformerLibrary.qm9("qm9.npz")
        lib = ConformerLibrary.geom("rdkit_folder.tar.gz", subset='drugs')

        lib[33]                # {'smi':.., 'coord':..}, or `loader(...)`'s result
        lib.get_smiles(33)     # just the SMILES, cheaply where the backend allows
        len(lib); 33 in lib; list(lib.keys())

    `backend` is always the first constructor argument: pass an
    explicit `ConformerLibraryBackend` (or any of the per-format
    `from_*`/named constructors below), or a raw tree/path/archive to
    have it wrapped in the default `NumpyTreeArchiveBackend`.

    `loader`, if given, is applied to every raw `{'smi':.., 'coord':..}`
    record before it's returned from `__getitem__`/`get_record` -- e.g.
    to turn it into a `Molecule` (or list of `Molecule`s) instead of a
    plain dict.
    """

    LibraryBackend = ConformerLibraryBackend # to make it easier to subclass without exposing more surface

    def __init__(self, backend=None, loader=None):
        if backend is None:
            backend = NumpyTreeArchiveBackend.from_tree({})
        elif not isinstance(backend, ConformerLibraryBackend):
            backend = NumpyTreeArchiveBackend(backend)
        self.backend = backend
        self.loader = loader

    def __len__(self):
        return len(self.backend)

    def __contains__(self, key):
        return key in self.backend

    def __iter__(self):
        return iter(self.backend.keys())

    def keys(self):
        return self.backend.keys()

    def get_smiles(self, key):
        return self.backend.get_smiles(key)

    def get_record(self, key):
        record = self.backend.get_record(key)
        if self.loader is not None:
            record = self.loader(record)
        return record

    def __getitem__(self, key):
        return self.get_record(key)

    def items(self):
        for key in self.keys():
            yield key, self[key]

    def save(self, file, **opts):
        """Persists this library, if its backend supports it (currently
        only `NumpyTreeArchiveBackend`)."""
        if not hasattr(self.backend, 'save'):
            raise TypeError(f"{type(self.backend).__name__} doesn't support `save`")
        return self.backend.save(file, **opts)

    def __repr__(self):
        return f"{type(self).__name__}({self.backend!r}, <{len(self)}>)"

    # -- one named constructor per supported backend -----------------------

    @classmethod
    def from_nparchive(cls, archive, loader=None, **opts):
        """Builds a library over the default `NumpyTreeArchive` backend
        (a path, an open `NumpyTreeArchive`, or a raw nested tree/dict)."""
        return cls(NumpyTreeArchiveBackend(archive, **opts), loader=loader)

    @classmethod
    def from_smidb(cls, smiles_file, loader=None, coord_key='coord', **opts):
        """Builds a library over a `SMILESSupplier`-backed `.smi`/
        `.lismi` database (a path, or an existing `SMILESSupplier`)."""
        return cls(SMILESDatabaseBackend(smiles_file, coord_key=coord_key, **opts), loader=loader)

    @classmethod
    def qm9(cls, qm9_data, loader=None, **opts):
        """Builds a library over a packed QM9 dataset (a path to its
        `.npz`, or an existing `QM9` wrapper)."""
        return cls(QM9Backend(qm9_data, **opts), loader=loader)

    @classmethod
    def geom(cls, root, subset='drugs', loader=None, **opts):
        """Builds a library over a GEOM `rdkit_folder` archive/directory
        (a path, or an existing `GEOMLoader`)."""
        return cls(GEOMBackend(root, subset=subset, **opts), loader=loader)

    # -- default creator for the "first" (NumpyTreeArchive) paradigm -------

    @classmethod
    def create_smiles_iterator_archive(
            cls, smi_list, target_file,
            loader,
            ensemble_generator=None,
            keys=None, ensemble_opts=None,
            save_opts=None
    ):
        """
        Builds a `NumpyTreeArchive`-backed conformer library by running
        `conformer_generator` over every SMILES in `smi_list`, then
        saving the resulting `{key: {'smi':.., 'coord':[...]}}` tree to
        `target_file`. This is the default creator for the "first"
        (`NumpyTreeArchive`) backend paradigm -- it's just the loop from
        that paradigm's own construction idiom, generalized to an
        arbitrary iterable of SMILES:

            conf_lib = {}
            for i, smi in enumerate(smi_list):
                confs, engs = generate_conformer_ensemble(Molecule.from_string, smi)
                conf_lib[str(i)] = {'smi': smi, 'coord': [c.coords for c in confs]}
            NumpyTreeArchive.from_tree(conf_lib).save(target_file)

            conf_lib = ConformerLibrary.create_smiles_iterator_archive(
                smi_list, "conformers.npz",
                loader=Molecule.from_string,
                conformer_generator=generate_conformer_ensemble
            )

        :param loader: the molecule constructor forwarded as
            `conformer_generator`'s first argument (e.g.
            `Molecule.from_string`)
        :param ensemble_generator: `(loader, smi, **ensemble_opts) ->
            (confs, engs)`, where every `conf` in `confs` exposes
            `.coords` -- e.g. a `generate_conformer_ensemble`-style
            ensemble generator. `engs` is accepted (to match that
            idiom's return signature) but not itself stored.
        :param keys: optional explicit top-level keys, index-aligned
            with `smi_list` (default: `str(i)` for `i, smi` in
            `enumerate(smi_list)`)
        :param ensemble_opts: extra keywords forwarded to
            `conformer_generator`
        :param save_opts: extra keywords forwarded to the archive's
            `.save(target_file, ...)`
        """
        if ensemble_generator is None:
            ensemble_generator = generate_conformer_ensemble

        ensemble_opts = ensemble_opts or {}
        entries = enumerate(smi_list) if keys is None else zip(keys, smi_list)

        conf_lib = {}
        for key, smi in entries:
            confs, engs = ensemble_generator(loader, smi, **ensemble_opts)
            conf_lib[str(key)] = {
                'smi': smi,
                'coord': [c.coords for c in confs],
                'energies': engs,
            }

        archive = NumpyTreeArchive.from_tree(conf_lib)
        archive.save(target_file, **(save_opts or {}))
        return cls(NumpyTreeArchiveBackend(archive)), target_file

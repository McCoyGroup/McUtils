import importlib
import io
import multiprocessing
import os
from pathlib import Path
import pickle
import sqlite3
import subprocess
import sys
from collections.abc import Mapping

import numpy as np
import tarfile

if "pytest" not in sys.modules:
    import unittest
    raise unittest.SkipTest("IndexedTarTests requires the pytest runner")
pytest = sys.modules["pytest"]

from McUtils.Scaffolding.Storage import FileStoreLock, IndexedTarStore, JSONLSupplier, NPZLSupplier
from McUtils.Scaffolding.Serializers import NumpyTreeArchive
from McUtils.Numputils.Serialization import MemmappedNPZFile, MemmappedNPTarFile


def append_worker(path, number):
    store = IndexedTarStore(path)
    for item in range(3):
        store.write_trees([(f"job-{number}-{item}", None, {"value": f"{number}:{item}".encode()})])


def crash_worker(path):
    store = IndexedTarStore(path)
    original = store._write_tree

    def interrupted(*args, **kwargs):
        original(*args, **kwargs)
        os._exit(17)

    store._write_tree = interrupted
    store.write_trees([("unfinished", None, {"value": b"must roll back"})])


def test_lookup_does_not_materialize_a_missing_store(tmp_path):
    store = IndexedTarStore(tmp_path / "absent" / "jobs.tar")
    assert store.names() == []
    with pytest.raises(FileNotFoundError):
        store.open("job/results.json")
    assert list(tmp_path.iterdir()) == []


def test_indexed_reads_seek_without_scanning_tar_and_survive_reopening(tmp_path, monkeypatch):
    path = tmp_path / "jobs.tar"
    directory = tmp_path / "source"
    directory.mkdir()
    (directory / "binary").write_bytes(bytes(range(256)) * 200)
    (directory / "empty").mkdir()
    (directory / "link").symlink_to("binary")
    (directory / "empty" / "parent-link").symlink_to("../binary")
    name = "job-" + "α" * 130
    store = IndexedTarStore(path)
    store.write_trees([(name, directory, {"results.json": b'{"value":1}'})])
    assert path.read_bytes()[:2] != b"\x1f\x8b"
    reopened = IndexedTarStore(path)
    with monkeypatch.context() as scoped:
        scoped.setattr(tarfile, "open", lambda *args, **kwargs: pytest.fail("lookup scanned the tar"))
        assert reopened.read(name + "/binary") == bytes(range(256)) * 200
        assert reopened.read(name + "/link") == bytes(range(256)) * 200
        assert reopened.read(name + "/empty/parent-link") == bytes(range(256)) * 200
        with reopened.open(name + "/binary") as stream:
            stream.seek(300)
            assert stream.read(6) == bytes(range(256))[44:50]
            stream.seek(-2, io.SEEK_END)
            assert stream.read() == b"\xfe\xff"
    Path(store.index_path).unlink()
    assert IndexedTarStore(path).read(name + "/results.json") == b'{"value":1}'


def test_replacement_rebuild_and_compaction_preserve_only_current_members(tmp_path):
    store = IndexedTarStore(tmp_path / "jobs.tar")
    store.write_trees([("job", None, {"old": b"x" * 50000, "value": b"before"})])
    with store.open("job/value") as old_reader:
        store.write_trees([("job", None, {"value": b"after"})])
        assert store.read("job/value") == b"after"
        with pytest.raises(FileNotFoundError):
            store.open("job/old")
        Path(store.index_path).unlink()
        assert "job/old" not in store.names()
        size = os.path.getsize(store.path)
        store.compact()
        assert os.path.getsize(store.path) < size
        assert old_reader.read() == b"before"
    store.discard("job")
    Path(store.index_path).unlink()
    with pytest.raises(FileNotFoundError):
        store.open("job/value")


def test_failed_append_preserves_previous_generation_and_source(tmp_path, monkeypatch):
    store = IndexedTarStore(tmp_path / "jobs.tar")
    store.write_trees([("job", None, {"value": b"old"})])
    directory = tmp_path / "source"
    directory.mkdir()
    (directory / "value").write_bytes(b"new")
    original = store._write_tree

    def fail(*args, **kwargs):
        original(*args, **kwargs)
        raise OSError("injected write failure")

    monkeypatch.setattr(store, "_write_tree", fail)
    with pytest.raises(OSError, match="injected"):
        store.write_trees([("job", directory, {})])
    assert store.read("job/value") == b"old"
    assert (directory / "value").read_bytes() == b"new"


def test_process_death_rolls_back_unpublished_append(tmp_path):
    path = str(tmp_path / "jobs.tar")
    store = IndexedTarStore(path)
    store.write_trees([("complete", None, {"value": b"saved"})])
    child = multiprocessing.get_context("spawn").Process(target=crash_worker, args=(path,))
    child.start()
    child.join(30)
    assert child.exitcode == 17
    assert store.read("complete/value") == b"saved"
    with pytest.raises(FileNotFoundError):
        store.open("unfinished/value")


def test_concurrent_processes_do_not_lose_members(tmp_path):
    path = str(tmp_path / "jobs.tar")
    context = multiprocessing.get_context("spawn")
    children = [context.Process(target=append_worker, args=(path, number)) for number in range(3)]
    for child in children:
        child.start()
    for child in children:
        child.join(30)
        assert child.exitcode == 0
    store = IndexedTarStore(path)
    for number in range(3):
        for item in range(3):
            assert store.read(f"job-{number}-{item}/value") == f"{number}:{item}".encode()


def test_lock_is_reentrant_across_instances_and_released_after_error(tmp_path):
    first = FileStoreLock(tmp_path / "store.lock")
    second = FileStoreLock(tmp_path / "store.lock")
    with pytest.raises(ValueError), first(), second():
        raise ValueError("test")
    with second(), first():
        pass


def test_compressed_export_and_invalid_paths(tmp_path):
    compressed = tmp_path / "job.tar.gz"
    IndexedTarStore.export_trees([("job", None, {"value": b"hello"})], compressed, compression="gz")
    with tarfile.open(compressed, "r:gz") as archive:
        assert archive.extractfile("job/value").read() == b"hello"
    store = IndexedTarStore(tmp_path / "jobs.tar")
    for name in ("/absolute", "../escape", "job/../escape"):
        with pytest.raises(ValueError):
            store.write_trees([(name, None, {})])
    with pytest.raises(ValueError, match="overlapping"):
        store.write_trees([("job", None, {}), ("job/child", None, {})])


def test_hardlinks_do_not_cross_independently_replaceable_records(tmp_path):
    first, second = tmp_path / "first", tmp_path / "second"
    first.mkdir()
    second.mkdir()
    (first / "value").write_bytes(b"original")
    os.link(first / "value", second / "value")
    store = IndexedTarStore(tmp_path / "jobs.tar")
    store.write_trees([("first", first, {}), ("second", second, {})])
    store.write_trees([("first", None, {"value": b"replacement"})])
    assert store.read("second/value") == b"original"
    store.discard("second")
    assert store.names("second") == []
    Path(store.index_path).unlink()
    assert store.names("second") == []

@pytest.mark.parametrize("module,name", [
    ("McUtils.Scaffolding.Serializers", "NumpyTreeArchive"),
    ("McUtils.Scaffolding.Serializers", "NumPySerializer"),
    ("McUtils.Scaffolding.Storage", "IndexedTarStore"),
    ("McUtils.Scaffolding.Storage", "JSONLSupplier"),
    ("McUtils.Numputils.Serialization", "MemmappedNPZFile"),
    ("McUtils.Numputils.Serialization", "MemmappedNPTarFile"),
])
def test_exports_and_pickle_references_use_the_defining_module(module, name):
    owner = importlib.import_module(module)
    obj = getattr(owner, name)
    assert obj.__module__ == module
    assert getattr(importlib.import_module(module.rsplit(".", 1)[0]), name) is obj
    assert pickle.loads(f"c{module}\n{name}\n.".encode()) is obj


@pytest.mark.parametrize("kind,suffix", [(NumpyTreeArchive, ".npz"), (MemmappedNPZFile, ".npz"),
                                         (MemmappedNPTarFile, ".nptar"), (IndexedTarStore, ".tar")])
def test_common_archive_mapping_factory_persistence_and_context(kind, suffix, tmp_path):
    value = b"payload" if kind is IndexedTarStore else np.arange(12).reshape(4, 3)
    destination = tmp_path / ("saved" + suffix)
    with kind.from_tree({"entry": value}) as archive:
        assert isinstance(archive, Mapping)
        assert list(archive) == list(archive.keys()) == archive.files == ["entry"]
        assert len(archive) == 1 and "entry" in archive
        assert archive.get("missing", "default") == "default"
        with pytest.raises(KeyError):
            archive["missing"]
        np.testing.assert_equal(archive["entry"], value)
        np.testing.assert_equal(dict(archive.items())["entry"], value)
        archive.save(destination)
    with kind.load(destination) as restored:
        np.testing.assert_equal(restored.unpack()["entry"], value)


def test_tar_nested_records_empty_directories_and_owned_storage(tmp_path):
    tree = {"job": {"nested": {"result": b"42"}, "empty": {}, "log": b"done"}, "README": b"root"}
    destination = tmp_path / "saved.tar"
    with IndexedTarStore.from_tree(tree) as archive:
        owned = Path(archive.path).parent
        assert archive["job"] == tree["job"]
        assert archive.get("job/nested") == {"result": b"42"}
        assert archive.unpack() == tree
        assert archive["job/empty"] == {}
        archive.save(destination)
    assert not owned.exists()
    assert IndexedTarStore.load(destination).unpack() == tree


def test_tar_saved_snapshot_excludes_superseded_members(tmp_path):
    archive = IndexedTarStore(tmp_path / "original.tar")
    archive.write_trees([("job", None, {"old": b"x" * 10000})])
    archive.write_trees([("job", None, {"new": b"latest"})])
    original_size = os.path.getsize(archive.path)
    archive.save(tmp_path / "snapshot.tar")
    with tarfile.open(tmp_path / "snapshot.tar", "r:") as plain:
        assert plain.getnames() == ["job", "job/new"]
    assert os.path.getsize(tmp_path / "snapshot.tar") < original_size
    assert archive["job"] == {"new": b"latest"}


def test_numpy_member_mapping_is_shared_between_tar_arrays_and_line_suppliers(tmp_path):
    arrays = importlib.import_module("McUtils.Numputils.Serialization")
    lines = importlib.import_module("McUtils.Scaffolding.Storage")
    assert lines._memmap_npy_member is arrays._memmap_npy_member
    value = np.arange(35, dtype=np.int64).reshape(5, 7)
    buffer = io.BytesIO()
    np.save(buffer, value, allow_pickle=False)
    archive = IndexedTarStore.from_tree({"record": {"value.npy": buffer.getvalue()}}, file=tmp_path / "data.tar")
    mapped = archive.memmap("record/value.npy")
    assert isinstance(mapped, np.memmap)
    np.testing.assert_equal(mapped, value)
    assert mapped.flags.writeable is False
    writable = archive.memmap("record/value.npy", mode="c")
    writable[0, 0] = -1
    assert archive.memmap("record/value.npy")[0, 0] == 0
    with pytest.raises(ValueError, match="modes"):
        archive.memmap("record/value.npy", mode="r+")


@pytest.mark.parametrize("backend", ["npz", "nptar"])
def test_tree_roundtrip_with_empty_scalar_and_fortran_arrays(tmp_path, backend, monkeypatch):
    tree = {"one": {"coords": np.asfortranarray(np.arange(24).reshape(4, 6)),
                    "empty": np.empty((0, 3)), "scalar": np.array(2.5)},
            "name": "molecule"}
    destination = tmp_path / ("tree." + backend)
    NumpyTreeArchive.from_tree(tree, max_depth=None).save(destination, backend=backend)
    if backend == "nptar":
        monkeypatch.setattr(tarfile.TarFile, "extractfile", lambda *args, **kwargs: pytest.fail("extracted an array"))
    with NumpyTreeArchive.load(destination, backend=backend) as restored:
        np.testing.assert_equal(restored["one/coords"], tree["one"]["coords"])
        assert restored["one/empty"].shape == (0, 3)
        assert restored["one/scalar"] == 2.5
        assert restored["name"] == "molecule"


@pytest.mark.parametrize("kind", [MemmappedNPZFile, MemmappedNPTarFile])
def test_mapped_arrays_save_back_to_the_same_path(tmp_path, kind):
    destination = tmp_path / "arrays"
    with kind.from_tree({"one": np.arange(3), "two": np.arange(11)}, file=destination) as archive:
        archive.save(destination)
        np.testing.assert_equal(archive["two"], np.arange(11))


def test_object_arrays_cannot_be_mapped(tmp_path):
    path = tmp_path / "objects.npz"
    np.savez(path, values=np.array([{"a": 1}], dtype=object))
    with MemmappedNPZFile.load(path) as archive:
        with pytest.raises(ValueError, match="object arrays"):
            archive["values"]


@pytest.mark.parametrize("records", [[], [{"n": 0}, None, {"n": 2}]])
def test_line_factories_and_mapping_access_preserve_streaming_contract(tmp_path, records):
    archive = JSONLSupplier.from_tree(records)
    try:
        assert list(archive) == records
        assert list(archive.values()) == records
        assert archive.unpack() == records
        assert list(archive.keys()) == list(range(len(records)))
        assert list(archive.items()) == list(enumerate(records))
        assert archive.get(len(records), "missing") == "missing"
        if records:
            assert None in archive
            assert archive[-1] == records[-1]
            assert archive[1:] == records[1:]
        with archive as context:
            assert isinstance(context, tuple) and context[0] is archive
        archive.save(tmp_path / "copy.tar")
    finally:
        archive.close()
    restored = JSONLSupplier.load(tmp_path / "copy.tar")
    try:
        assert restored.unpack() == records
    finally:
        restored.close()


def test_line_save_preserves_metadata_and_numpy_record_values(tmp_path):
    path = tmp_path / "metadata.tar"
    JSONLSupplier.create_jump_database([{"x": 1}, {"x": 2}], path, metadata_arrays={"quality": [.2, .7]})
    archive = JSONLSupplier.load(path)
    try:
        archive.save(tmp_path / "copy.tar")
    finally:
        archive.close()
    copy = JSONLSupplier.load(tmp_path / "copy.tar")
    try:
        assert copy[1] == ({"x": 2}, {"quality": .7})
    finally:
        copy.close()
    numpy_records = NPZLSupplier.from_tree([{"coords": np.arange(6).reshape(2, 3)}])
    try:
        np.testing.assert_equal(numpy_records[0]["coords"], np.arange(6).reshape(2, 3))
        numpy_records.save(tmp_path / "numpy.tar")
    finally:
        numpy_records.close()


def test_fresh_import_orders_have_no_initialization_cycle():
    for first in ("McUtils.Numputils.Serialization", "McUtils.Scaffolding.Storage",
                  "McUtils.Scaffolding.Serializers"):
        code = (f"import {first}; from McUtils.Numputils import *; "
                "from McUtils.Scaffolding.Storage import IndexedTarStore; "
                "from McUtils.Scaffolding.Serializers import NumpyTreeArchive")
        completed = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=30)
        assert completed.returncode == 0, completed.stderr


def test_npz_tree_can_use_the_native_mapped_reader_directly(tmp_path, monkeypatch):
    from McUtils.Numputils.Serialization import load_npz_memmap
    path = tmp_path / "tree.npz"
    NumpyTreeArchive.from_tree({"record": {"coords": np.arange(20).reshape(4, 5)}}).save(path)
    monkeypatch.setattr(np, "load", lambda *args, **kwargs: pytest.fail("materialized an NPZ member"))
    with NumpyTreeArchive.load(path, reader=load_npz_memmap) as archive:
        np.testing.assert_equal(archive["record"]["coords"], np.arange(20).reshape(4, 5))


def test_archive_readout_indexes_file_metadata_without_loading_payloads(monkeypatch):
    from McUtils.Scaffolding.Readouts import ArchiveReadout
    with IndexedTarStore.from_tree({"record": {"large": b"x" * 1000000}}) as archive:
        monkeypatch.setattr(archive, "read", lambda *args: pytest.fail("read a payload during indexing"))
        entries = ArchiveReadout(archive).index()
        assert len(entries) == 1 and entries[0][0] == "record/large" and entries[0][3] == 1000000


def test_line_readout_uses_record_keys():
    from McUtils.Scaffolding.Readouts import ArchiveReadout
    archive = JSONLSupplier.from_tree([{"score": 1.5}])
    try:
        assert ArchiveReadout(archive).index()[0][0] == "0/score"
    finally:
        archive.close()


def test_numeric_archive_module_works_without_importing_scaffolding(tmp_path):
    # Load the numerical module directly, independent of McUtils' umbrella
    # initializer, to verify the NumPy/stdlib-only boundary in a fresh process.
    module = importlib.import_module("McUtils.Numputils.Serialization")
    code = '''
import importlib.util
import pathlib
import sys
import numpy as np
spec = importlib.util.spec_from_file_location("standalone_numeric_archives", sys.argv[1])
numeric = importlib.util.module_from_spec(spec)
spec.loader.exec_module(numeric)
root = pathlib.Path(sys.argv[2])
for kind in (numeric.MemmappedNPZFile, numeric.MemmappedNPTarFile):
    target = root / (kind.__name__ + ".archive")
    with kind.from_tree({"coords": np.arange(12).reshape(4, 3)}) as archive:
        archive.save(target)
    with kind.load(target) as archive:
        np.testing.assert_array_equal(archive["coords"], np.arange(12).reshape(4, 3))
assert not any(name == "McUtils.Scaffolding" or name.startswith("McUtils.Scaffolding.")
               for name in sys.modules)
assert "McUtils" not in sys.modules
'''
    completed = subprocess.run([sys.executable, "-c", code, module.__file__, str(tmp_path)],
                               capture_output=True, text=True, timeout=30)
    assert completed.returncode == 0, completed.stderr

"""Regression tests for the self-contained IndexedTarStore format."""

import io
import multiprocessing
import os
from pathlib import Path
import shutil
import tarfile

import pytest

from McUtils.Scaffolding.Storage import IndexedTarStore


def publication_crash_worker(path, stage):
    store = IndexedTarStore(path)
    original = store._publish_index

    def interrupted(stream, pointer, **options):
        stream.flush()
        os.fsync(stream.fileno())
        if stage == "partial":
            stream.seek(512 + (pointer["generation"] % 2) * store._SLOT_SIZE)
            stream.write(b"torn pointer" * 10)
            stream.flush()
            os.fsync(stream.fileno())
        elif stage == "after":
            original(stream, pointer, **options)
        os._exit(17)

    store._publish_index = interrupted
    store.write_trees([("job", None, {"value": b"new"})])


@pytest.mark.parametrize("stage,expected", [("before", b"old"), ("partial", b"old"), ("after", b"new")])
def test_process_death_during_index_publication(tmp_path, monkeypatch, stage, expected):
    path = str(tmp_path / "jobs.tar")
    store = IndexedTarStore.from_tree({"job": {"value": b"stale"}}, file=path)
    store.write_trees([("job", None, {"value": b"old"})])
    child = multiprocessing.get_context("spawn").Process(target=publication_crash_worker, args=(path, stage))
    child.start()
    child.join(30)
    assert child.exitcode == 17
    with monkeypatch.context() as scoped:
        scoped.setattr(tarfile, "open", lambda *a, **k: pytest.fail("recovery scanned the tar"))
        assert IndexedTarStore(path).read("job/value") == expected
    store.write_trees([("next", None, {"value": b"ok"})])
    assert IndexedTarStore(path).read("job/value") == expected
    assert IndexedTarStore(path).read("next/value") == b"ok"


def test_tar_contains_its_index_and_can_be_copied_alone(tmp_path, monkeypatch):
    source = tmp_path / "source" / "jobs.tar"
    store = IndexedTarStore.from_tree({"job": {"result": b"42"}}, file=source)
    with tarfile.open(source, "r:") as archive:
        assert archive.getnames() == [store._LOCATOR_NAME, "job", "job/result", store._INDEX_NAME]
        import json
        index = [json.loads(line) for line in archive.extractfile(store._INDEX_NAME)]
        assert index[0] == {"version": 2, "previous": None, "replace": []}
        assert {row[0] for row in index[1:]} == {"job", "job/result"}
    assert sorted(p.name for p in source.parent.iterdir()) == ["jobs.tar", "jobs.tar.lock"]
    copy = tmp_path / "only-the-tar.tar"
    shutil.copyfile(source, copy)
    monkeypatch.setattr(tarfile, "open", lambda *a, **k: pytest.fail("copied tar needed a header scan"))
    restored = IndexedTarStore(copy)
    assert restored.read("job/result") == b"42"
    assert restored.names() == ["job", "job/result"]


@pytest.mark.parametrize("operation", ["save", "compact", "export"])
def test_new_snapshots_reopen_without_scanning_headers(tmp_path, monkeypatch, operation):
    source = tmp_path / "jobs.tar"
    store = IndexedTarStore.from_tree({"job": {"value": b"first"}}, file=source)
    store.write_trees([("job", None, {"value": b"latest"})])
    target = tmp_path / "snapshot.tar"
    if operation == "save":
        store.save(target)
    elif operation == "compact":
        store.compact()
        target = source
    else:
        IndexedTarStore.export_trees([("job", None, {"value": b"latest"})], target)
    monkeypatch.setattr(tarfile, "open", lambda *a, **k: pytest.fail("snapshot needed a header scan"))
    assert IndexedTarStore(target).unpack() == {"job": {"value": b"latest"}}


def test_plain_tar_reads_do_not_write_and_next_append_embeds_index(tmp_path, monkeypatch):
    path = tmp_path / "plain.tar"
    with tarfile.open(path, "w") as archive:
        for data in (b"obsolete", b"current"):
            rows = []
            IndexedTarStore._write_tree(archive, "job", None, {"value": data}, rows)
    before = path.read_bytes()
    monkeypatch.setattr(tarfile.TarFile, "extractfile", lambda *a, **k: pytest.fail("rebuild read payloads"))
    store = IndexedTarStore(path)
    assert store.read("job/value") == b"current"
    assert path.read_bytes() == before
    assert sorted(p.name for p in tmp_path.iterdir()) == ["plain.tar", "plain.tar.lock"]
    store.write_trees([("next", None, {"value": b"new"})])
    monkeypatch.setattr(tarfile, "open", lambda *a, **k: pytest.fail("upgrade did not embed index"))
    restored = IndexedTarStore(path)
    assert restored.read("job/value") == b"current"
    assert restored.read("next/value") == b"new"


def test_empty_and_filelike_snapshots_are_self_contained(tmp_path, monkeypatch):
    path = tmp_path / "empty.tar"
    with IndexedTarStore.from_tree({}, file=path) as store:
        assert store.unpack() == {}
        buffer = io.BytesIO()
        store.save(buffer)
    copy = tmp_path / "copy.tar"
    copy.write_bytes(buffer.getvalue())
    monkeypatch.setattr(tarfile, "open", lambda *a, **k: pytest.fail("empty snapshot needed a scan"))
    assert IndexedTarStore(copy).names() == []


def test_from_empty_tree_replaces_an_existing_archive(tmp_path):
    path = tmp_path / "jobs.tar"
    IndexedTarStore.from_tree({"old": b"value"}, file=path)
    assert IndexedTarStore.from_tree({}, file=path).unpack() == {}


def test_corrupt_index_does_not_replay_unpublished_members(tmp_path):
    path = tmp_path / "jobs.tar"
    store = IndexedTarStore.from_tree({"job": {"value": b"old"}}, file=path)
    with tarfile.open(path, "r:") as archive:
        index = archive.getmember(store._INDEX_NAME)
    with path.open("r+b") as stream:
        stream.seek(index.offset_data)
        stream.write(b"!")
    with pytest.raises(ValueError, match="no valid published index"):
        IndexedTarStore(path).names()


@pytest.mark.parametrize("name", [".__mcutils_index__", ".__mcutils_index__/locator",
                                  ".__mcutils_index__/index.json", ".__mcutils_index__/index.jsonl"])
def test_internal_metadata_paths_cannot_be_overwritten(tmp_path, name):
    store = IndexedTarStore(tmp_path / "jobs.tar")
    with pytest.raises(ValueError, match="reserved"):
        store.write_trees([(name, None, {"": b"overwrite"})])
    assert not Path(store.path).exists()


def test_export_rejects_global_pax_headers_before_writing_an_invalid_locator(tmp_path):
    with pytest.raises(ValueError, match="global PAX"):
        IndexedTarStore.export_trees([], tmp_path / "jobs.tar", pax_headers={"comment": "global"})



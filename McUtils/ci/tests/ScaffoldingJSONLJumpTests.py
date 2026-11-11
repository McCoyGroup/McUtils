"""JSONL jump records, incremental writes, and legacy JSON compatibility."""

import hashlib
import io
import json
import tarfile

import pytest

from McUtils.Scaffolding.Storage import IndexedTarStore


def legacy_indexed_tar(path):
    rows = []
    with path.open("wb") as stream:
        with tarfile.open(fileobj=stream, mode="w") as archive:
            IndexedTarStore._write_locator(archive)
            IndexedTarStore._write_tree(archive, "job", None, {"value": b"legacy", "old": b"hidden later"}, rows)
            payload = json.dumps({"version": 1, "members": rows}).encode("utf-8")
            member = tarfile.TarInfo(IndexedTarStore._LEGACY_INDEX_NAME)
            member.size = len(payload)
            offset = archive.offset + 512
            archive.addfile(member, io.BytesIO(payload))
            pointer = {"version": 1, "generation": 1, "offset": offset,
                       "size": len(payload), "end": archive.offset,
                       "sha256": hashlib.sha256(payload).hexdigest()}
        IndexedTarStore._publish_index(stream, pointer)


def test_small_update_writes_only_changed_index_entries(tmp_path, monkeypatch):
    path = tmp_path / "jobs.tar"
    tree = {f"job-{i}": {"value": str(i).encode()} for i in range(64)}
    store = IndexedTarStore.from_tree(tree, file=path)
    with tarfile.open(path, "r:") as archive:
        snapshot_size = archive.getmember(store._INDEX_NAME).size
    store.write_trees([("job-0", None, {"value": b"replacement"})])
    with tarfile.open(path, "r:") as archive:
        member = archive.getmember(store._INDEX_NAME)
        records = [json.loads(line) for line in archive.extractfile(member)]
        assert member.size < snapshot_size // 8
        assert records[0]["replace"] == ["job-0"]
        assert records[0]["previous"] is not None
        assert {row[0] for row in records[1:]} == {"job-0", "job-0/value"}
    store.discard("job-1")
    with tarfile.open(path, "r:") as archive:
        records = [json.loads(line) for line in archive.extractfile(store._INDEX_NAME)]
        assert len(records) == 1 and records[0]["replace"] == ["job-1"]
    monkeypatch.setattr(tarfile, "open", lambda *a, **k: pytest.fail("replayed tar headers"))
    restored = IndexedTarStore(path)
    expected = dict(tree)
    expected["job-0"] = {"value": b"replacement"}
    expected.pop("job-1")
    assert restored.unpack() == expected


def test_prefix_replacement_and_deletion_hide_older_jsonl_rows(tmp_path):
    path = tmp_path / "jobs.tar"
    store = IndexedTarStore.from_tree({"job": {"a": {"value": b"before", "old": b"hide"}, "b": b"stay"},
                                      "other": b"root"}, file=path)
    store.write_trees([("job/a", None, {"value": b"after"})])
    assert IndexedTarStore(path).unpack() == {"job": {"a": {"value": b"after"}, "b": b"stay"}, "other": b"root"}
    store.discard("job/a")
    assert IndexedTarStore(path).unpack() == {"job": {"b": b"stay"}, "other": b"root"}
    store.write_trees([("job", None, {"new": b"whole replacement"})])
    assert IndexedTarStore(path).unpack() == {"job": {"new": b"whole replacement"}, "other": b"root"}


@pytest.mark.parametrize("operation", ["save", "compact"])
def test_jsonl_history_is_consolidated_by_snapshots(tmp_path, operation):
    path = tmp_path / "jobs.tar"
    store = IndexedTarStore.from_tree({"job": {"value": b"old", "gone": b"x"}}, file=path)
    store.write_trees([("job", None, {"value": b"new"})])
    target = tmp_path / "snapshot.tar"
    if operation == "save":
        store.save(target)
    else:
        store.compact()
        target = path
    with tarfile.open(target, "r:") as archive:
        assert archive.getnames().count(store._INDEX_NAME) == 1
        records = [json.loads(line) for line in archive.extractfile(store._INDEX_NAME)]
        assert records[0]["previous"] is None
        assert records[0]["replace"] == []
        assert {row[0] for row in records[1:]} == {"job", "job/value"}
    assert IndexedTarStore(target).unpack() == {"job": {"value": b"new"}}


def test_legacy_json_index_reads_unchanged_and_accepts_jsonl_updates(tmp_path, monkeypatch):
    path = tmp_path / "legacy.tar"
    legacy_indexed_tar(path)
    before = path.read_bytes()
    with monkeypatch.context() as scoped:
        scoped.setattr(tarfile, "open", lambda *a, **k: pytest.fail("JSON fallback scanned tar headers"))
        assert IndexedTarStore(path).read("job/value") == b"legacy"
    assert path.read_bytes() == before
    store = IndexedTarStore(path)
    store.write_trees([("job", None, {"value": b"JSONL"})])
    store.write_trees([("next", None, {"value": b"new"})])
    with monkeypatch.context() as scoped:
        scoped.setattr(tarfile, "open", lambda *a, **k: pytest.fail("mixed history scanned tar headers"))
        assert IndexedTarStore(path).unpack() == {"job": {"value": b"JSONL"}, "next": {"value": b"new"}}
    store.compact()
    with tarfile.open(path, "r:") as archive:
        assert store._LEGACY_INDEX_NAME not in archive.getnames()
        assert archive.getnames().count(store._INDEX_NAME) == 1


def test_corrupt_latest_segment_falls_back_to_previous_published_view(tmp_path, monkeypatch):
    path = tmp_path / "jobs.tar"
    store = IndexedTarStore.from_tree({"job": {"value": b"old"}}, file=path)
    store.write_trees([("job", None, {"value": b"new"})])
    with tarfile.open(path, "r:") as archive:
        latest = archive.getmember(store._INDEX_NAME)
    with path.open("r+b") as stream:
        stream.seek(latest.offset_data)
        stream.write(b"!")
    with monkeypatch.context() as scoped:
        scoped.setattr(tarfile, "open", lambda *a, **k: pytest.fail("corruption recovery scanned headers"))
        assert IndexedTarStore(path).read("job/value") == b"old"
    store.write_trees([("next", None, {"value": b"recovered"})])
    assert IndexedTarStore(path).unpack() == {"job": {"value": b"old"}, "next": {"value": b"recovered"}}



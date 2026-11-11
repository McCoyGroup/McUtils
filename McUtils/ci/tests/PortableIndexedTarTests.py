"""Self-contained indexed snapshots must work after a one-file transfer."""
import io
import json
from pathlib import Path
import shutil
import tarfile
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pytest

from McUtils.Scaffolding.Storage import IndexedTarStore


def test_embedded_snapshot_transfers_without_sidecars_or_tar_scan(tmp_path, monkeypatch):
    data = io.BytesIO()
    np.save(data, np.arange(30, dtype='>i8').reshape(5, 6), allow_pickle=False)
    source = IndexedTarStore.from_tree({'expression': {'values.npy': data.getvalue(), 'text': b'math'}},
                                       file=tmp_path / 'build.tar')
    source.save(tmp_path / 'portable.tar')
    source.write_trees([('expression', None, {'text': b'new build'})])
    target = tmp_path / 'recipient'
    target.mkdir()
    shutil.copyfile(tmp_path / 'portable.tar', target / 'expression.tar')
    before = sorted(p.name for p in target.iterdir())
    with tarfile.open(target / 'expression.tar', 'r:') as plain:
        assert plain.extractfile('expression/text').read() == b'math'
        assert plain.getnames()[0] == IndexedTarStore._LOCATOR_NAME
    monkeypatch.setattr(tarfile, 'open', lambda *a, **k: pytest.fail('read scanned tar headers'))
    with IndexedTarStore.load(target / 'expression.tar', read_only=True) as archive:
        assert len(archive) == 3
        assert archive.read('expression/text') == b'math'
        assert archive.names('expression') == ['expression', 'expression/values.npy', 'expression/text']
        mapped = archive.memmap('expression/values.npy')
        assert isinstance(mapped, np.memmap)
        assert not mapped.flags.writeable
        np.testing.assert_array_equal(mapped, np.arange(30).reshape(5, 6))
        for operation in (lambda: archive.write_trees([]), lambda: archive.discard('expression'), archive.compact):
            with pytest.raises(PermissionError, match='read-only'):
                operation()
    assert sorted(p.name for p in target.iterdir()) == before


def test_embedded_snapshot_includes_only_latest_generation_and_links(tmp_path):
    directory = tmp_path / 'tree'
    directory.mkdir()
    (directory / 'value').write_bytes(b'target')
    (directory / 'link').symlink_to('value')
    archive = IndexedTarStore(tmp_path / 'build.tar')
    archive.write_trees([('job', None, {'obsolete': b'x' * 10000})])
    archive.write_trees([('job', directory, {})])
    archive.save(tmp_path / 'frozen.tar')
    with IndexedTarStore(tmp_path / 'frozen.tar', read_only=True) as restored:
        assert restored.read('job/link') == b'target'
        assert 'job/obsolete' not in restored
        restored.save(tmp_path / 'copied.tar')
    with IndexedTarStore(tmp_path / 'copied.tar', read_only=True) as copied:
        assert copied.read('job/value') == b'target'
        with ThreadPoolExecutor(max_workers=4) as pool:
            assert list(pool.map(lambda _: copied.read('job/link'), range(16))) == [b'target'] * 16
        copied.save(tmp_path / 'ordinary.tar')
    assert IndexedTarStore(tmp_path / 'ordinary.tar').read('job/value') == b'target'


def test_embedded_snapshot_detects_replacement_and_truncation(tmp_path):
    source = IndexedTarStore.from_tree({'value': b'one'})
    target = tmp_path / 'frozen.tar'
    source.save(target)
    with IndexedTarStore(target, read_only=True) as restored:
        assert restored.read('value') == b'one'
        with target.open('ab') as stream:
            stream.write(b'x')
        with pytest.raises(ValueError, match='changed'):
            restored.read('value')
    with IndexedTarStore(target, read_only=True) as broken:
        # Unpublished tail bytes are deliberately ignored by the native store.
        assert broken.read('value') == b'one'
    with target.open('r+b') as stream:
        stream.truncate(512)
    with IndexedTarStore(target, read_only=True) as broken:
        with pytest.raises(ValueError, match='indexed tar'):
            broken.read('value')
    source.close()


def test_embedded_index_rejects_reserved_names_and_unindexed_archives(tmp_path):
    with pytest.raises(ValueError, match='reserved'):
        IndexedTarStore.from_tree({IndexedTarStore._LOCATOR_NAME: b'collision'})
    ordinary = tmp_path / 'ordinary.tar'
    with tarfile.open(ordinary, 'w') as archive:
        info = tarfile.TarInfo('value')
        info.size = 4
        archive.addfile(info, io.BytesIO(b'math'))
    before = sorted(path.name for path in tmp_path.iterdir())
    with IndexedTarStore(ordinary, read_only=True) as plain:
        assert plain.read('value') == b'math'
    assert sorted(path.name for path in tmp_path.iterdir()) == before

"""Export Gaussian results using Scaffolding's nested NumPy archive format.

Run ``python -m McUtils.ExternalPrograms.Parsers.GaussianLogNPZ input.log``
to create input.npz. Large components remain opt-in with --include-all-fields.
"""

import argparse
import os
from pathlib import Path
import tempfile

import numpy as np

from ...Scaffolding import NumpyTreeArchive

__all__ = ["export_gaussian_log"]


def _archive_records(value):
    """Adapt parser records to the string-keyed tree supported by Scaffolding.

    Named tuples become named records. Record sequences and heterogeneous or
    ragged sequences become dictionaries indexed by zero-based string keys.
    Rectangular numerical/string sequences become arrays. Non-string mapping
    keys (e.g. orbital pairs) use their Python string representation; collisions
    raise rather than discard data. No object arrays or pickling are needed.
    """
    if isinstance(value, tuple) and hasattr(value, "_asdict"):
        value = value._asdict()
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            key = str(key)
            if key in result:
                raise ValueError("Gaussian archive mapping keys collide: {!r}".format(key))
            result[key] = _archive_records(item)
        return result
    if isinstance(value, np.ndarray):
        if value.dtype.hasobject:
            return _archive_records(value.tolist())
        return value
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (list, tuple)):
        items = [_archive_records(item) for item in value]
        array_kinds = {item.dtype.kind for item in items if isinstance(item, np.ndarray)}
        if items and len(array_kinds) <= 1 and not any(isinstance(item, dict) for item in items):
            try:
                array = np.asarray(items)
            except (ValueError, TypeError):
                pass
            else:
                if not array.dtype.hasobject:
                    # NumPy would silently stringify mixed string/numeric data.
                    if array.dtype.kind not in "US" or all(
                            np.asarray(item).dtype.kind in "US" for item in items):
                        return array
        return {str(i): item for i, item in enumerate(items)}
    if value is None or isinstance(value, (str, bool, int, float, complex)):
        return value
    raise TypeError("unsupported Gaussian archive value: {}".format(type(value).__name__))


def _reader_archive(reader, keys=None, num=None, include_all_fields=False, source=None):
    jobs = reader.parse_jobs(keys=keys, num=num, include_all_fields=include_all_fields)
    tree = {
        "format": "McUtils.GaussianLog",
        "schema_version": 1,
        "source": None if source is None else os.fspath(source),
        "include_all_fields": bool(include_all_fields),
        "job_count": len(jobs),
        "job_types": tuple(dict.fromkeys(kind for job in jobs for kind in job["job_types"])),
        "jobs": {str(job["index"]): job for job in jobs},
    }
    # Index each job's metadata and component paths, without building a jump
    # table entry for every row in potentially very large numerical records.
    return NumpyTreeArchive.from_tree(_archive_records(tree), allow_pickle=False, max_depth=3)


def _save_archive(archive, output_file, compress=True, overwrite=False):
    output = Path(output_file)
    if output.suffix.lower() != ".npz":
        raise ValueError("Gaussian archive output must have a .npz extension")
    if not overwrite and output.exists():
        raise FileExistsError("archive already exists: {} (use overwrite=True)".format(output))
    # Save before publishing the result, so a failed conversion cannot leave a
    # partial archive or damage an existing one. link also checks no-overwrite
    # atomically, including when another writer creates the output meanwhile.
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, prefix=".gaussian-", suffix=".npz", delete=False) as stream:
            temporary = Path(stream.name)
            archive.save(stream, compress=compress)
        if overwrite:
            os.replace(temporary, output)
        else:
            os.link(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return output


def export_gaussian_log(file, output_file=None, *, keys=None, num=None,
                        include_all_fields=False, compress=True, overwrite=False,
                        encoding="utf-8", reader_type=None):
    """Read a log without requiring write access and save one nested .npz file.

    Defaults to a sibling .npz. Load the result with NumpyTreeArchive.load();
    archive["jobs/0/data"] contains the first job's fields. All printed units,
    job status, routes, and omitted-field inventories are retained.
    """
    from .GaussianImporter import GaussianLogReader
    from ...Parsers import StringStreamReader

    input_file = Path(file)
    output_file = input_file.with_suffix(".npz") if output_file is None else Path(output_file)
    if input_file.resolve() == output_file.resolve():
        raise ValueError("Gaussian archive output must differ from the input log")
    if reader_type is None:
        reader_type = GaussianLogReader

    class TextReader(reader_type, StringStreamReader):
        def __init__(self, text):
            StringStreamReader.__init__(self, text)

    with TextReader(input_file.read_text(encoding=encoding, errors="replace")) as reader:
        archive = _reader_archive(reader, keys=keys, num=num,
                                  include_all_fields=include_all_fields, source=input_file)
    return _save_archive(archive, output_file, compress=compress, overwrite=overwrite)

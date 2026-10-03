"""
Implements an importer for Gaussian output formats
"""

import numpy as np, re, math, io
from .GaussianLogComponents import GaussianLogComponents, GaussianLogDefaults, GaussianLogOrdering
from . import GaussianLogComponents as GaussianLogParsers
from .GaussianFChkComponents import FormattedCheckpointComponents, FormattedCheckpointCommonNames
from ...Parsers import FileStreamReader, FileStreamCheckPoint, FileStreamReaderException, StringStreamReader

__all__ = ["GaussianFChkReader", "GaussianLogReader", "GaussianLogReaderException", "GaussianFChkReaderException"]
__reload_hook__ = [ '.GaussianFChkComponents', ".GaussianLogComponents" ]

########################################################################################################################
#
#                                           GaussianLogReader
#
class GaussianLogReaderException(FileStreamReaderException):
    """
    A class for holding exceptions that occur in the course of reading from a log file
    """
    pass

class GaussianLogReader(FileStreamReader):
    """
    Implements a stream based reader for a Gaussian .log file.
    This is inherits from the `FileStreamReader` base, and takes a two pronged approach to getting data.
    First, a block is found in a log file based on a pair of tags.
    Next, a function (usually based on a `StringParser`) is applied to this data to convert it into a usable data format.
    The goal is to move toward wrapping all returned data in a `QuantityArray` so as to include data type information, too.

    parse() discovers the available components and job types automatically.
    parse_jobs() separates linked jobs. Large blocks are opt-in through
    include_all_fields=True or explicit keys. available_fields(True) lists the
    complete inventory without converting numerical data. Field definitions
    and parsers are registered in GaussianLogComponents, including custom
    literal-tag and multiline-regex components.

    """

    registered_components = GaussianLogComponents
    default_keys = GaussianLogDefaults
    default_ordering = GaussianLogOrdering
    parsers = GaussianLogParsers

    def to_readout(self, keys=None, **opts):
        """
        **LLM Docstring**

        Build a `Readout` of parsed results (`GaussianLogReadout`); ``keys`` limits what is parsed.

        :param opts: `ReadoutInterface.to_readout` options (``include``, ``exclude``, ``units``, ...)
        :return: the readout
        :rtype: McUtils.Jupyter.Readouts.Readout
        """
        from ..Readouts.ElectronicStructure import GaussianLogReadout
        return GaussianLogReadout.from_reader(self, keys=keys).to_readout(**opts)

    def _read_source(self, from_start=False):
        with FileStreamCheckPoint(self):
            if from_start:
                self.seek(0)
            return self.read(-1)

    @staticmethod
    def _has_component(component, source):
        pattern = component.get("block_pattern")
        if pattern is not None:
            return pattern.search(source) is not None
        tag = component.get("tag_start")
        if tag is None:
            return True
        tags = getattr(tag, "tags", (tag,))
        return any(t in source for t in tags)

    def available_fields(self, include_all_fields=False):
        """Discover fields without converting numeric blocks.

        ``include_all_fields=True`` also lists large and alternative legacy
        representations. The reader position is preserved.
        """
        return self._default_keys(self._read_source(from_start=True), include_all_fields)

    def _default_keys(self, source, include_all_fields=False):
        return tuple(k for k, c in self.registered_components.items()
                     if (include_all_fields or c.get("default", True))
                     and (include_all_fields or not c.get("large", False))
                     and self._has_component(c, source))

    def get_default_keys(self, include_all_fields=False):
        """Select every available default field, for any Gaussian job type."""
        return self.available_fields(include_all_fields=include_all_fields)

    def detect_job_types(self):
        """Return all detected job types across the printed route sections."""
        from .GaussianLogTools import parse_job_types
        return parse_job_types(self._read_source(from_start=True))

    def _parse_component(self, key, source, num=None):
        component = self.registered_components[key]
        pattern = component.get("block_pattern")
        if pattern is not None:
            matches = pattern.finditer(source)
            if component["mode"] == "Single":
                match = next(matches, None)
                return None if match is None else component["parser"](match.group())
            from itertools import islice
            if num is not None:
                matches = islice(matches, num)
            blocks = [m.group() for m in matches]
            if not blocks:
                return []
            if component.get("parse_mode", "List") == "List":
                return component["parser"](blocks)
            return [component["parser"](b) for b in blocks]
        # Isolating each component fixes ordering dependencies between Single
        # blocks and ensures absent fields never reach a parser as None.
        with StringStreamReader(source) as reader:
            if component["mode"] == "Single":
                block = reader._parse_block(component.get("tag_start"), component.get("tag_end"),
                                            component.get("validator"), component.get("tag_validator"),
                                            component.get("allow_terminal", False), component.get("expand_until_valid", False),
                                            component.get("preserve_tag", False), False,
                                            component.get("direction", "forward"))
                if block is None:
                    return None
                parser = component.get("parser")
                return block if parser is None else parser(block)
            # Avoid FileStreamReader's fixed-count path, which passes a trailing
            # None to parsers when num exceeds the number of available blocks.
            blocks = []
            while num is None or len(blocks) < num:
                block = reader._parse_block(component.get("tag_start"), component.get("tag_end"),
                                            component.get("validator"), component.get("tag_validator"),
                                            component.get("allow_terminal", False), component.get("expand_until_valid", False),
                                            component.get("preserve_tag", False), False,
                                            component.get("direction", "forward"))
                if block is None:
                    break
                blocks.append(block)
            if not blocks:
                return []
            parser = component.get("parser")
            if parser is None:
                return blocks
            if component.get("parse_mode", "List") == "List":
                return parser(blocks, reader=reader) if component.get("pass_context") else parser(blocks)
            return [parser(b, reader=reader) if component.get("pass_context") else parser(b) for b in blocks]

    def parse_key_block(self, *args, block_pattern=None, **kwargs):
        """Also accept regex-based registrations from GaussianLogComponents."""
        if block_pattern is None:
            return super().parse_key_block(*args, **kwargs)
        source = self._read_source()
        # Use the same dispatch as parse without modifying the shared registry.
        pattern = block_pattern if hasattr(block_pattern, "finditer") else re.compile(block_pattern, re.MULTILINE)
        matches = pattern.finditer(source)
        parser = kwargs.get("parser", lambda b: b)
        if kwargs.get("mode", "Single") == "Single":
            match = next(matches, None)
            if match is None:
                return None
            result = parser(match.group())
            encoding = getattr(self.stream, "_encoding", "utf-8")
            self.seek(self.tell() + len(source[:match.end()].encode(encoding)))
            return result
        from itertools import islice
        if kwargs.get("num") is not None:
            matches = islice(matches, kwargs["num"])
        blocks = [m.group() for m in matches]
        return parser(blocks) if kwargs.get("parse_mode", "List") == "List" else [parser(b) for b in blocks]

    def parse(self, keys=None, num=None, reset=False, include_all_fields=False):
        """Read structured results with automatic field selection.

        With no keys, read all recognized useful fields in the complete file.
        Large AO/MO, density, basis, archive and derivative blocks are omitted
        unless include_all_fields is True. Explicit keys always override this
        policy, including custom registrations. Missing explicit fields return
        None (Single) or [] (List). Malformed present fields raise with the key
        and original exception. num limits repeated blocks independently.

        Automatic reads preserve the current stream position. Explicit reads
        start at the current position; reset=True preserves that position, while
        reset=False advances past the last requested Single component.
        """
        if num is not None and (not isinstance(num, int) or isinstance(num, bool) or num < 0):
            raise ValueError("num must be a nonnegative integer or None")
        automatic = keys is None
        source = self._read_source(from_start=automatic)
        if automatic:
            keys = self._default_keys(source, include_all_fields)
        elif isinstance(keys, str):
            keys = (keys,)
        else:
            keys = tuple(keys)
        results = {}
        position = self.tell()
        advance = 0
        for key in keys:
            component = self.registered_components[key]
            try:
                results[key] = self._parse_component(key, source, num=num)
                if not automatic and not reset and component["mode"] == "Single" and results[key] is not None:
                    pattern = component.get("block_pattern")
                    if pattern is not None:
                        match = pattern.search(source)
                        if match is not None:
                            advance = max(advance, match.end())
                    else:
                        with StringStreamReader(source) as reader:
                            reader.get_tagged_block(component.get("tag_start"), component.get("tag_end"))
                            advance = max(advance, reader.tell())
            except Exception as exc:
                raise GaussianLogReaderException("failed to parse block for key '{}'".format(key)) from exc
        if advance:
            encoding = getattr(self.stream, "_encoding", "utf-8")
            self.seek(position + len(source[:advance].encode(encoding)))
        return results

    def parse_jobs(self, keys=None, num=None, include_all_fields=False):
        """Read each linked job separately, preserving the stream position.

        Each item contains route/config/job_types/status, a data dictionary,
        available_fields, and omitted_fields. Offsets are decoded text offsets.
        """
        if num is not None and (not isinstance(num, int) or isinstance(num, bool) or num < 0):
            raise ValueError("num must be a nonnegative integer or None")
        from .GaussianLogTools import gaussian_job_metadata
        source = self._read_source(from_start=True)
        jobs = gaussian_job_metadata(source)
        explicit = None if keys is None else ((keys,) if isinstance(keys, str) else tuple(keys))
        for job in jobs:
            section = source[job["start"]:job["end"]]
            available = self._default_keys(section, True)
            selected = self._default_keys(section, include_all_fields) if explicit is None else explicit
            # Avoid recursively duplicating file-wide job metadata per job.
            selected = tuple(k for k in selected if k != "Jobs")
            job["available_fields"] = available
            job["omitted_fields"] = tuple(k for k in available if k not in selected and k != "Jobs")
            job["data"] = {}
            for key in selected:
                try:
                    job["data"][key] = self._parse_component(key, section, num=num)
                except Exception as exc:
                    raise GaussianLogReaderException("failed to parse block for key '{}' in job {}".format(key, job["index"])) from exc
        return jobs

    def to_archive(self, keys=None, num=None, include_all_fields=False, source=None):
        """Build a Scaffolding NumpyTreeArchive of all linked jobs.

        Job records use zero-based string keys: archive["jobs/0/data"]. Large
        fields remain opt-in. The reader position is preserved.
        """
        from .GaussianLogNPZ import _reader_archive
        return _reader_archive(self, keys=keys, num=num,
                               include_all_fields=include_all_fields, source=source)

    def to_npz(self, output_file, keys=None, num=None, include_all_fields=False,
               compress=True, overwrite=False, source=None):
        """Save linked jobs to one nested .npz and return its path."""
        from .GaussianLogNPZ import _save_archive
        archive = self.to_archive(keys=keys, num=num,
                                  include_all_fields=include_all_fields, source=source)
        return _save_archive(archive, output_file, compress=compress, overwrite=overwrite)

    @classmethod
    def export_npz(cls, file, output_file=None, **options):
        """Convert a log to .npz using read-only input access.

        Default output replaces the input suffix with .npz. Options are keys,
        num, include_all_fields, compress, overwrite and encoding. The output
        uses Scaffolding.NumpyTreeArchive and never requires pickle.
        """
        from .GaussianLogNPZ import export_gaussian_log
        return export_gaussian_log(file, output_file, reader_type=cls, **options)

    @classmethod
    def read_props(cls, file, keys=None, **kwargs):
        """Open a log and read automatic or explicitly selected fields."""
        with cls(file) as reader:
            result = reader.parse(keys, **kwargs)
        return result[keys] if isinstance(keys, str) else result

########################################################################################################################
#
#                                           GaussianFChkReader
#
class GaussianFChkReaderException(FileStreamReaderException):
    pass

class GaussianFChkReader(FileStreamReader):
    """Implements a stream based reader for a Gaussian .fchk file. Pretty generall I think. Should be robust-ish.
    One place to change things up is convenient parsers for specific commonly pulled parts of the fchk

    """

    GaussianFChkReaderException = GaussianFChkReaderException
    registered_components = FormattedCheckpointComponents
    common_names = {to_:from_ for from_, to_ in FormattedCheckpointCommonNames.items()}
    to_common_name = FormattedCheckpointCommonNames

    def to_readout(self, keys=None, **opts):
        """
        **LLM Docstring**

        Build a `Readout` of parsed results (`GaussianFChkReadout`); ``keys`` limits what is parsed.

        :param opts: `ReadoutInterface.to_readout` options (``include``, ``exclude``, ``units``, ...)
        :return: the readout
        :rtype: McUtils.Jupyter.Readouts.Readout
        """
        from ..Readouts.ElectronicStructure import GaussianFChkReadout
        return GaussianFChkReadout.from_reader(self, keys=keys).to_readout(**opts)

    def __init__(self, file, **kwargs):
        """
        **LLM Docstring**

        Open a Gaussian `.fchk` file for stream reading.

        :param file: the `.fchk` file
        :type file: str
        :param kwargs: extra arguments for the stream reader
        """
        super().__init__(file, **kwargs)
        self._num_atoms = None
        # with self: self.num_atoms = self.parse("Number of atoms")["Number of atoms"]

    def read_header(self):
        """Reads the header and skips the stream to where we want to be

        :return: the header
        :rtype: str
        """
        return self.get_tagged_block(None, "Number of atoms")

    fchk_re_pattern = r"^(.+?)\s+(I|R|C|H)\s+(N=)?\s+(.+)\s+" # matches name, type, num (if there), and val
    fchk_re = re.compile(fchk_re_pattern)
    def get_next_block_params(self):
        """Pulls the tag of the next block, the type, the number of bytes it'll be,
        and if it's a single-line block it'll also spit back the block itself

        :return:
        :rtype: dict
        """
        with FileStreamCheckPoint(self):
            tag_line = self.readline()
            if tag_line == b'' or tag_line == '':
                return None
            match = re.match(self.fchk_re, tag_line)
            if match is None:
                with FileStreamCheckPoint(self):
                    for i in range(4):
                        prev_lines = self.rfind("\n")
                        self.seek(prev_lines)
                    lines = "".join(self.readline() for i in range(4))
                    raise GaussianFChkReaderException("{}.{}: line '{}' couldn't be read as a tag line (in '{}')".format(
                        type(self).__name__,
                        "get_next_block_params",
                        tag_line,
                        lines
                    ))
            jump = self.tell()
        self.seek(jump)

        name, btype, numQ, val = gg = match.groups()
        # print(gg)
        if numQ:
            byte_count = 0
            shits = int(val)
            # hard coded these block formats since they're documented by Gaussian and thus unlikely to change
            if btype == "I":
                byte_per_shit = 12
                shits_per_line = 6
                btype = int
            elif btype == "R":
                byte_per_shit = 16
                shits_per_line = 5
                btype = float
            elif btype == "C":
                byte_per_shit = 12
                shits_per_line = 5
                btype = str
            elif btype == "L":
                byte_per_shit = 12
                shits_per_line = 5
                btype = bool
            byte_count = shits * byte_per_shit + math.ceil( shits / shits_per_line ) # each newline needs a byte
        else:
            byte_count = None
            if btype == "I":
                val = int(val)
            elif btype == "R":
                val = float(val)
            elif btype == "L":
                val = bool(int(val))

        return {
            "name": name,
            "dtype": btype,
            "byte_count": byte_count,
            "value": val
        }

    def get_block(self, name = None, dtype = None, byte_count = None, value = None):
        """Pulls the next block by first pulling the block tag

        :return:
        :rtype:
        """

        if byte_count is not None:

            block_str = self.read(byte_count)
            if dtype in {int, float}:
                block_str = io.StringIO(block_str.replace("\n", "")) # flatten it out
                value = np.loadtxt(block_str)
                if dtype == int:
                    value = value.astype(np.int64)
            else:
                value = block_str

        # try:
        parser = self.registered_components.get(name, None)
        if parser is not None:
            value = parser(value, reader=self)
        # except KeyError:
        #     pass

        return value

    def skip_block(self, name = None, dtype = None, byte_count = None, value = None):
        """Skips the next block

        :return:
        :rtype:
        """

        if byte_count is not None:
            self.seek(self.tell() + byte_count)

    @property
    def num_atoms(self):
        """
        **LLM Docstring**

        The number of atoms in the file, parsed (and cached) from the `Number of atoms`
        block on first access.

        :return: the atom count
        :rtype: int
        """
        if self._num_atoms is None:
            self._num_atoms = self.parse(["Number of atoms"])["Number of atoms"]
        return self._num_atoms
    def parse(self, keys=None, default='raise'):
        """
        **LLM Docstring**

        Parse the requested blocks out of the `.fchk` file (or every block when no keys
        are given), resolving common-name aliases and skipping unrequested blocks.

        Malformed blocks are skipped where possible; when a requested key can't be found,
        either raises or fills in `default` depending on the `default` argument.

        :param keys: the block key(s) to read (all if omitted)
        :type keys: str | Iterable[str] | None
        :param default: value to use for missing keys, or `'raise'` to error
        :type default: Any
        :return: the parsed blocks keyed by name
        :rtype: dict
        """
        if keys is None:
            keys_to_go = None
        else:
            if isinstance(keys, str):
                keys = (keys,)
            keys_original = set(keys)
            keys_to_go = { (self.common_names[k] if k in self.common_names else k) for k in keys }

        parse_results = {}
        header = self.read_header()
        if self._num_atoms is None:
            self._num_atoms = self.get_block(**self.get_next_block_params())
        parse_results["Number of atoms"] = self._num_atoms

        parse_results['Header'] = header
        if keys_to_go is None:
            while True: # I'll just break once I've exhausted everything
                next_block = self.get_next_block_params()
                if next_block is None:
                    break
                tag = next_block["name"]
                parse_results[tag] = self.get_block(**next_block)
        else:
            while len(keys_to_go)>0:
                # try to skip malformatted blocks...
                try:
                    next_block = self.get_next_block_params()
                except GaussianFChkReaderException:
                    fp = self.find("\n")
                    if fp == -1:
                        next_block = None
                    else:
                        next_block = ""
                        self.seek(fp + 1)
                    while next_block is not None and next_block == "":
                        try:
                            next_block = self.get_next_block_params()
                        except GaussianFChkReaderException:
                            fp = self.find("\n")
                            if fp == -1:
                                next_block = None
                            else:
                                self.seek(fp + 1)

                if next_block is None:
                    if isinstance(default, str) and default == 'raise':
                        raise GaussianFChkReaderException("{}.{}: couldn't find keys {}".format(
                            type(self).__name__,
                            "parse",
                            keys_to_go
                            )
                        )
                    else:
                        for tag in keys_to_go:
                            if tag not in keys_original:
                                tag = self.to_common_name[tag]
                            parse_results[tag] = default
                        break
                tag = next_block["name"]
                if tag in keys_to_go:
                    keys_to_go.remove(tag)
                    if tag not in keys_original:
                        tag = self.to_common_name[tag]
                    parse_results[tag] = self.get_block(**next_block)
                else:
                    self.skip_block(**next_block)

        return parse_results

    @classmethod
    def read_props(cls, file, keys):
        """
        **LLM Docstring**

        Convenience classmethod: open `file`, parse the requested keys, and return the
        result (unwrapped to the single value when one key is given).

        :param file: the `.fchk` file
        :type file: str
        :param keys: the block key(s) to read
        :type keys: str | list[str]
        :return: the parsed data
        :rtype: dict | Any
        """
        with cls(file) as reader:
            parse = reader.parse(keys)
        if isinstance(keys, str):
            parse = parse[keys]
        return parse
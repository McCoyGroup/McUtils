"""
Documentation examples that produce readouts.

An example is an ordinary fenced ``python`` block in documentation Markdown that is
*opted in* by an HTML comment on the line above it::

    <!-- readout(id="water-modes", include=["overview", "normal_modes"]) -->
    ```python
    mol = Molecule.from_file("water.fchk")
    mol
    ```

The comment is invisible in ordinary Markdown renderers, so unprocessed docs still read normally.
Blocks without the marker are plain code and are never executed.

The pieces:

* `ExampleParser` finds marked blocks (without executing anything), parses the marker options with
  `ast` (literals only, no `eval`), and computes a **chained MD5 key** for each block.
* `ReadoutStore` is the on-disk export point: one directory per key plus a ``manifest.json``.
* `ExampleCache` decides which blocks need to be (re)generated.
* `ExampleRunner` executes the blocks that need it (in-process), turns the value of the last
  expression into a `Readout` (`value_to_readout`), and writes the result to the store.
  `ExampleView` is the single place that turns an example's outcome into a readout, so the
  documentation build and `jdoc` render the same thing.

Importing this module does not import the plotting/Jupyter stack; that is loaded lazily when a
readout is actually built. Only `ExampleRunner` executes example code.

The rest of the pipeline lives in this file too, in order:

* `ExamplesParser` turns a unit-test file into examples Markdown (the source of the marked blocks).
* `ExampleEmbedder` / `ExampleCollector` (``examples_processor`` of a `DocWalker`) put the stored output into
  pages **without running anything**, and `publish_readouts` copies the store next to the built pages.
* `SubprocessExampleRunner` runs a page in a worker process (`run_worker`), so a crash, hang or ``sys.exit`` in
  an example can't take the build down.
* `LiveExamplePage` runs the marked blocks on demand in a notebook (``jdoc``'s **Run** buttons), through the same
  `ExampleView` the build uses.
"""

import ast, collections, contextlib, datetime, fnmatch, hashlib, html, importlib, inspect, io, json, linecache, os, \
    queue, random, re, shutil, signal, subprocess, sys, tempfile, threading, time, traceback

__all__ = [
    "ExampleMarkerError",
    "ExampleBlock",
    "ParsedExamples",
    "ExampleParser",
    "ReadoutStore",
    "ExampleCache",
    "ExampleError",
    "ExampleTimeout",
    "ExampleResult",
    "ExampleView",
    "ExampleRunner",
    "value_to_readout",
    "ExamplesParser",
    "ExampleEmbedError",
    "ExampleEmbedder",
    "ExampleCollector",
    "publish_readouts",
    "ExampleWorkerError",
    "ExampleWorkerCrash",
    "SubprocessExampleRunner",
    "run_worker",
    "LiveExamplePage",
    "LiveExampleResult",
    "split_examples",
]


class ExampleMarkerError(ValueError):
    """
    Raised when a ``<!-- readout(...) -->`` marker is malformed or isn't followed by a Python fence.
    """


# --------------------------------------------------------------------------------------------- #
# marker options
# --------------------------------------------------------------------------------------------- #

def _check_id(v):
    if not isinstance(v, str) or not re.fullmatch(r"[A-Za-z0-9_.#:/-]+", v):
        raise ExampleMarkerError("`id` must be a string of letters, digits and `_.#:/-`, got {!r}".format(v))
    return v

def _check_include(v):
    if v is None or isinstance(v, (str, bool)):
        return v
    if isinstance(v, (list, tuple)) and all(isinstance(x, str) for x in v):
        return list(v)
    if isinstance(v, dict) and all(isinstance(k, str) for k in v):
        return v
    raise ExampleMarkerError(
        "`include`/`exclude` must be None, a string, a list of strings or a dict, got {!r}".format(v)
    )

def _check_units_style(v):
    if v is None or isinstance(v, (str, dict)):
        return v
    raise ExampleMarkerError("`units`/`style` must be None, a string or a dict, got {!r}".format(v))

def _check_bool(v):
    if not isinstance(v, bool):
        raise ExampleMarkerError("expected True or False, got {!r}".format(v))
    return v

def _check_choice(*choices):
    def check(v):
        if v not in choices:
            raise ExampleMarkerError("expected one of {}, got {!r}".format(list(choices), v))
        return v
    return check

def _check_timeout(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or v <= 0:
        raise ExampleMarkerError("`timeout` must be a positive number of seconds, got {!r}".format(v))
    return v


class _Option:
    def __init__(self, check, affects_output):
        self.check = check
        self.affects_output = affects_output


_OPTIONS = collections.OrderedDict([
    # name: validator, does it change what the example *produces* (and so belong in the cache key)?
    ("id",       _Option(_check_id, False)),
    ("include",  _Option(_check_include, True)),
    ("exclude",  _Option(_check_include, True)),
    ("units",    _Option(_check_units_style, True)),
    ("style",    _Option(_check_units_style, True)),
    ("display",  _Option(_check_choice("readout", "output", "both", "none"), True)),
    ("css",      _Option(_check_choice("inline", "stylesheet"), True)),
    ("show_trivial", _Option(_check_bool, True)),
    ("isolated", _Option(_check_bool, False)),
    ("timeout",  _Option(_check_timeout, False)),
])


def _parse_marker_options(args_text, where):
    """
    Parses the text inside ``readout( ... )`` into a validated dict.

    Only keyword arguments with literal values are accepted (via `ast.literal_eval`); a single
    positional string is accepted as shorthand for ``id=``.
    """
    try:
        call = ast.parse("readout({})".format(args_text), mode="eval").body
    except SyntaxError as e:
        raise ExampleMarkerError("{}: could not parse marker options {!r}: {}".format(where, args_text, e.msg))
    options = collections.OrderedDict()
    if len(call.args) > 1 or any(isinstance(a, ast.Starred) for a in call.args):
        raise ExampleMarkerError("{}: at most one positional argument (the id) is allowed".format(where))
    if len(call.args) == 1:
        try:
            options["id"] = _check_id(ast.literal_eval(call.args[0]))
        except ValueError as e:
            raise ExampleMarkerError("{}: {}".format(where, e))
    for kw in call.keywords:
        if kw.arg is None:
            raise ExampleMarkerError("{}: `**` expansion is not allowed in markers".format(where))
        if kw.arg not in _OPTIONS:
            raise ExampleMarkerError(
                "{}: unknown option `{}`; valid options are {}".format(where, kw.arg, list(_OPTIONS))
            )
        if kw.arg in options:
            raise ExampleMarkerError("{}: option `{}` given twice".format(where, kw.arg))
        try:
            value = ast.literal_eval(kw.value)
        except ValueError:
            raise ExampleMarkerError("{}: option `{}` must be a literal".format(where, kw.arg))
        try:
            options[kw.arg] = _OPTIONS[kw.arg].check(value)
        except ExampleMarkerError as e:
            raise ExampleMarkerError("{}: option `{}`: {}".format(where, kw.arg, e))
    return options


# --------------------------------------------------------------------------------------------- #
# keys
# --------------------------------------------------------------------------------------------- #

KEY_VERSION = "mcr-example-v1"


def normalize_source(source):
    """
    The bytes that get hashed: the block's source with CRLF/CR line endings converted to LF and
    exactly one trailing newline. Everything else (indentation, tabs, comments, blank lines) matters.
    """
    source = source.replace("\r\n", "\n").replace("\r", "\n")
    return source.rstrip("\n") + "\n"


def key_options(options):
    """The subset of marker options that change what an example produces, in a canonical order."""
    return collections.OrderedDict(
        (k, options[k]) for k in _OPTIONS if k in options and _OPTIONS[k].affects_output
    )


def compute_key(source, options, prev_key=""):
    """
    ``md5(version, previous key, canonical output-affecting options, normalized source bytes)``.

    ``id``, ``timeout`` and ``isolated`` are *not* hashed, so renaming an example or changing its
    time budget doesn't invalidate it; ``isolated`` acts by passing ``prev_key=""``.
    """
    h = hashlib.md5()
    h.update(KEY_VERSION.encode("utf-8") + b"\0")
    h.update((prev_key or "").encode("ascii") + b"\0")
    h.update(json.dumps(key_options(options), sort_keys=True, separators=(",", ":"),
                        default=repr).encode("utf-8") + b"\0")
    h.update(normalize_source(source).encode("utf-8"))
    return h.hexdigest()


# --------------------------------------------------------------------------------------------- #
# blocks and parsing
# --------------------------------------------------------------------------------------------- #

class ExampleBlock:
    """
    One marked example.

    :ivar index: zero-based position among the marked blocks of the page
    :ivar id: the explicit ``id`` option, else ``"<owner>#<index+1>"``
    :ivar options: the options given in the marker (validated)
    :ivar source: the code inside the fence
    :ivar key: the chained MD5 hex digest
    :ivar prev_key: the key of the previous block in the chain (``""`` for the first or an isolated block)
    :ivar line: one-based line number of the marker in the parsed text (offset by ``first_line``)
    :ivar raw: the original text of the marker through the closing fence
    :ivar marker: the original marker comment
    :ivar owner: the name of the documented object, if given
    """

    def __init__(self, index, options, source, raw, marker, fence_info, line, owner=None, id=None):
        self.index = index
        self.options = options
        self.source = normalize_source(source)
        self.raw = raw
        self.marker = marker
        self.fence_info = fence_info
        self.line = line
        self.owner = owner
        self.id = id
        self.prev_key = ""
        self.key = None

    @property
    def isolated(self):
        return bool(self.options.get("isolated", False))

    @property
    def fence(self):
        """The block's code fence as Markdown (its original text without the marker comment), ending in a newline."""
        fence = self.raw[len(self.marker):].lstrip("\r\n")
        return fence if fence.endswith("\n") else fence + "\n"

    def __repr__(self):
        return "{}(id={!r}, key={}, line={})".format(
            type(self).__name__, self.id, None if self.key is None else self.key[:8], self.line
        )


class ParsedExamples:
    """
    The result of parsing a page: the original text split into plain-text pieces and `ExampleBlock`s.
    ``str(parsed)`` reproduces the input exactly. ``owner`` and ``first_line`` are what the page was
    parsed with, so it can be re-parsed elsewhere (e.g. in a worker process) with the same ids.
    """

    def __init__(self, segments, owner=None, first_line=1):
        self.segments = segments
        self.owner = owner
        self.first_line = first_line

    @property
    def blocks(self):
        return [s for s in self.segments if isinstance(s, ExampleBlock)]

    def __str__(self):
        return "".join(s.raw if isinstance(s, ExampleBlock) else s for s in self.segments)

    def render(self, replace):
        """
        Rebuilds the text with each block's marker+fence replaced by ``replace(block)``.
        """
        return "".join(replace(s) if isinstance(s, ExampleBlock) else s for s in self.segments)

    def chain(self, block):
        """
        The blocks that must be executed, in order, to produce ``block``'s namespace: every
        earlier block back to the most recent isolated block (or the page start), then ``block``.
        """
        blocks = self.blocks
        i = blocks.index(block)
        start = i
        while start > 0 and not blocks[start].isolated:
            start -= 1
        return blocks[start:i + 1]


_FENCE_OPEN = re.compile(r"^( {0,3})(`{3,}|~{3,})[ \t]*([^\s`]*)[^`]*$")
_PYTHON_LANGS = {"python", "py", "python3"}


class ExampleParser:
    """
    Finds ``<!-- readout(...) -->``-marked Python fences in Markdown text.

    Fences are tracked line by line, so a marker shown *inside* some other code fence (for example
    in docs about this feature) is never treated as a marker.
    """

    marker_start = re.compile(r"^[ \t]*<!--[ \t\n]*readout\b")

    @classmethod
    def has_markers(cls, text):
        """Cheap check for whether ``text`` contains a line that starts a ``readout(...)`` marker."""
        return isinstance(text, str) and "readout" in text and any(
            cls.marker_start.match(line) for line in text.splitlines()
        )

    @classmethod
    def parse(cls, text, owner=None, first_line=1):
        """
        :param text: Markdown text (a docstring `:examples:` field, an examples file, ...)
        :param owner: name of the documented object, used for default ids and error messages
        :param first_line: line number of the first line of ``text`` in its file, for messages/manifest
        :return: the parsed page
        :rtype: ParsedExamples
        :raises ExampleMarkerError: for malformed markers or duplicate ids
        """
        lines = text.splitlines(keepends=True)
        segments = []
        pending = []  # plain text lines not yet flushed
        blocks = []
        i = 0
        n = len(lines)

        def flush():
            if pending:
                segments.append("".join(pending))
                del pending[:]

        def where(lineno):
            return "{}line {}".format("" if owner is None else "{}, ".format(owner), lineno)

        while i < n:
            line = lines[i]
            m = _FENCE_OPEN.match(line.rstrip("\r\n"))
            if m is not None:
                # copy an unmarked fence verbatim, so markers inside it are inert
                fence = m.group(2)
                j = i + 1
                while j < n:
                    stripped = lines[j].rstrip("\r\n")
                    if re.match(r"^ {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}[ \t]*$", stripped):
                        break
                    j += 1
                pending.extend(lines[i:j + 1])
                i = j + 1
                continue
            if cls.marker_start.match(line):
                start = i
                marker_lines = [line]
                k = i
                while "-->" not in lines[k]:
                    k += 1
                    if k >= n:
                        raise ExampleMarkerError("{}: unterminated readout marker".format(where(first_line + start)))
                    marker_lines.append(lines[k])
                marker = "".join(marker_lines)
                body = marker.strip()
                body = body[len("<!--"):body.index("-->")].strip()
                rest = body[len("readout"):].strip()
                if rest == "":
                    args = ""
                elif rest.startswith("(") and rest.endswith(")"):
                    args = rest[1:-1]
                else:
                    raise ExampleMarkerError(
                        "{}: expected `readout(...)` or `readout`, got `{}`".format(where(first_line + start), body)
                    )
                options = _parse_marker_options(args, where(first_line + start))
                # the next non-blank line must open a python fence
                f = k + 1
                while f < n and lines[f].strip() == "":
                    f += 1
                fm = _FENCE_OPEN.match(lines[f].rstrip("\r\n")) if f < n else None
                if fm is None:
                    raise ExampleMarkerError(
                        "{}: a readout marker must be followed by a fenced code block".format(where(first_line + start))
                    )
                lang = fm.group(3).lower()
                if lang.split("{")[0] not in _PYTHON_LANGS:
                    raise ExampleMarkerError(
                        "{}: a readout marker must precede a ```python block, got `{}`".format(
                            where(first_line + start), lang or "(no language)"
                        )
                    )
                fence = fm.group(2)
                close = f + 1
                while close < n:
                    stripped = lines[close].rstrip("\r\n")
                    if re.match(r"^ {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}[ \t]*$", stripped):
                        break
                    close += 1
                else:
                    raise ExampleMarkerError(
                        "{}: unterminated code fence after readout marker".format(where(first_line + f))
                    )
                source = "".join(lines[f + 1:close])
                indent = len(fm.group(1))
                if indent:
                    source = "".join(l[indent:] if l[:indent].strip() == "" else l for l in source.splitlines(True))
                raw = "".join(lines[start:close + 1])
                flush()
                block = ExampleBlock(
                    len(blocks), options, source, raw, marker, fm.group(3), first_line + start, owner=owner
                )
                blocks.append(block)
                segments.append(block)
                i = close + 1
                continue
            pending.append(line)
            i += 1
        flush()

        cls._assign_ids_and_keys(blocks, owner, first_line)
        return ParsedExamples(segments, owner=owner, first_line=first_line)

    @staticmethod
    def _assign_ids_and_keys(blocks, owner, first_line):
        seen = {}
        prev = ""
        for b in blocks:
            b.id = b.options.get("id", "{}#{}".format("example" if owner is None else owner, b.index + 1))
            if b.id in seen:
                raise ExampleMarkerError(
                    "duplicate example id `{}` (lines {} and {})".format(b.id, seen[b.id], b.line)
                )
            seen[b.id] = b.line
            b.prev_key = "" if b.isolated else prev
            b.key = compute_key(b.source, b.options, b.prev_key)
            prev = b.key


# --------------------------------------------------------------------------------------------- #
# store
# --------------------------------------------------------------------------------------------- #

class ReadoutStore:
    """
    The on-disk export point for generated example output.

    Layout (``root`` is committed to the repository)::

        root/manifest.json              id -> key/owner/line/status, sorted for stable diffs
        root/<key[:2]>/<key>/meta.json  status, options, timings, revisions, ...
        root/<key[:2]>/<key>/<files>    fragment.html, readout.json, readout.txt, assets/...

    Entries are content addressed, so identical examples share an entry. Writes go to a temporary
    directory that is renamed into place, so an interrupted build never leaves a half-written entry.
    """

    manifest_name = "manifest.json"
    meta_name = "meta.json"
    format_version = 1

    def __init__(self, root):
        self.root = os.fspath(root)

    # ---- entries ---- #
    @staticmethod
    def _check_key(key):
        if not re.fullmatch(r"[0-9a-f]{32}", key or ""):
            raise ValueError("not an example key: {!r}".format(key))
        return key

    def entry_path(self, key, *parts):
        self._check_key(key)
        return os.path.join(self.root, key[:2], key, *parts)

    def has(self, key):
        return os.path.isfile(self.entry_path(key, self.meta_name))

    def has_file(self, key, name):
        return os.path.isfile(self.entry_path(key, self._check_filename(name)))

    def read_meta(self, key):
        path = self.entry_path(key, self.meta_name)
        if not os.path.isfile(path):
            return None
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _check_filename(name):
        parts = name.replace("\\", "/").split("/")
        if name == "" or os.path.isabs(name) or ".." in parts or "" in parts:
            raise ValueError("invalid entry file name: {!r}".format(name))
        return name

    def write(self, key, meta, files=None):
        """
        Writes (replacing) the entry for ``key``.

        :param meta: JSON-able metadata; ``key``, ``written`` and ``store_version`` are added
        :param files: mapping of relative file name (``/`` allowed for subdirectories) to ``str``/``bytes``
        :return: the entry directory
        """
        self._check_key(key)
        final = self.entry_path(key)
        tmp = os.path.join(self.root, ".tmp-{}-{}".format(key, os.getpid()))
        if os.path.isdir(tmp):
            shutil.rmtree(tmp)
        os.makedirs(tmp)
        try:
            full_meta = dict(meta, key=key, store_version=self.format_version,
                             written=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
            for name, data in (files or {}).items():
                self._check_filename(name)
                if name == self.meta_name:
                    raise ValueError("`{}` is reserved".format(self.meta_name))
                path = os.path.join(tmp, *name.split("/"))
                os.makedirs(os.path.dirname(path), exist_ok=True)
                if isinstance(data, str):
                    with open(path, "w", encoding="utf-8", newline="\n") as f:
                        f.write(data)
                else:
                    with open(path, "wb") as f:
                        f.write(data)
            with open(os.path.join(tmp, self.meta_name), "w", encoding="utf-8", newline="\n") as f:
                json.dump(full_meta, f, indent=2, sort_keys=True)
                f.write("\n")
            os.makedirs(os.path.dirname(final), exist_ok=True)
            if os.path.isdir(final):
                shutil.rmtree(final)
            os.replace(tmp, final)
        finally:
            if os.path.isdir(tmp):
                shutil.rmtree(tmp)
        return final

    def read_file(self, key, name, binary=False):
        self._check_filename(name)
        path = self.entry_path(key, *name.split("/"))
        with open(path, "rb" if binary else "r", **({} if binary else {"encoding": "utf-8"})) as f:
            return f.read()

    def keys(self):
        """All keys present in the store."""
        found = []
        if os.path.isdir(self.root):
            for shard in sorted(os.listdir(self.root)):
                sp = os.path.join(self.root, shard)
                if len(shard) == 2 and os.path.isdir(sp):
                    for key in sorted(os.listdir(sp)):
                        if key.startswith(shard) and os.path.isfile(os.path.join(sp, key, self.meta_name)):
                            found.append(key)
        return found

    def prune(self, keep_keys, dry_run=False):
        """
        Removes entries whose key is not in ``keep_keys`` (and empty shard directories).

        :return: the keys that were (or, with ``dry_run``, would be) removed
        """
        keep = set(keep_keys)
        doomed = [k for k in self.keys() if k not in keep]
        if not dry_run:
            for k in doomed:
                shutil.rmtree(self.entry_path(k))
                shard = os.path.dirname(self.entry_path(k))
                if not os.listdir(shard):
                    os.rmdir(shard)
        return doomed

    # ---- shared stylesheet ---- #
    stylesheet_name = "mcr.css"

    def write_stylesheet(self, css):
        """Writes the shared ``mcr.css`` (for ``css='stylesheet'``); returns whether the file changed."""
        path = os.path.join(self.root, self.stylesheet_name)
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                if f.read() == css:
                    return False
        os.makedirs(self.root, exist_ok=True)
        tmp = path + ".tmp-{}".format(os.getpid())
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write(css)
        os.replace(tmp, path)
        return True

    def stylesheet_md5(self):
        """MD5 of the stored ``mcr.css``, or ``None`` if there isn't one."""
        path = os.path.join(self.root, self.stylesheet_name)
        if not os.path.isfile(path):
            return None
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    # ---- manifest ---- #
    def load_manifest(self):
        path = os.path.join(self.root, self.manifest_name)
        if not os.path.isfile(path):
            return {"version": self.format_version, "entries": {}}
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def update_manifest(self, entries, drop=()):
        """
        Merges ``entries`` (id -> dict) into ``manifest.json`` and removes the ids in ``drop``.
        The file is only rewritten if its content changes, to keep git diffs quiet.

        :return: whether the file was rewritten
        """
        manifest = self.load_manifest()
        current = manifest.setdefault("entries", {})
        for k in drop:
            current.pop(k, None)
        current.update(entries)
        text = json.dumps(
            {"version": self.format_version, "entries": current}, indent=2, sort_keys=True
        ) + "\n"
        path = os.path.join(self.root, self.manifest_name)
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                if f.read() == text:
                    return False
        os.makedirs(self.root, exist_ok=True)
        tmp = path + ".tmp-{}".format(os.getpid())
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        os.replace(tmp, path)
        return True


# --------------------------------------------------------------------------------------------- #
# cache policy
# --------------------------------------------------------------------------------------------- #

class ExampleCache:
    """
    Decides which blocks have to be (re)generated, without running anything.

    Statuses: ``"missing"`` (no entry), ``"ok"``, ``"error"`` (the stored run failed; errors are cached
    so a broken example isn't re-run on every build) and ``"stale"`` (an ``ok`` entry recorded against
    different library revisions than ``revisions``).
    """

    def __init__(self, store, revisions=None):
        """
        :param store: the `ReadoutStore`
        :param revisions: ``{package: revision}`` for the code in use now; ``None`` disables staleness checks
        """
        self.store = store
        self.revisions = revisions

    def status(self, block):
        meta = self.store.read_meta(block.key)
        if meta is None:
            return "missing"
        if meta.get("status") == "error":
            return "error"
        if self.revisions:
            recorded = meta.get("revisions") or {}
            if any(recorded.get(k) != v for k, v in self.revisions.items()):
                return "stale"
        return "ok"

    def plan(self, blocks, refresh=False):
        """
        :param blocks: blocks to consider
        :param refresh: ``False`` (only missing entries), ``"stale"`` (missing and stale), ``"errors"`` (missing and
                        failed: retry what failed), ``True``/``"all"`` (everything), or a glob / list of globs over block ids (those, plus missing entries)
        :return: ``[(block, reason), ...]`` in page order; reasons are ``"missing"``, ``"stale"``,
                 ``"refresh"``, ``"retry"``. Executing a block also requires replaying the earlier blocks of its chain
                 (`ParsedExamples.chain`); the plan lists only the blocks whose *output* must be produced.
        """
        if refresh is True or refresh == "all":
            return [(b, "refresh") for b in blocks]
        errors = False
        if refresh is False or refresh is None:
            globs = []
            stale = False
        elif refresh == "stale":
            globs = []
            stale = True
        elif refresh == "errors":
            globs = []
            stale = False
            errors = True
        else:
            globs = [refresh] if isinstance(refresh, str) else list(refresh)
            stale = False
        todo = []
        for b in blocks:
            status = self.status(b)
            if status == "missing":
                todo.append((b, "missing"))
            elif globs and any(fnmatch.fnmatchcase(b.id, g) for g in globs):
                todo.append((b, "refresh"))
            elif stale and status == "stale":
                todo.append((b, "stale"))
            elif errors and status == "error":
                todo.append((b, "retry"))
        return todo

    def report(self, blocks):
        """``{status: [block ids]}`` for all blocks, e.g. for ``--status`` output."""
        out = collections.OrderedDict((s, []) for s in ("ok", "stale", "error", "missing"))
        for b in blocks:
            out[self.status(b)].append(b.id)
        return out

    def sync_manifest(self, blocks, drop=()):
        """Records ``blocks`` in the store's ``manifest.json`` (id, key, owner, line, status)."""
        entries = {
            b.id: {"key": b.key, "owner": b.owner, "line": b.line, "status": self.status(b)}
            for b in blocks
        }
        return self.store.update_manifest(entries, drop=drop)


# --------------------------------------------------------------------------------------------- #
# running
# --------------------------------------------------------------------------------------------- #

class ExampleError(Exception):
    """An example failed in a way the runner reports (as opposed to a bug in the runner itself)."""


class ExampleTimeout(ExampleError):
    """An example exceeded its time limit."""


_NO_VALUE = object()


def _compile_block(source, filename):
    """
    Compiles ``source`` into ``(body, value)`` code objects: everything but a trailing expression
    statement, and that expression (``None`` if the block doesn't end in one, or the expression
    ends with ``;``, the notebook convention for "don't display this").
    """
    tree = ast.parse(source, filename=filename)
    value_expr = None
    stripped = source.rstrip()
    last_line = stripped.splitlines()[-1].rstrip() if stripped else ""
    if tree.body and isinstance(tree.body[-1], ast.Expr) and not last_line.endswith(";"):
        value_expr = ast.Expression(tree.body.pop().value)
        ast.fix_missing_locations(value_expr)
    body = compile(ast.Module(tree.body, type_ignores=[]), filename, "exec")
    value = compile(value_expr, filename, "eval") if value_expr is not None else None
    return body, value


@contextlib.contextmanager
def _time_limit(seconds):
    """
    Raises `ExampleTimeout` in the running code after ``seconds`` (POSIX main thread only, via
    ``SIGALRM``). Elsewhere it is a no-op; the yielded flag says whether the limit is enforced.
    """
    enforce = (seconds is not None and hasattr(signal, "setitimer")
               and threading.current_thread() is threading.main_thread())
    if not enforce:
        yield False
        return

    def handler(signum, frame):
        raise ExampleTimeout("example exceeded its time limit of {} s".format(seconds))

    old = signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield True
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)


def _clip(text, limit):
    if limit is not None and len(text) > limit:
        return text[:limit] + "\n… ({} more characters)".format(len(text) - limit)
    return text


def value_to_readout(value, options=None):
    """
    Turns the value an example produced into a `Readout`.

    Dispatch order: an existing `Readout`; an object with a registered adapter or a ``to_readout``
    method (``include``/``exclude``/``units`` from the marker are passed on); an object with
    ``_repr_html_``; otherwise the generic record view.
    """
    from ..Readouts.Interface import to_readout, find_readout_adapter
    from ..Readouts.Nodes import Readout
    from ..Readouts.Views import ReadoutHTML
    options = options or {}
    kw = {k: options[k] for k in ("include", "exclude", "units") if options.get(k) is not None}
    if isinstance(value, Readout):
        return value
    is_instance = not isinstance(value, type)
    if find_readout_adapter(value) is not None or (is_instance and hasattr(value, "to_readout")):
        return to_readout(value, **kw)
    repr_html = getattr(value, "_repr_html_", None) if is_instance else None
    if callable(repr_html):
        text = repr_html()
        if isinstance(text, str) and text.strip():
            return Readout(ReadoutHTML(text), id="html")
    return to_readout(value, **kw)


class ExampleView:
    """
    The single place an example's outcome becomes a `Readout`, shared by the documentation build
    and the interactive (``jdoc``) path so they can't drift apart.

    :param block: the `ExampleBlock`
    :param value: the value of the block's last expression (or ``_NO_VALUE``/``None``)
    :param stdout: the text the block printed
    :param to_readout: override for `value_to_readout` (a callable ``(value, options) -> Readout``)
    :param show_trivial: show readouts that say next to nothing (a bare number's one-field record, see
        `is_trivial`); ``None`` (default) defers to the block's ``show_trivial`` option, which defaults to off
    """

    def __init__(self, block, value=_NO_VALUE, stdout="", to_readout=None, max_output=20000, show_trivial=None):
        self.show_trivial = show_trivial
        self.block = block
        self.value = value
        self.stdout = stdout or ""
        self.to_readout = to_readout
        self.max_output = max_output

    @property
    def display(self):
        return self.block.options.get("display", "readout")

    @property
    def has_value(self):
        return self.value is not _NO_VALUE and self.value is not None

    @property
    def shows_trivial(self):
        if self.show_trivial is not None:
            return bool(self.show_trivial)
        return str(self.block.options.get("show_trivial", False)).lower() in ("1", "true", "yes", "on")

    def node(self, include_code=False):
        """
        The `Readout` for this example according to its ``display`` option; ``None`` for
        ``display="none"``. With ``include_code`` the example's source is shown first.

        :raises ExampleError: if the display mode needs a value or output and the block has neither
        """
        from ..Readouts.Nodes import Readout, ReadoutSection, ReadoutText
        from ..Readouts.Views import ReadoutCode
        display = self.display
        if display == "none":
            return None
        base = None
        extra = []
        if display in ("readout", "both"):
            if self.has_value:
                base = (self.to_readout or value_to_readout)(self.value, self.block.options)
            elif display == "readout":
                raise ExampleError(
                    "example `{}` produced no value to display; end the block with the object to show "
                    "(and no trailing `;`), or use display=\"output\" or display=\"none\"".format(self.block.id)
                )
        if display in ("output", "both"):
            text = self.stdout
            if text.strip():
                code = ReadoutCode(_clip(text.rstrip("\n"), self.max_output), language="text")
                extra.append(code if display == "output" else ReadoutSection(code, id="output", title="Output"))
            elif display == "output":
                extra.append(ReadoutText("This example printed nothing.", role="note"))
            elif base is None:
                raise ExampleError("example `{}` produced neither a value nor any output".format(self.block.id))
        lead = [ReadoutCode(self.block.source.rstrip("\n"), language="python")] if include_code else []
        if base is None:
            return Readout(*lead, *extra, id="example-" + self.block.key[:8])
        if not (lead or extra or self.shows_trivial):
            from ..Readouts.Renderers.Base import is_trivial
            if is_trivial(base):
                return None
        if lead or extra:
            return Readout(*lead, *base.get_children(), *extra, title=base.title, subtitle=base.subtitle,
                           units=base.units, id=base.id, meta=base.meta)
        return base

    def to_fragment(self, style=None, x3dom_path=None, css="inline"):
        """The embeddable `FragmentResult` for the site, or ``None`` for ``display="none"``."""
        node = self.node()
        return None if node is None else node.to_html_fragment(style=style, x3dom_path=x3dom_path, css=css)

    def to_element(self, mode="static", style=None, css="inline", include_code=True, **opts):
        """
        The code plus its output as an element: ``mode="static"`` (plain elements, ``.tostring()``) for
        pages, ``mode="widget"`` for Jupyter. With ``include_code=False`` only the output (``None`` for
        ``display="none"``), for hosts that already show the code.
        """
        from ..Readouts.Renderers.HTML import HTMLReadoutRenderer
        node = self.node(include_code=include_code)
        if node is None:
            return None
        return HTMLReadoutRenderer(style, mode=mode, css=css, header="auto", **opts).render_readout(node)


class ExampleResult:
    """
    The outcome of one block in `ExampleRunner.run_page`.

    :ivar status: ``"ok"``, ``"error"`` (the failure is cached in the store) or ``"blocked"`` (an earlier
        block in its chain failed; nothing is stored, so it is retried once the chain is fixed)
    :ivar meta: the metadata written to the store (``None`` for blocked blocks)
    :ivar reason: why it ran: ``"missing"``, ``"stale"`` or ``"refresh"``
    """

    def __init__(self, block, status, meta=None, reason=None, blocked_by=None):
        self.block = block
        self.status = status
        self.meta = meta
        self.reason = reason
        self.blocked_by = blocked_by

    @property
    def ok(self):
        return self.status == "ok"

    def __repr__(self):
        return "{}({!r}, {})".format(type(self).__name__, self.block.id, self.status)


_IMPLICIT_NAMES = {}


def implicit_namespace(owner):
    """
    The names an example page can use without importing them: what ``from <module> import *`` gives for the
    longest importable prefix of ``owner`` (the documented object's dotted name, e.g. ``McUtils.Zachary`` for
    ``McUtils.Zachary.FiniteDifferenceFunction.finite_difference``), plus the top-level package itself. A module
    without ``__all__`` contributes its public names. Best effort: a prefix that fails to import is skipped, and
    ``{}`` comes back for no owner or nothing importable.
    """
    if not owner:
        return {}
    if owner not in _IMPLICIT_NAMES:
        parts = owner.split(".")
        names = {}
        for n in range(len(parts), 0, -1):
            try:
                module = importlib.import_module(".".join(parts[:n]))
            except Exception:
                continue
            exported = getattr(module, "__all__", None)
            if exported is None:
                exported = [k for k in dir(module) if not k.startswith("_")]
            for k in exported:
                if isinstance(k, str) and hasattr(module, k):
                    names[k] = getattr(module, k)
            break
        try:
            names.setdefault(parts[0], importlib.import_module(parts[0]))
        except Exception:
            pass
        _IMPLICIT_NAMES[owner] = names
    return dict(_IMPLICIT_NAMES[owner])


class ExampleRunner:
    """
    Runs the example blocks that need it and writes their output to a `ReadoutStore`.

    Blocks on a page share a namespace in order (the same chain used for their keys), so producing
    one block's output replays the earlier blocks of its chain. This runner executes **in the current
    process**; the documentation build is meant to use a subprocess wrapper around it (phase 3) so a crash
    or hang in an example can't take the build down.

    :param store: the `ReadoutStore` to write to
    :param revisions: ``{package: revision}`` recorded in each entry (and used for staleness checks)
    :param style: default theme/preset for the rendered fragments (a marker's ``style`` overrides it)
    :param x3dom_path: ``None`` (default CDN) or the URL of a published X3DOM script
    :param css: default ``'inline'`` or ``'stylesheet'`` (a marker's ``css`` overrides it)
    :param seed: seed ``random`` and ``numpy.random`` from each block's key before it runs
    :param namespace: names every chain's namespace starts with
    :param imports: ``True`` (default) starts every chain with `implicit_namespace` of the page's owner, so
        examples on a module's page can use its public names without importing them (explicit imports in an
        example still work and win); ``False`` for an empty start
    :param timeout: default per-block time limit in seconds (a marker's ``timeout`` overrides it)
    :param to_readout: override for `value_to_readout`
    """

    def __init__(self, store, revisions=None, style=None, x3dom_path=None, css="inline", seed=True,
                 namespace=None, timeout=None, to_readout=None, max_output=20000, clock=time.perf_counter,
                 imports=True):
        if css not in ("inline", "stylesheet"):
            raise ValueError("css must be 'inline' or 'stylesheet'")
        self.store = store
        self.revisions = dict(revisions or {})
        self.cache = ExampleCache(store, revisions or None)
        self.style = style
        self.x3dom_path = x3dom_path
        self.css = css
        self.seed = seed
        self.namespace = dict(namespace or {})
        self.imports = imports
        self.timeout = timeout
        self.to_readout = to_readout
        self.max_output = max_output
        self.clock = clock
        self._stylesheet = None

    # ---- planning / driving ---- #
    def plan(self, parsed, refresh=False):
        return self.cache.plan(parsed.blocks, refresh)

    def run_text(self, text, owner=None, refresh=False, first_line=1):
        """Parses ``text`` and runs whatever it needs; see `run_page`."""
        return self.run_page(ExampleParser.parse(text, owner=owner, first_line=first_line), refresh=refresh)

    def analyse(self, parsed, refresh=False):
        """
        Works out what `run_page` would do, without running anything.

        :return: ``(reasons, need, doomed)``: ``{id: reason}`` for the blocks whose output is wanted; the ids
            of every block that has to execute (wanted blocks plus the earlier blocks of their chains); and
            ``{id: culprit id}`` for wanted blocks that can't be produced because an earlier block of their
            chain has a cached failure (those are reported ``blocked`` and their chains are not replayed)
        """
        blocks = parsed.blocks
        reasons = {b.id: r for b, r in self.cache.plan(blocks, refresh)}
        doomed = {}
        need = set()
        for b in blocks:
            if b.id in reasons:
                chain = parsed.chain(b)
                culprit = next((x.id for x in chain[:-1] if x.id not in reasons and self.cache.status(x) == "error"), None)
                if culprit is None:
                    need.update(x.id for x in chain)
                else:
                    doomed[b.id] = culprit
        return reasons, need, doomed

    def run_page(self, parsed, refresh=False, sync=True, on_event=None):
        """
        Generates output for the blocks `ExampleCache.plan` selects (``refresh`` as there).

        A block that only has to be replayed to rebuild a namespace, but whose stored entry is a cached
        failure, is *not* re-run: it blocks the rest of its chain instead, so a broken (or hanging)
        example costs one run, not one per build.

        :param parsed: a `ParsedExamples`
        :param sync: update ``manifest.json`` afterwards
        :param on_event: ``callback(event, block, result=None)`` called with ``"start"`` before each block
            executes and ``"result"`` with its `ExampleResult` (also for blocked blocks); used by the
            subprocess runner to report progress
        :return: `ExampleResult`s, in page order, for the blocks that were planned
        """
        blocks = parsed.blocks
        reasons, need, doomed = self.analyse(parsed, refresh)
        results = []

        def add(b, result):
            results.append(result)
            if on_event is not None:
                on_event("result", b, result)

        namespace = None
        failed = None
        for b in blocks:
            if b.index == 0 or b.isolated:
                namespace = self._new_namespace(parsed.owner)
                failed = None
            if b.id in doomed:
                add(b, ExampleResult(b, "blocked", reason=reasons[b.id], blocked_by=doomed[b.id]))
                continue
            if b.id not in need:
                continue
            planned = b.id in reasons
            if failed is None and not planned and self.cache.status(b) == "error":
                failed = b.id
            if failed is not None:
                if planned:
                    add(b, ExampleResult(b, "blocked", reason=reasons[b.id], blocked_by=failed))
                continue
            if on_event is not None:
                on_event("start", b, None)
            try:
                outcome = self._execute(b, namespace)
            except (Exception, SystemExit) as e:
                failed = b.id
                if planned:
                    add(b, self._record_error(b, e, reasons[b.id]))
                continue
            if planned:
                add(b, self._record_ok(b, outcome, reasons[b.id]))
        if self._stylesheet is not None:
            self.store.write_stylesheet(self._stylesheet)
        if sync:
            self.cache.sync_manifest(blocks)
        return results

    # ---- execution ---- #
    def new_namespace(self, owner=None):
        """A fresh namespace for a chain of blocks on the page of ``owner`` (see ``imports``)."""
        return self._new_namespace(owner)

    def execute(self, block, namespace):
        """
        Runs one block in ``namespace`` without touching the store (the interactive path).

        :return: ``{"value", "stdout", "stderr", "duration", "timeout_enforced"}``
        :raises: whatever the example raises (including `ExampleTimeout`)
        """
        return self._execute(block, namespace)

    def format_error(self, exc):
        """The user-code-only traceback text recorded for a failed example."""
        return self._format_error(exc)

    def _new_namespace(self, owner=None):
        ns = {"__name__": "__mcr_example__"}
        if self.imports:
            ns.update(implicit_namespace(owner))
        ns.update(self.namespace)
        return ns

    def _seed(self, block):
        seed = int(block.key[:8], 16)
        random.seed(seed)
        try:
            import numpy as np
        except ImportError:
            return
        np.random.seed(seed)

    def _execute(self, block, namespace):
        filename = "<example {}>".format(block.id)
        linecache.cache[filename] = (len(block.source), None, block.source.splitlines(True), filename)
        body, value_code = _compile_block(block.source, filename)
        if self.seed:
            self._seed(block)
        out, err = io.StringIO(), io.StringIO()
        value = _NO_VALUE
        start = self.clock()
        with _time_limit(block.options.get("timeout", self.timeout)) as enforced:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                exec(body, namespace)
                if value_code is not None:
                    value = eval(value_code, namespace)
        return {"value": value, "stdout": out.getvalue(), "stderr": err.getvalue(),
                "duration": self.clock() - start, "timeout_enforced": enforced}

    # ---- recording ---- #
    def _base_meta(self, block, reason):
        return {
            "id": block.id, "owner": block.owner, "line": block.line,
            "options": dict(block.options), "prev_key": block.prev_key,
            "display": block.options.get("display", "readout"),
            "python": sys.version.split()[0], "revisions": self.revisions, "reason": reason,
        }

    def _format_error(self, exc):
        here = os.path.dirname(os.path.abspath(__file__))
        frames = [f for f in traceback.extract_tb(exc.__traceback__)   # drop the example machinery's own frames
                  if not (os.path.dirname(os.path.abspath(f.filename)) == here
                          and os.path.basename(f.filename).startswith("Example"))]
        lines = ["Traceback (most recent call last):\n"] if frames else []
        lines += traceback.format_list(frames)
        lines += traceback.format_exception_only(type(exc), exc)
        return "".join(lines)

    def _record_error(self, block, exc, reason):
        meta = self._base_meta(block, reason)
        meta.update(status="error", error={
            "type": type(exc).__name__, "message": str(exc), "traceback": self._format_error(exc),
        })
        self.store.write(block.key, meta)
        return ExampleResult(block, "error", meta, reason)

    def _record_ok(self, block, outcome, reason):
        try:
            return self._record_ok_unchecked(block, outcome, reason)
        except (Exception, SystemExit) as e:
            return self._record_error(block, e, reason)

    def _record_ok_unchecked(self, block, outcome, reason):
        meta = self._base_meta(block, reason)
        files = {}
        warnings = []
        view = ExampleView(block, outcome["value"], outcome["stdout"], self.to_readout, self.max_output)
        node = view.node()
        if node is not None:
            css = block.options.get("css", self.css)
            fragment = node.to_html_fragment(
                style=block.options.get("style", self.style), x3dom_path=self.x3dom_path, css=css
            )
            if fragment.css is not None:
                digest = hashlib.md5(fragment.css.encode("utf-8")).hexdigest()
                if self._stylesheet is not None and hashlib.md5(self._stylesheet.encode("utf-8")).hexdigest() != digest:
                    raise ExampleError(
                        "css='stylesheet' publishes one shared mcr.css, but this example's style produces a "
                        "different stylesheet than an earlier one in this run"
                    )
                self._stylesheet = fragment.css
                meta["css_md5"] = digest
            files["fragment.html"] = fragment.html
            meta["fragment"] = fragment.to_dict()
            for name, make in (("readout.json", node.to_json), ("readout.txt", node.to_text)):
                try:
                    files[name] = make()
                except Exception as e:
                    warnings.append("could not write {}: {}: {}".format(name, type(e).__name__, e))
        meta.update(
            status="ok", duration=round(outcome["duration"], 4),
            timeout_enforced=outcome["timeout_enforced"],
            stdout=_clip(outcome["stdout"], self.max_output),
            warnings=warnings,
        )
        if outcome["stderr"].strip():
            meta["stderr"] = _clip(outcome["stderr"], self.max_output)
        self.store.write(block.key, meta, files)
        return ExampleResult(block, "ok", meta, reason)


# --------------------------------------------------------------------------------------------- #
# examples from unit tests
# --------------------------------------------------------------------------------------------- #

class ExamplesParser:
    """
    Provides a parser for unit tests to turn them into examples
    """

    def __init__(self, unit_tests):
        """
        **LLM Docstring**

        Parses unit-test source into an AST and initializes lazy caches.

        The constructor does not classify tests immediately; `walk_tree` populates the cached class, setup, function, and function-map fields on demand.

        :param unit_tests: the Python source containing setup code and test methods
        :type unit_tests: str
        """
        self.source = unit_tests
        self.ast = ast.parse(unit_tests)
        self._class_node = None
        self._setup = None
        self._functions = None
        self._functions_map = None
        self._node_cache = {}

    def find_setup(self, tree_iter):
        """
        **LLM Docstring**

        Consumes leading module-level setup nodes until the first class definition.

        :param tree_iter: an iterator over top-level AST nodes
        :type tree_iter: Iterator[ast.AST]
        :return: the first class node, or `None`, together with the preceding setup nodes
        :rtype: tuple[ast.ClassDef | None, list[ast.AST]]
        """
        setup = []
        for node in tree_iter:
            node_type = type(node).__name__
            if node_type not in ["ClassDef"]:
                setup.append(node)
            else:
                break
        else:
            node = None
        return node, setup

    def parse_tests(self, tree_iter):
        """
        Parses out the
        :param tree_iter:
        :type tree_iter:
        :return:
        :rtype:
        """
        class_setup = []
        functions = collections.OrderedDict()
        for node in tree_iter:
            node_type = type(node).__name__
            if node_type == 'FunctionDef':
                fname = node.name
                if fname.startswith('test_'):
                    functions[fname.split("_", 1)[1]] = node
                else:
                    class_setup.append(node)
            else:
                class_setup.append(node)
            # else:
            #     raise ValueError(
            #         "AST node of type {} with body {} not handled".format(
            #             node_type, ast.get_source_segment(self.source, node)
            #         )
            #     )
        return class_setup, functions

    def walk_tree(self):
        """
        **LLM Docstring**

        Separates module setup, class setup, and `test_` methods and refreshes all parser caches.

        This implementation assumes the first class node exists and passes its body to `parse_tests`.
        :return: the module/class setup pair and ordered mapping of example names to test nodes
        :rtype: tuple[tuple[list[ast.AST], list[ast.AST]], collections.OrderedDict[str, ast.FunctionDef]]
        """
        if hasattr(self.ast, 'body'):
            tree = self.ast.body
        else:
            tree = self.ast
        tree_iter = iter(tree)
        class_node, base_setup = self.find_setup(tree_iter)
        class_setup, functions = self.parse_tests(class_node.body)
        self._class_node = class_node
        self._setup = (base_setup, class_setup)
        self._functions = functions
        self._functions_map = self.load_function_map()
        return self._setup, self._functions

    def format_node(self, node):
        """
        **LLM Docstring**

        Returns the source text for an AST node with its original leading indentation.

        :param node: the node to format
        :type node: ast.AST
        :return: the cached source fragment
        :rtype: str
        """
        try:
            repr = self._node_cache[node]
        except KeyError:
            base = ast.get_source_segment(self.source, node)
            indent = " "*node.col_offset
            repr = indent + base
            self._node_cache[node] = repr
        return repr

    @classmethod
    def from_file(cls, tests_file):
        """
        **LLM Docstring**

        Creates a parser from a test source file.

        :param tests_file: the file to read
        :type tests_file: str | os.PathLike
        :return: a parser for the file contents
        :rtype: ExamplesParser
        """
        with open(tests_file) as f:
            return cls(f.read())

    @property
    def class_spec(self):
        """
        **LLM Docstring**

        Returns the parsed test class and its non-test setup nodes.

        Parsing is triggered lazily if necessary.
        :return: the class node and class-setup list
        :rtype: tuple[ast.ClassDef, list[ast.AST]]
        """
        if self._class_node is None:
            self.walk_tree()
        return (self._class_node, self._setup[1])
    @property
    def setup(self):
        """
        **LLM Docstring**

        Returns module-level setup nodes preceding the test class.

        Parsing is triggered lazily if necessary.
        :return: the setup-node list
        :rtype: list[ast.AST]
        """
        if self._setup is None:
            self.walk_tree()
        return self._setup[0]
    @property
    def functions(self):
        """
        **LLM Docstring**

        Returns the ordered mapping of example names to `test_` function nodes.

        The `test_` prefix is removed from each key.
        :return: the parsed test-function mapping
        :rtype: collections.OrderedDict[str, ast.FunctionDef]
        """
        if self._functions is None:
            self.walk_tree()
        return self._functions
    @property
    def functions_map(self):
        """
        **LLM Docstring**

        Returns the reverse mapping from referenced names to examples that use them.

        Parsing and map construction are triggered lazily if necessary.
        :return: the referenced-name mapping
        :rtype: dict[str, list[str]]
        """
        if self._functions is None:
            self.walk_tree()
        return self._functions_map

    def load_function_map(self):
        """
        **LLM Docstring**

        Builds a reverse index of names referenced by each parsed test function.
        :return: a mapping from referenced names to example keys
        :rtype: dict[str, list[str]]
        """
        mapping = {}
        for k,v in self._functions.items():
            for f in self.get_examples_functions(v):
                if f not in mapping:
                    mapping[f] = [k]
                else:
                    mapping[f].append(k)
        return mapping

    IGNORE_UNHANDLED_STATEMENTS = False
    def _handle_stmt(self, stmt, all_fns):
        """
        **LLM Docstring**

        Collects recognizable referenced names from one AST node.

        The traversal deliberately handles only common node shapes. Several expression forms are ignored for speed, and unrecognized forms raise unless `IGNORE_UNHANDLED_STATEMENTS` is enabled.

        :param stmt: the statement or expression to inspect
        :type stmt: ast.AST | None

        :param all_fns: the accumulator updated in place
        :type all_fns: set[str]
        """
        if hasattr(stmt, 'body'):
            all_fns.update(self.get_examples_functions(stmt))
        elif hasattr(stmt, 'names'):
            for name in stmt.names:
                if isinstance(name, str):
                    all_fns.add(name)
                else:
                    all_fns.add(name.name)
        elif hasattr(stmt, 'id'):
            name = stmt.id
            if isinstance(name, str):
                all_fns.add(name)
            else:
                all_fns.add(name.name)
        elif hasattr(stmt, 'func'):
            self._handle_stmt(stmt.func, all_fns)
            # for substmt in stmt.args:
            #     self._handle_stmt(substmt, all_fns)
        # we'll only check common patterns for speed purposes...
        elif hasattr(stmt, 'operand'):
            pass
            # self._handle_stmt(stmt.operand, all_fns)
        elif hasattr(stmt, 'right'):
            pass
            # self._handle_stmt(stmt.left, all_fns)
            # self._handle_stmt(stmt.right, all_fns)
        elif hasattr(stmt, 'comparators'):
            pass
            # self._handle_stmt(stmt.left, all_fns)
            # for v in stmt.comparators:
            #     self._handle_stmt(v, all_fns)
        elif hasattr(stmt, 'value'):
            if hasattr(stmt, 'targets'):
                # assignment
                self._handle_stmt(stmt.value, all_fns)
            else:
                node_type = type(stmt).__name__
                if node_type == 'Constant':
                    pass
                else:
                    self._handle_stmt(stmt.value, all_fns)
        elif hasattr(stmt, 'values'):
            pass
            # for v in stmt.values:
            #     self._handle_stmt(v, all_fns)
        elif hasattr(stmt, 'elts'):
            pass
            # for v in stmt.elts:
            #     self._handle_stmt(v, all_fns)
        elif (
            stmt is None
            or hasattr(stmt, 'generators')
            or hasattr(stmt, 'exc')
            or hasattr(stmt, 'targets')
        ):
            pass # for now at least...
        else:
            if self.IGNORE_UNHANDLED_STATEMENTS:
                print("IGNORING:", stmt)
            else:
                raise ValueError(f"don't know what to do with statement {stmt}")
    def get_examples_functions(self, node):
        """
        **LLM Docstring**

        Collects names referenced by a function or AST node body.

        :param node: the node whose body should be inspected
        :type node: ast.AST
        :return: the referenced-name set
        :rtype: set[str]
        """
        all_fns = set()
        try:
            for stmt in node.body:
                self._handle_stmt(stmt, all_fns)
        except TypeError:
            self._handle_stmt(node.body, all_fns)
        return all_fns

    def filter_by_name(self, name):
        """
        **LLM Docstring**

        Returns a shallow parser copy restricted to examples that reference a given name.

        :param name: the referenced function or object name
        :type name: str
        :return: a restricted parser, or `None` when no examples match
        :rtype: ExamplesParser | None
        """
        import copy
        if self._functions is None:
            self.walk_tree()
        c = copy.copy(self)
        try:
            keys = c._functions_map[name]
        except KeyError:
            new_fns = {}
        else:
            new_fns = {k:c._functions[k] for k in keys if k in c._functions}
        if len(new_fns) == 0:
            return None
        else:
            c._functions = new_fns
            return c


# --------------------------------------------------------------------------------------------- #
# embedding stored output in pages
# --------------------------------------------------------------------------------------------- #

class ExampleEmbedError(Exception):
    """Marked examples had no usable stored output and the embedder was ``strict``."""


# (Deliberately not in ``__all__``: the doc walker treats exported strings as importable names.)
# The loader must not contain Liquid delimiters (double braces or brace-percent), since pages go through Jekyll.
# For a notebook, where examples are run and shown after the page has loaded: nothing in a readout fragment loads the
# X3DOM runtime (a fragment is markup only), so this loads it the first time an ``<x3d>`` element appears in the
# document and asks X3DOM to pick up each new scene. It is shown once per ``jdoc`` call through the display API (which
# runs scripts, in trusted notebooks); a second copy does nothing.
X3DOM_WATCHER_JS = """
(function(){
if(window.mcrX3DOMWatch){return;}
var runtime=__RUNTIME__;
var once={};
function memo(key,make,keep){if(!once[key]){once[key]=make();once[key].then(null,function(){delete once[key];});}return once[key];}
function loadScript(src){return memo("s:"+src,function(){return new Promise(function(ok,no){var s=document.createElement("script");s.src=src;s.onload=ok;s.onerror=function(){s.remove();no(new Error("could not load X3DOM from "+src));};document.head.appendChild(s);});});}
function loadCss(href){if(href&&!once["c:"+href]){once["c:"+href]=Promise.resolve();var l=document.createElement("link");l.rel="stylesheet";l.href=href;document.head.appendChild(l);}}
function sync(){
var fresh=document.querySelectorAll("x3d:not([data-mcr-x3d])");
if(!fresh.length){return;}
loadCss(runtime.stylesheet);
loadScript(runtime.script).then(function(){
var todo=document.querySelectorAll("x3d:not([data-mcr-x3d])");
if(!todo.length){return;}
for(var i=0;i<todo.length;i++){todo[i].setAttribute("data-mcr-x3d","1");}
if(window.x3dom&&window.x3dom.reload){window.x3dom.reload();}
},function(e){console.error(e);});
}
window.mcrX3DOMWatch=sync;
var pending=false;
function hasScene(n){return n.nodeType===1&&(n.matches("x3d")||!!n.querySelector("x3d"));}
new MutationObserver(function(records){
var added=false;
for(var i=0;i<records.length&&!added;i++){var nodes=records[i].addedNodes;for(var j=0;j<nodes.length&&!added;j++){added=hasScene(nodes[j]);}}
if(added&&!pending){pending=true;setTimeout(function(){pending=false;sync();},50);}
}).observe(document.documentElement,{childList:true,subtree:true});
sync();
})();
"""

EXAMPLE_LOADER_JS = """
(function(){
if(window.mcrReadouts){return;}
var once={};
function memo(key,make){if(!once[key]){once[key]=make();}return once[key];}
function loadScript(src){return memo("s:"+src,function(){return new Promise(function(ok,no){var s=document.createElement("script");s.src=src;s.onload=ok;s.onerror=no;document.head.appendChild(s);});});}
function loadCss(href){memo("c:"+href,function(){var l=document.createElement("link");l.rel="stylesheet";l.href=href;document.head.appendChild(l);return true;});}
function mount(el){
if(el.getAttribute("data-state")){return;}
el.setAttribute("data-state","loading");
fetch(el.getAttribute("data-src")).then(function(r){if(!r.ok){throw new Error("HTTP "+r.status);}return r.text();}).then(function(markup){
var css=el.getAttribute("data-css-href");if(css){loadCss(css);}
var show=function(){el.innerHTML=markup;el.setAttribute("data-state","ready");if(window.x3dom&&window.x3dom.reload){window.x3dom.reload();}};
if((el.getAttribute("data-needs")||"").indexOf("x3dom")>=0){
var x3css=el.getAttribute("data-x3dom-css");if(x3css){loadCss(x3css);}
loadScript(el.getAttribute("data-x3dom-script")).then(show,show);
}else{show();}
}).catch(function(){el.setAttribute("data-state","failed");el.className+=" mcr-failed";});
}
var io=("IntersectionObserver" in window)?new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting){io.unobserve(e.target);mount(e.target);}});},{rootMargin:"200px"}):null;
function watch(el){
if(el.getAttribute("data-state")||el.__mcrWatched){return;}
el.__mcrWatched=true;
if(io&&el.getAttribute("data-lazy")!=="false"){io.observe(el);}else{mount(el);}
}
function scan(){var found=document.querySelectorAll(".mcr-example[data-src]");for(var i=0;i<found.length;i++){watch(found[i]);}}
window.mcrReadouts={scan:scan,mount:mount};
if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",scan);}else{scan();}
window.addEventListener("load",scan);
if("MutationObserver" in window){var pending=false;new MutationObserver(function(){if(!pending){pending=true;setTimeout(function(){pending=false;scan();},50);}}).observe(document.documentElement,{childList:true,subtree:true});}
})();
""".strip()


# Opt-in (``debug=True``): a corner badge and console log reporting how many readouts on the page have loaded.
EXAMPLE_DEBUG_JS = """
(function(){
if(window.mcrDebug){return;}
window.mcrDebug=true;
var badge=document.createElement("div");
badge.style.cssText="position:fixed;right:8px;bottom:8px;z-index:99999;background:#222;color:#fff;font:12px/1.4 monospace;padding:4px 8px;border-radius:4px;opacity:.85";
function count(){
var all=document.querySelectorAll(".mcr-example"),c={ready:0,loading:0,failed:0,waiting:0,missing:0,error:0};
for(var i=0;i<all.length;i++){var e=all[i],s=e.getAttribute("data-state");
if(e.className.indexOf("mcr-missing")>=0){c.missing++;}else if(e.className.indexOf("mcr-error")>=0){c.error++;}
else if(s==="ready"){c.ready++;}else if(s==="loading"){c.loading++;}else if(s==="failed"){c.failed++;}else{c.waiting++;}}
return [all.length,c];
}
var last="";
function update(){
var r=count(),text="readouts: "+r[1].ready+"/"+r[0]+" loaded";
for(var k in r[1]){if(k!=="ready"&&r[1][k]){text+=", "+r[1][k]+" "+k;}}
badge.textContent=text;
if(text!==last){last=text;console.info("[mcr] "+text);}
}
function start(){document.body.appendChild(badge);update();setInterval(update,300);}
if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",start);}else{start();}
})();
""".strip()


def _attr(value):
    return html.escape(str(value), quote=True)


class ExampleEmbedder:
    """
    Callable ``examples_processor``: ``embedder(markdown, handler_or_owner) -> markdown``.

    :param store: the `ReadoutStore` (or its root directory)
    :param url_template: where a published fragment lives. ``{key}`` and ``{key2}`` (its first two
        characters) are replaced. The default goes through Jekyll's ``relative_url`` filter, which honours the
        site's ``baseurl``; use e.g. ``"/readouts/{key2}/{key}/fragment.html"`` for a plain absolute path.
    :param stylesheet_url_template: the same for the shared ``mcr.css`` (used for ``css="stylesheet"`` entries)
    :param lazy: fetch fragments when they become visible (default) rather than on page load
    :param strict: make `finish` raise if any marked block had no stored output or a failed one
    :param warn: callable for warnings (default ``print``)
    :param debug: also add a small script that shows a corner badge (and logs to the console) with how many
        readouts on the page have loaded, for checking a built site by eye
    :param inline: put each stored fragment directly into the page instead of a placeholder that is fetched
        later (for single-file HTML such as `static_doc`). No loader script is emitted; what the page still has
        to provide (an X3DOM runtime) is collected in ``assets``.
    """

    default_url_template = "{{ '/readouts/{key2}/{key}/fragment.html' | relative_url }}"
    default_stylesheet_url_template = "{{ '/readouts/mcr.css' | relative_url }}"

    def __init__(self, store, url_template=None, stylesheet_url_template=None, lazy=True, strict=False, warn=print,
                 loader=True, debug=False, inline=False):
        self.store = store if isinstance(store, ReadoutStore) else ReadoutStore(store)
        self.cache = ExampleCache(self.store)
        self.url_template = url_template or self.default_url_template
        self.stylesheet_url_template = stylesheet_url_template or self.default_stylesheet_url_template
        self.lazy = lazy
        self.strict = strict
        self.warn = warn
        self.loader = loader
        self.debug = debug
        self.inline = inline
        self.problems = []   # [(owner, id, kind, detail)]
        self.embedded = []   # [(owner, id, key)]
        self.assets = {}     # inline mode: what the host page must provide, e.g. {"x3dom": {"script": ..., "stylesheet": ...}}

    # ---- the processor interface ---- #
    def __call__(self, text, handler=None, owner=None):
        if owner is None and handler is not None:
            owner = getattr(handler, "identifier", None)
        if "readout" not in text:
            return text
        parsed = ExampleParser.parse(text, owner=owner)
        blocks = parsed.blocks
        if not blocks:
            return text
        state = {"first": True}

        def replace(block):
            fence = block.fence
            extra = self.placeholder(block, owner)
            if extra is None:
                return fence
            out = fence + "\n" + extra + "\n"
            if self.loader and not self.inline and state["first"]:
                out += "\n<script>\n" + EXAMPLE_LOADER_JS + "\n</script>\n"
                if self.debug:
                    out += "\n<script>\n" + EXAMPLE_DEBUG_JS + "\n</script>\n"
                state["first"] = False
            return out

        return parsed.render(replace)

    # ---- placeholders ---- #
    def url(self, key):
        return self.url_template.replace("{key2}", key[:2]).replace("{key}", key)

    def _problem(self, owner, block, kind, detail):
        self.problems.append((owner, block.id, kind, detail))
        if self.warn is not None:
            self.warn("readout {} for example `{}`{}: {}".format(
                kind, block.id, "" if owner is None else " ({})".format(owner), detail))

    def placeholder(self, block, owner=None):
        """The markup that follows a block's code fence, or ``None`` for ``display="none"``."""
        if block.options.get("display", "readout") == "none":
            return None
        meta = self.store.read_meta(block.key)
        if meta is None:
            self._problem(owner, block, "missing", "no stored output; run ci/build_readouts.py")
            return ('<div class="mcr-example mcr-missing" data-readout="{}" data-key="{}">'
                    "Readout not generated yet.</div>").format(_attr(block.id), block.key)
        if meta.get("status") == "error":
            err = meta.get("error") or {}
            self._problem(owner, block, "failed", "{}: {}".format(err.get("type", "error"), err.get("message", "")))
            return ('<div class="mcr-example mcr-error" data-readout="{}" data-key="{}">'
                    "This example failed when its output was generated: {}: {}</div>").format(
                _attr(block.id), block.key, _attr(err.get("type", "error")), _attr(err.get("message", "")))
        if not self.store.has_file(block.key, "fragment.html"):
            self._problem(owner, block, "missing", "the entry has no fragment")
            return None
        fragment = meta.get("fragment") or {}
        if self.inline:
            return self._inline_markup(block, owner, fragment)
        url = self.url(block.key)
        attrs = ['class="mcr-example"', 'data-readout="{}"'.format(_attr(block.id)), 'data-key="{}"'.format(block.key),
                 'data-src="{}"'.format(url)]
        if fragment.get("css") == "stylesheet":
            attrs.append('data-css-href="{}"'.format(self.stylesheet_url_template))
        needs = fragment.get("needs") or []
        if needs:
            attrs.append('data-needs="{}"'.format(_attr(" ".join(needs))))
            x3 = (fragment.get("runtime") or {}).get("x3dom") or {}
            if x3.get("script"):
                attrs.append('data-x3dom-script="{}"'.format(_attr(x3["script"])))
            if x3.get("stylesheet"):
                attrs.append('data-x3dom-css="{}"'.format(_attr(x3["stylesheet"])))
        if not self.lazy:
            attrs.append('data-lazy="false"')
        self.embedded.append((owner, block.id, block.key))
        return "<div {}><a href=\"{}\">Open readout</a></div>".format(" ".join(attrs), url)

    def _inline_markup(self, block, owner, fragment):
        html = self.store.read_file(block.key, "fragment.html")
        parts = []
        if fragment.get("css") == "stylesheet" and not self.assets.get("stylesheet"):
            css_path = os.path.join(self.store.root, self.store.stylesheet_name)
            if os.path.isfile(css_path):
                with open(css_path, encoding="utf-8") as f:
                    self.assets["stylesheet"] = f.read()
                parts.append("<style>\n" + self.assets["stylesheet"] + "\n</style>")
        if "x3dom" in (fragment.get("needs") or []):
            x3 = (fragment.get("runtime") or {}).get("x3dom") or {}
            self.assets.setdefault("x3dom", {k: x3[k] for k in ("script", "stylesheet") if x3.get(k)})
        self.embedded.append((owner, block.id, block.key))
        parts.append('<div class="mcr-example mcr-inline" data-readout="{}" data-key="{}">\n{}\n</div>'.format(
            _attr(block.id), block.key, html))
        return "\n".join(parts)

    def finish(self):
        """Raises `ExampleEmbedError` listing every problem if ``strict``; otherwise returns the problems."""
        if self.strict and self.problems:
            raise ExampleEmbedError("{} example(s) have no usable output:\n{}".format(
                len(self.problems), "\n".join("  {} / {}: {} ({})".format(*p) for p in self.problems)))
        return list(self.problems)


class ExampleCollector:
    """
    The same interface as `ExampleEmbedder`, but only records the pages that have marked examples and
    returns the text unchanged. ``pages`` maps an owner to the text seen for it.
    """

    def __init__(self):
        self.pages = {}
        self.ids = {}

    def __call__(self, text, handler=None, owner=None):
        if owner is None and handler is not None:
            owner = getattr(handler, "identifier", None)
        if "readout" not in text:
            return text
        parsed = ExampleParser.parse(text, owner=owner)
        if parsed.blocks:
            self.pages[owner] = text
            for b in parsed.blocks:
                other = self.ids.setdefault(b.id, owner)
                if other != owner:
                    raise ValueError("example id `{}` is used by both `{}` and `{}`; ids must be unique across "
                                     "pages because the manifest is keyed by id".format(b.id, other, owner))
        return text

    def parsed_pages(self):
        return [(owner, ExampleParser.parse(text, owner=owner)) for owner, text in self.pages.items()]


def publish_readouts(store, target, stylesheet=True):
    """
    Copies a store into a site directory as ``<target>/readouts`` (when it isn't already there).
    Returns the destination.
    """
    store = store if isinstance(store, ReadoutStore) else ReadoutStore(store)
    dest = os.path.join(target, "readouts")
    if os.path.abspath(dest) == os.path.abspath(store.root) or not os.path.isdir(store.root):
        return dest
    os.makedirs(dest, exist_ok=True)
    for name in os.listdir(store.root):
        src = os.path.join(store.root, name)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(dest, name), dirs_exist_ok=True)
        elif name == ReadoutStore.stylesheet_name and stylesheet:
            shutil.copy2(src, os.path.join(dest, name))
    return dest


# --------------------------------------------------------------------------------------------- #
# running a page in a worker process
# --------------------------------------------------------------------------------------------- #

class ExampleWorkerError(ExampleError):
    """The worker process couldn't do its job at all (e.g. it failed before running anything)."""


class ExampleWorkerCrash(ExampleError):
    """The worker process died or had to be killed while running an example."""


def _glob_escape(text):
    return re.sub(r"([*?\[])", r"[\1]", text)


class SubprocessExampleRunner:
    """
    The same interface as `ExampleRunner` (``plan``, ``run_text``, ``run_page``), but each page runs in its
    own worker process (``python -c "from McUtils.Docs.Examples import run_worker; ..."``).

    The parent plans from the store, so a page with nothing to do never starts a process. The worker
    reports one event per block; the parent enforces limits on top of the in-worker ``SIGALRM`` timeout
    (which can't interrupt native code):

    * a block that runs longer than its timeout plus ``kill_grace`` seconds gets the worker killed,
    * the worker has ``startup_timeout`` seconds to import everything and report ready,
    * ``page_timeout`` (optional) bounds the whole page.

    A block that was running when the worker died or was killed is recorded as an error (cached, like any
    other failure), the rest of its chain is reported ``blocked``, and the remaining chains are run by a
    fresh worker.

    :param store: the `ReadoutStore`
    :param timeout: default per-block limit in seconds (a marker's ``timeout`` overrides it)
    :param python: the interpreter to run (default: the current one)
    :param sys_path: extra import paths for the worker (default: the parent's ``sys.path``)
    :param cwd: working directory of the worker
    :param env: extra environment variables for the worker
    :param revisions, style, x3dom_path, css, seed, max_output, imports: as for `ExampleRunner`
    """

    def __init__(self, store, revisions=None, style=None, x3dom_path=None, css="inline", seed=True,
                 timeout=None, page_timeout=None, kill_grace=15.0, startup_timeout=120.0, python=None,
                 sys_path=None, cwd=None, env=None, max_output=20000, verbose=False, stream=None, imports=True):
        # an in-process runner is used for planning and to record failures the worker couldn't
        self.local = ExampleRunner(store, revisions=revisions, style=style, x3dom_path=x3dom_path, css=css,
                                   seed=seed, timeout=timeout, max_output=max_output, imports=imports)
        self.store = store
        self.cache = self.local.cache
        self.revisions = dict(revisions or {})
        self.style = style
        self.x3dom_path = x3dom_path
        self.css = css
        self.seed = seed
        self.imports = imports
        self.timeout = timeout
        self.page_timeout = page_timeout
        self.kill_grace = kill_grace
        self.startup_timeout = startup_timeout
        self.python = python or sys.executable
        self.sys_path = [p for p in (sys.path if sys_path is None else sys_path) if p]
        self.cwd = cwd
        self.env = dict(env or {})
        self.max_output = max_output
        self.verbose = verbose
        self.stream = stream
        self.last_log = ""

    # ---- same interface as ExampleRunner ---- #
    def plan(self, parsed, refresh=False):
        return self.cache.plan(parsed.blocks, refresh)

    def run_text(self, text, owner=None, refresh=False, first_line=1):
        return self.run_page(ExampleParser.parse(text, owner=owner, first_line=first_line), refresh=refresh)

    def run_page(self, parsed, refresh=False, sync=True):
        blocks = parsed.blocks
        by_id = {b.id: b for b in blocks}
        reasons = {b.id: r for b, r in self.cache.plan(blocks, refresh)}
        results = {}
        log = []
        passes = 0
        while True:
            remaining = [i for i in reasons if i not in results]
            if not remaining:
                break
            pass_refresh = refresh if passes == 0 else [_glob_escape(i) for i in remaining]
            _, need, doomed = self.local.analyse(parsed, pass_refresh)
            for i, culprit in doomed.items():
                results.setdefault(i, ExampleResult(by_id[i], "blocked", reason=reasons.get(i), blocked_by=culprit))
            if not need:
                break  # nothing left that has to execute, so no worker is needed
            passes += 1
            if passes > len(blocks) + 1:
                raise ExampleWorkerError("example worker kept failing; giving up on {}".format(remaining))
            events, running, finished, fatal, stderr_tail = self._run_worker(parsed, pass_refresh, by_id)
            log.append(stderr_tail)
            for ev in events:
                if ev["event"] == "result" and ev["id"] in reasons and ev["id"] not in results:
                    results[ev["id"]] = ExampleResult(
                        by_id[ev["id"]], ev["status"], ev.get("meta"), ev.get("reason"), ev.get("blocked_by")
                    )
            if finished:
                break
            if fatal is not None and running is None:
                raise ExampleWorkerError("example worker failed before running anything:\n" + fatal)
            if running is None:
                raise ExampleWorkerError(
                    "example worker exited without finishing and without running anything:\n" + stderr_tail
                )
            if running in results:
                continue  # it had reported its result just as the process went away
            message = fatal or self._crash_message
            if stderr_tail.strip():
                message += "\n--- worker stderr (tail) ---\n" + stderr_tail
            results[running] = self.local._record_error(
                by_id[running], ExampleWorkerCrash(message), reasons.get(running, "missing")
            )
        self.last_log = "\n".join(l for l in log if l.strip())
        if sync:
            self.cache.sync_manifest(blocks)
        return [results[b.id] for b in blocks if b.id in results]

    # ---- the process ---- #
    _crash_message = "the worker process died while running this example"

    def _job(self, parsed, refresh):
        return {
            "text": str(parsed), "owner": parsed.owner, "first_line": parsed.first_line, "refresh": refresh,
            "store": self.store.root, "revisions": self.revisions, "style": self.style,
            "x3dom_path": self.x3dom_path, "css": self.css, "seed": self.seed, "timeout": self.timeout,
            "max_output": self.max_output, "sys_path": self.sys_path, "imports": self.imports,
        }

    def _environment(self):
        env = dict(os.environ)
        here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        paths = [here] + [p for p in env.get("PYTHONPATH", "").split(os.pathsep) if p]
        env["PYTHONPATH"] = os.pathsep.join(paths)
        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        env.update(self.env)
        return env

    def _block_limit(self, block):
        limit = block.options.get("timeout", self.timeout)
        return None if limit is None else limit + self.kill_grace

    def _run_worker(self, parsed, refresh, by_id):
        """Runs one worker; returns ``(events, running_id, finished, fatal_text, stderr_tail)``."""
        job = self._job(parsed, refresh)
        errfile = tempfile.TemporaryFile(mode="w+b")
        posix = os.name == "posix"
        proc = subprocess.Popen(
            [self.python, "-c", WORKER_COMMAND], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=errfile, cwd=self.cwd, env=self._environment(), start_new_session=posix,
        )
        lines = queue.Queue()

        def pump():
            for raw in proc.stdout:
                lines.put(raw)
            lines.put(None)

        reader = threading.Thread(target=pump, daemon=True)
        reader.start()
        try:
            proc.stdin.write(json.dumps(job).encode("utf-8"))
            proc.stdin.close()
        except OSError:
            pass  # the worker died early; its stderr explains
        events = []
        running = None
        finished = False
        fatal = None
        ready = False
        start = time.monotonic()
        page_deadline = None if self.page_timeout is None else start + self.page_timeout
        block_deadline = None
        startup_deadline = start + self.startup_timeout
        killed_for = None
        while True:
            deadlines = [d for d in (page_deadline, block_deadline, None if ready else startup_deadline)
                         if d is not None]
            wait = None if not deadlines else max(0.0, min(deadlines) - time.monotonic())
            try:
                raw = lines.get(timeout=wait)
            except queue.Empty:
                now = time.monotonic()
                if page_deadline is not None and now >= page_deadline:
                    killed_for = "the page time limit of {} s".format(self.page_timeout)
                elif block_deadline is not None and now >= block_deadline:
                    killed_for = "its time limit (plus {} s of grace)".format(self.kill_grace)
                else:
                    killed_for = "startup ({} s)".format(self.startup_timeout)
                self._kill(proc)
                break
            if raw is None:
                break
            try:
                ev = json.loads(raw.decode("utf-8"))
            except ValueError:
                continue
            kind = ev.get("event")
            if self.verbose and self.stream is not None and kind in ("start", "result"):
                print("  {} {}{}".format(kind, ev.get("id"), "" if kind == "start" else " -> " + ev.get("status", "")),
                      file=self.stream)
            if kind == "ready":
                ready = True
            elif kind == "start":
                running = ev["id"]
                block_deadline = None
                if running in by_id:
                    limit = self._block_limit(by_id[running])
                    block_deadline = None if limit is None else time.monotonic() + limit
            elif kind == "result":
                events.append(ev)
                if ev["id"] == running:
                    running = None
                    block_deadline = None
            elif kind == "done":
                finished = True
            elif kind == "fatal":
                fatal = ev.get("error", "")
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self._kill(proc)
            proc.wait()
        reader.join(timeout=2)
        proc.stdout.close()
        errfile.seek(0)
        stderr_tail = errfile.read()[-4000:].decode("utf-8", "replace")
        errfile.close()
        if not finished:
            if killed_for is not None:
                self._crash_message = (
                    "the worker was killed after this example exceeded {} without returning "
                    "(it may be stuck in native code)".format(killed_for)
                )
            else:
                code = proc.returncode
                what = "exit code {}".format(code)
                if code is not None and code < 0:
                    try:
                        what = "signal {}".format(signal.Signals(-code).name)
                    except ValueError:
                        pass
                self._crash_message = "the worker process died ({}) while running this example".format(what)
        return events, running, finished, fatal, stderr_tail

    @staticmethod
    def _kill(proc):
        try:
            if os.name == "posix":
                os.killpg(proc.pid, signal.SIGKILL)
            else:
                proc.kill()
        except (OSError, ProcessLookupError):
            pass


# --------------------------------------------------------------------------------------------- #
# the worker process (`run_worker`)
# --------------------------------------------------------------------------------------------- #

WORKER_COMMAND = "import sys; from McUtils.Docs.Examples import run_worker; sys.exit(run_worker())"
# (Not ``python -m``: the package imports this module, so ``-m`` would run it a second time as ``__main__``.)

# Events: {"event": "ready"}, {"event": "start", "id"}, {"event": "result", "id", "status", "reason",
# "blocked_by", "meta"}, {"event": "done"}, {"event": "fatal", "error"}.


def run_worker(argv=None):
    import faulthandler
    faulthandler.enable()  # a segfault in native code leaves a Python traceback in the stderr log
    proto = os.fdopen(os.dup(1), "w", encoding="utf-8", buffering=1)
    os.dup2(2, 1)  # stray writes to stdout land in the stderr log
    devnull = os.open(os.devnull, os.O_RDONLY)

    def emit(**event):
        proto.write(json.dumps(event, default=str) + "\n")
        proto.flush()

    try:
        job = json.loads(sys.stdin.read())
        os.dup2(devnull, 0)  # an example calling input() gets EOF instead of hanging
        for p in reversed(job.get("sys_path") or []):
            if p and p not in sys.path:
                sys.path.insert(0, p)
        store = ReadoutStore(job["store"])
        runner = ExampleRunner(
            store, revisions=job.get("revisions"), style=job.get("style"), x3dom_path=job.get("x3dom_path"),
            css=job.get("css", "inline"), seed=job.get("seed", True), timeout=job.get("timeout"),
            max_output=job.get("max_output", 20000), imports=job.get("imports", True)
        )
        parsed = ExampleParser.parse(job["text"], owner=job.get("owner"), first_line=job.get("first_line", 1))
        emit(event="ready")

        def on_event(event, block, result=None):
            if event == "start":
                emit(event="start", id=block.id)
            else:
                emit(event="result", id=block.id, status=result.status, reason=result.reason,
                     blocked_by=result.blocked_by, meta=result.meta)

        runner.run_page(parsed, refresh=job.get("refresh", False), sync=False, on_event=on_event)
        emit(event="done")
        return 0
    except BaseException:
        emit(event="fatal", error=traceback.format_exc())
        return 3




# --------------------------------------------------------------------------------------------- #
# interactive (notebook) examples
# --------------------------------------------------------------------------------------------- #

def split_examples(text, owner=None):
    """
    Splits examples Markdown into the pieces an interactive view renders separately.

    :return: ``[("text", markdown)]`` and ``[("code", block)]`` pieces in page order, where the markdown of a
        code piece is ``block.fence``; ``None`` if ``text`` has no (valid) markers, so the caller can render it
        as plain Markdown exactly as before
    """
    if not ExampleParser.has_markers(text):
        return None
    try:
        parsed = ExampleParser.parse(text, owner=owner)
    except ExampleMarkerError:
        return None
    pieces = []
    for seg in parsed.segments:
        if isinstance(seg, str):
            if seg.strip():
                pieces.append(("text", seg))
        else:
            pieces.append(("code", seg))
    return pieces if any(kind == "code" for kind, _ in pieces) else None


class Fragment(str):
    """Marks a string as ready-made HTML rather than text to be escaped."""


class LiveExampleResult:
    """
    What running a block gave: ``status`` is ``"ok"``, ``"empty"`` (``display="none"``, or nothing to show) or
    ``"error"``; ``view`` is the `ExampleView` (``ok`` only); ``error`` the traceback text (``error`` only).
    """

    def __init__(self, block, status, view=None, error=None, duration=None):
        self.block = block
        self.status = status
        self.view = view
        self.error = error
        self.duration = duration

    @property
    def ok(self):
        return self.status == "ok"

    def fragment(self, style=None, css="inline"):
        """The output as an embeddable `FragmentResult` (the same thing the build stores), or ``None``."""
        if self.view is None:
            return None
        return self.view.to_fragment(style=style, css=css)

    def element(self, mode="widget", style=None, css="inline", **opts):
        """The output as a JHTML element (no code), or ``None``."""
        if self.view is None:
            return None
        return self.view.to_element(mode, style=style, css=css, include_code=False, **opts)

    def __repr__(self):
        return "{}({!r}, {})".format(type(self).__name__, self.block.id, self.status)


class LiveExamplePage:
    """
    Runs the marked blocks of one examples text interactively.

    Blocks share a namespace in order (the chain used for their stored keys): running a block first runs, once,
    the earlier blocks of its chain that haven't run yet; running a block again re-runs only that block.
    Each block is seeded from its key like the build does, so a seeded example gives the output stored for it.

    :param text: Markdown with marked examples
    :param owner: the documented object's name (used for default ids)
    :param store: a `ReadoutStore` (or its directory) holding the output the documentation build stored, for
        showing it before a block is run
    :param namespace: ``None`` (default) for a private namespace per chain of blocks, a dict to run every block in
        (e.g. the notebook's namespace), or ``"user"`` for IPython's ``user_ns``
    :param timeout: per-block time limit in seconds (a marker's ``timeout`` overrides it)
    :param imports: start each chain with the owner's public names (see `ExampleRunner`); ignored if ``runner`` is given
    :param runner: an `ExampleRunner` to execute with; defaults to one with the given ``timeout``
    """

    def __init__(self, text, owner=None, store=None, namespace=None, timeout=60, runner=None, to_readout=None,
                 imports=True):
        self.owner = owner
        self.parsed = ExampleParser.parse(text, owner=owner)
        if isinstance(store, (str, os.PathLike)):
            store = ReadoutStore(store)
        self.store = store
        self.runner = runner or ExampleRunner(store, timeout=timeout, to_readout=to_readout, imports=imports)
        self.namespace = namespace
        self._namespaces = {}
        self._ran = set()
        self.results = {}

    @property
    def blocks(self):
        return self.parsed.blocks

    def block(self, block):
        """Resolves a block given as an `ExampleBlock`, an id, or an index."""
        blocks = self.blocks
        if isinstance(block, int):
            return blocks[block]
        if isinstance(block, str):
            for b in blocks:
                if b.id == block:
                    return b
            raise KeyError("no example with id {!r}".format(block))
        # a block from another parse of the same text (`split_examples` parses separately from the page that runs
        # it) is the same example: match it by key, which chains in everything before it
        for b in blocks:
            if b is block:
                return b
        for b in blocks:
            if b.key == block.key and b.id == block.id:
                return b
        raise KeyError("example {!r} is not on this page".format(getattr(block, "id", block)))

    # ---- stored output ---- #
    def stored_fragment(self, block):
        """The HTML the documentation build stored for ``block``, or ``None`` (not stored, failed, or no store)."""
        if self.store is None:
            return None
        block = self.block(block)
        meta = self.store.read_meta(block.key)
        if meta is None or meta.get("status") != "ok" or not self.store.has_file(block.key, "fragment.html"):
            return None
        return self.store.read_file(block.key, "fragment.html")

    def stored_output(self, block):
        """The `FragmentResult` the build stored for ``block`` (with what it needs to run), or ``None``."""
        html = self.stored_fragment(block)
        if html is None:
            return None
        from ..Readouts.Renderers.HTML import FragmentResult
        info = self.store.read_meta(self.block(block).key).get("fragment") or {}
        return FragmentResult(html, info.get("needs", ()), info.get("runtime"), info.get("head", ()))

    # ---- running ---- #
    def _namespace_for(self, block):
        ns = self.namespace
        if ns == "user":
            from IPython import get_ipython
            shell = get_ipython()
            if shell is None:
                raise RuntimeError("namespace='user' needs a running IPython session")
            return shell.user_ns
        if ns is not None:
            return ns
        start = self.parsed.chain(block)[0].index
        if start not in self._namespaces:
            self._namespaces[start] = self.runner.new_namespace(self.owner)
        return self._namespaces[start]

    def _execute(self, block, namespace):
        outcome = self.runner.execute(block, namespace)
        self._ran.add(block.id)
        return ExampleView(block, outcome["value"], outcome["stdout"], self.runner.to_readout,
                           self.runner.max_output), outcome["duration"]

    def run(self, block):
        """
        Runs ``block`` (after any earlier blocks of its chain that haven't run) and returns its `ExampleView`.

        :raises: whatever the example raises
        """
        block = self.block(block)
        namespace = self._namespace_for(block)
        for earlier in self.parsed.chain(block)[:-1]:
            if earlier.id not in self._ran:
                self._execute(earlier, namespace)
        view, _ = self._execute(block, namespace)
        return view

    def try_run(self, block):
        """Like `run`, but returns a `LiveExampleResult` instead of raising (a failure is ``status="error"``)."""
        block = self.block(block)
        try:
            view = self.run(block)
        except (Exception, SystemExit) as e:
            result = LiveExampleResult(block, "error", error=self.runner.format_error(e))
        else:
            if view.display == "none":
                result = LiveExampleResult(block, "empty", view)
            else:
                try:
                    node = view.node()
                except (Exception, SystemExit) as e:   # e.g. display="readout" with no value
                    result = LiveExampleResult(block, "error", error=self.runner.format_error(e))
                else:   # no node: nothing worth showing (a trivial readout is suppressed unless show_trivial)
                    result = LiveExampleResult(block, "empty" if node is None else "ok", view)
        self.results[block.id] = result
        return result

    def reset(self):
        """Forgets every namespace and run, so the next run starts the page again."""
        self._namespaces.clear()
        self._ran.clear()
        self.results.clear()

    # ---- notebook controls ---- #
    def control(self, block, show_stored=True, label="Run"):
        """
        A **Run** button with an output area under it, built from `JHTML` elements: the click is a JHTML
        ``event_handlers`` entry and the output is written into a ``JHTML.Div`` through its content setters, so
        the interaction goes through the ``ActiveHTMLWidget`` layer and never touches ``ipywidgets`` directly.
        The first display also checks that the ``ActiveHTMLWidget`` extension is installed (see
        `HTMLWidgets.check_extension`) and says how to install it if not.

        The button runs the block (and whatever it needs). With ``show_stored``, a block whose output the
        documentation build stored shows that output and gets no button; a block without stored output gets the button.

        :param block: the block, id or index
        :param show_stored: show the stored output before the first run
        :param label: the button text
        :return: a ``JHTML.Div`` holding the button and the output area
        """
        from ..Jupyter import JHTML
        from ..Jupyter.Apps.Themes import AppHTML
        block = self.block(block)
        self.show_runtime()
        out = JHTML.Div(cls="mcr-live-output", dynamic=True, style={"margin-top": ".6em", "min-width": "0"})

        def show(display):
            self.place(out, display)

        if show_stored:
            stored = self.stored_output(block)
            if stored is not None:
                # the documentation build already has this output, so there is nothing to run
                show(stored)
                return JHTML.Div(out, cls="mcr-live-example", style={"margin": ".4em 0 1.2em 0"})

        def run(*_):
            result = self.try_run(block)
            self.show_result(result, show)
            if result.status != "error":
                # the output stays, the button goes; after a failure it stays so the example can be retried
                button.set_attribute("display", "none")

        # the Apps element factory: the button takes the look of whichever Apps theme is active (native `mcui-button`,
        # or Bootstrap's `btn`), like the Opener and the rest of the documentation view, instead of the browser default
        button = AppHTML.Bootstrap.Button(label, event_handlers={"click": run}, cls="mcr-run btn-sm", variant="primary")
        return JHTML.Div(button, out, cls="mcr-live-example", style={"margin": ".4em 0 1.2em 0"})

    _runtime_shown = False

    def show_runtime(self):
        """
        Shows, once per page object, the script (`X3DOM_WATCHER_JS`) that loads the X3DOM runtime when a 3D scene
        appears. The ActiveHTMLWidget frontend sets ``innerHTML`` without running scripts, and a readout fragment is
        markup only, so something on the page has to load the runtime; the display API runs scripts when it is
        shown in a trusted notebook. It is shown where ``jdoc`` is called (a callback's display output goes
        elsewhere), and it does nothing a second time.
        """
        if self._runtime_shown:
            return
        self._runtime_shown = True
        from ..Jupyter.JHTML.WidgetTools import JupyterAPIs
        from ..Readouts.Renderers.HTML import HTMLReadoutRenderer
        try:
            runtime = HTMLReadoutRenderer(x3dom_path=getattr(self.runner, "x3dom_path", None)).runtime_info()
        except ValueError:      # 'local'/'inline' only make sense in standalone documents
            runtime = HTMLReadoutRenderer().runtime_info()
        script = X3DOM_WATCHER_JS.replace("__RUNTIME__", json.dumps(runtime))
        display = JupyterAPIs.get_display_api()
        if display is not None:
            display.display(display.HTML("<script>" + script + "</script>"))

    @staticmethod
    def place(target, display):
        """
        Replaces the content of a JHTML element: `Fragment` and plain JHTML elements are written into its
        ``html_string``, strings are shown as escaped text, and live JHTML widgets become its child. A readout
        `FragmentResult` is written the same way; if it holds a 3D scene, the page's X3DOM watcher (see
        `show_runtime`) loads the runtime and starts it.
        """
        from ..Readouts.Renderers.HTML import FragmentResult
        from ..Jupyter import JHTML
        from ..Jupyter.JHTML.HTML import HTML as _HTML
        from ..Jupyter.JHTML.HTMLWidgets import ActiveHTMLWrapper
        if isinstance(display, FragmentResult):
            target.html_string = display.html
        elif isinstance(display, ActiveHTMLWrapper):
            target.html_string = ""
            target.children = [target.canonicalize_widget(display)]
        else:
            if isinstance(display, Fragment):
                markup = str(display)
            elif isinstance(display, str):
                markup = JHTML.Pre(display).tostring()
            elif isinstance(display, _HTML.XMLElement):
                markup = display.tostring()
            else:
                raise TypeError("don't know how to place {}".format(type(display).__name__))
            target.html_string = markup

    def show_result(self, result, show):
        """Calls ``show(display)`` with what a `LiveExampleResult` should look like in a JHTML output area."""
        if result.status == "error":
            show("Example `{}` failed:\n{}".format(result.block.id, result.error))
        elif result.status == "empty":
            show("Ran `{}` (nothing to display).".format(result.block.id))
        else:
            fragment = result.fragment()
            show(fragment if fragment is not None else "Ran `{}` (nothing to display).".format(result.block.id))

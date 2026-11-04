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
"""

import ast, collections, contextlib, datetime, fnmatch, hashlib, io, json, linecache, os, random, re, \
    shutil, signal, sys, threading, time, traceback

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
        :param refresh: ``False`` (only missing entries), ``"stale"`` (missing and stale), ``True``/``"all"``
                        (everything), or a glob / list of globs over block ids (those, plus missing entries)
        :return: ``[(block, reason), ...]`` in page order; reasons are ``"missing"``, ``"stale"``,
                 ``"refresh"``. Executing a block also requires replaying the earlier blocks of its chain
                 (`ParsedExamples.chain`); the plan lists only the blocks whose *output* must be produced.
        """
        if refresh is True or refresh == "all":
            return [(b, "refresh") for b in blocks]
        if refresh is False or refresh is None:
            globs = []
            stale = False
        elif refresh == "stale":
            globs = []
            stale = True
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
    """

    def __init__(self, block, value=_NO_VALUE, stdout="", to_readout=None, max_output=20000):
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
        if lead or extra:
            return Readout(*lead, *base.get_children(), *extra, title=base.title, subtitle=base.subtitle,
                           units=base.units, id=base.id, meta=base.meta)
        return base

    def to_fragment(self, style=None, x3dom_path=None, css="inline"):
        """The embeddable `FragmentResult` for the site, or ``None`` for ``display="none"``."""
        node = self.node()
        return None if node is None else node.to_html_fragment(style=style, x3dom_path=x3dom_path, css=css)

    def to_element(self, mode="static", style=None, css="inline", **opts):
        """
        The code plus its output as an element: ``mode="static"`` (plain elements, ``.tostring()``) for
        pages, ``mode="widget"`` for Jupyter.
        """
        from ..Readouts.Renderers.HTML import HTMLReadoutRenderer
        node = self.node(include_code=True)
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
    :param timeout: default per-block time limit in seconds (a marker's ``timeout`` overrides it)
    :param to_readout: override for `value_to_readout`
    """

    def __init__(self, store, revisions=None, style=None, x3dom_path=None, css="inline", seed=True,
                 namespace=None, timeout=None, to_readout=None, max_output=20000, clock=time.perf_counter):
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
                namespace = self._new_namespace()
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
    def _new_namespace(self):
        ns = {"__name__": "__mcr_example__"}
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
        frames = [f for f in traceback.extract_tb(exc.__traceback__)
                  if os.path.abspath(f.filename) != os.path.abspath(__file__)]
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

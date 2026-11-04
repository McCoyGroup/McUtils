"""
Adds ``<!-- readout(...) -->`` markers to the plain Python examples in ``ci/docs/examples``, where showing
their output makes sense.

    python ci/mark_examples.py                     # report what would be marked; change nothing
    python ci/mark_examples.py --write             # add the markers
    python ci/mark_examples.py McUtils/Combinatorics.md --write

A Python fence is a candidate if it ends in an expression (its value is shown) or prints something (its output
is shown), isn't already marked, and isn't inside one of the hand-made ``in-out-block`` cards that carry their own
picture of the result. Every candidate is marked ``isolated=True`` (each block of these pages brings its own
imports) and then *run*, in a worker process with a time limit and a scratch working directory, and the marker is
kept only if it ran cleanly. Blocks that fail (they need an earlier block, a data file, a display, ...) stay
unmarked and are listed with the reason, so the pages can be fixed up by hand. Nothing is written to the readout
store: run ``ci/build_readouts.py`` afterwards to generate the output the markers ask for.

Ids are ``<page>-<n>``, where ``n`` counts every Python fence on the page, so adding a marker to another fence
never renames one that exists.
"""

import argparse, ast, contextlib, io, os, re, sys, tempfile

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
if root not in sys.path:
    sys.path.insert(0, root)

DEFAULT_EXAMPLES = os.path.join(here, "docs", "examples")

# things an automatic run shouldn't do on the author's machine
UNSAFE = re.compile(
    r"\b(input\(|os\.remove|os\.unlink|shutil\.rmtree|rmtree\(|subprocess|os\.system|"
    r"plt\.show|\.show\(\)|webbrowser|requests\.|urllib|socket\.)"
)


class Fence:
    """A Python fence found in a page: ``start``/``end`` are 0-based line indices of the fences' lines."""

    def __init__(self, ordinal, start, end, source, marked, handmade):
        self.ordinal = ordinal
        self.start = start
        self.end = end
        self.source = source
        self.marked = marked
        self.handmade = handmade
        self.display = None
        self.skip = None


def scan(text):
    """The Python fences of a Markdown text, outermost fences only, in order."""
    from McUtils.Docs.Examples import _FENCE_OPEN, _PYTHON_LANGS, ExampleParser
    lines = text.splitlines()
    fences = []
    i = 0
    while i < len(lines):
        m = _FENCE_OPEN.match(lines[i])
        if not m:
            i += 1
            continue
        indent, ticks, lang = m.group(1), m.group(2), m.group(3)
        j = i + 1
        while j < len(lines) and not re.match(r"^ {0,3}" + ticks[0] + "{" + str(len(ticks)) + r",}[ \t]*$", lines[j]):
            j += 1
        if lang.split("{")[0] in _PYTHON_LANGS and j < len(lines):
            prev = next((lines[k] for k in range(i - 1, -1, -1) if lines[k].strip()), "")
            marked = bool(ExampleParser.marker_start.match(prev)) or prev.strip().endswith("-->") and "readout" in prev
            handmade = "in-out-block" in prev
            fences.append(Fence(len(fences) + 1, i, j, "\n".join(lines[i + 1:j]), marked, handmade))
        i = j + 1
    return lines, fences


def classify(fence):
    """Decides what (if anything) to show for a fence; sets ``fence.display`` or ``fence.skip``."""
    if fence.marked:
        fence.skip = "already marked"
    elif fence.handmade:
        fence.skip = "has a hand-made output card"
    elif UNSAFE.search(fence.source):
        fence.skip = "does something an automatic run shouldn't (files, network, display)"
    else:
        try:
            tree = ast.parse(fence.source)
        except SyntaxError as e:
            fence.skip = "not valid Python on its own ({})".format(e.msg)
            return
        stripped = fence.source.rstrip()
        last = stripped.splitlines()[-1].rstrip() if stripped else ""
        has_value = bool(tree.body) and isinstance(tree.body[-1], ast.Expr) and not last.endswith(";")
        prints = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print"
                     for n in ast.walk(tree))
        if has_value and prints:
            fence.display = "both"
        elif has_value:
            fence.display = "readout"
        elif prints:
            fence.display = "output"
        else:
            fence.skip = "ends in a statement and prints nothing, so there is nothing to show"


def page_owner(rel):
    """The documented object an examples file belongs to, as the docs walk names it: ``McUtils/Zachary.md`` is ``McUtils.Zachary``."""
    return os.path.splitext(rel)[0].replace(os.sep, ".")


def page_slug(rel):
    return re.sub(r"[^a-z0-9]+", "-", os.path.splitext(rel)[0].lower()).strip("-")


def marker_text(slug, fence, timeout=None):
    opts = ['id="{}-{}"'.format(slug, fence.ordinal), "isolated=True"]
    if fence.display != "readout":
        opts.append('display="{}"'.format(fence.display))
    if timeout is not None:
        opts.append("timeout={:g}".format(timeout))
    return "<!-- readout({}) -->".format(", ".join(opts))


def insert_markers(lines, fences, slug, keep=None):
    """The page text with markers before the fences in ``keep`` (a set of ordinals; default: every candidate)."""
    out = []
    chosen = {f.start: f for f in fences if f.skip is None and (keep is None or f.ordinal in keep)}
    for n, line in enumerate(lines):
        if n in chosen:
            indent = re.match(r"^( *)", line).group(1)
            out.append(indent + marker_text(slug, chosen[n]))
        out.append(line)
    return "\n".join(out) + "\n"


def process_page(path, rel, timeout, runner, log):
    owner = page_owner(rel)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines, fences = scan(text)
    for fence in fences:
        classify(fence)
    candidates = [f for f in fences if f.skip is None]
    slug = page_slug(rel)
    if not candidates:
        return text, text, fences, {}
    trial = insert_markers(lines, fences, slug)
    results = {}
    for r in runner.run_text(trial, owner=owner):
        results[r.block.id] = r
    keep = set()
    reasons = {}
    for f in candidates:
        r = results.get("{}-{}".format(slug, f.ordinal))
        if r is not None and r.status == "ok":
            keep.add(f.ordinal)
        else:
            f.skip = "failed: " + _why(r)
    return text, insert_markers(lines, fences, slug, keep), fences, results


def _why(result):
    if result is None:
        return "was not run"
    if result.status == "blocked":
        return "blocked by {}".format(result.blocked_by)
    err = (result.meta or {}).get("error") or {}
    msg = (err.get("message") or "").strip().splitlines()
    return "{}{}".format(err.get("type", result.status), (": " + msg[0][:100]) if msg else "")


def find_pages(paths, examples):
    found = []
    targets = [os.path.join(examples, p) if not os.path.isabs(p) and not os.path.exists(p) else p for p in paths] or [examples]
    for target in targets:
        if os.path.isdir(target):
            for dirpath, _, files in sorted(os.walk(target)):
                found += [os.path.join(dirpath, n) for n in sorted(files) if n.endswith(".md")]
        else:
            found.append(target)
    return found


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("pages", nargs="*", help="example pages or folders (default: all of ci/docs/examples)")
    ap.add_argument("--examples", default=DEFAULT_EXAMPLES, help="the examples folder (default: %(default)s)")
    ap.add_argument("--write", action="store_true", help="rewrite the pages (default: report only)")
    ap.add_argument("--timeout", type=float, default=30.0, help="per-example limit in seconds (default: %(default)s)")
    ap.add_argument("--no-implicit-imports", action="store_true",
                    help="run examples without the names of the module they document (the build's default has them)")
    ap.add_argument("-v", "--verbose", action="store_true", help="also list the fences that were left alone and why")
    args = ap.parse_args(argv)

    from McUtils.Docs import ReadoutStore, SubprocessExampleRunner
    examples = os.path.abspath(args.examples)
    pages = find_pages(args.pages, examples)
    total = {"marked": 0, "failed": 0, "skipped": 0, "pages": 0}
    old_cwd = os.getcwd()
    with tempfile.TemporaryDirectory(prefix="mark-examples-") as tmp:
        runner = SubprocessExampleRunner(ReadoutStore(os.path.join(tmp, "store")), timeout=args.timeout,
                                         imports=not args.no_implicit_imports)
        work = os.path.join(tmp, "cwd")
        os.makedirs(work)
        os.chdir(work)     # examples that write files write them here
        try:
            for path in pages:
                rel = os.path.relpath(path, examples)
                with contextlib.redirect_stdout(io.StringIO()):
                    old, new, fences, results = process_page(path, rel, args.timeout, runner, print)
                marked = sum(1 for f in fences if f.skip is None)
                failed = [f for f in fences if f.skip and f.skip.startswith("failed")]
                skipped = [f for f in fences if f.skip and not f.skip.startswith("failed")]
                print("{}: {} marked, {} failed, {} left alone of {} Python fence(s)".format(
                    rel, marked, len(failed), len(skipped), len(fences)))
                for f in failed:
                    print("    {}-{} (line {}): {}".format(page_slug(rel), f.ordinal, f.start + 1, f.skip))
                if args.verbose:
                    for f in skipped:
                        print("    left alone: {}-{} (line {}): {}".format(page_slug(rel), f.ordinal, f.start + 1, f.skip))
                total["marked"] += marked
                total["failed"] += len(failed)
                total["skipped"] += len(skipped)
                total["pages"] += 1 if marked else 0
                if args.write and new != old:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new)
        finally:
            os.chdir(old_cwd)
    print("{} marker(s) {} on {} page(s); {} candidate(s) failed, {} fence(s) left alone".format(
        total["marked"], "written" if args.write else "would be written", total["pages"], total["failed"],
        total["skipped"]))
    if total["marked"] and not args.write:
        print("run again with --write to add them, then ci/build_readouts.py to generate their output")
    return 0


if __name__ == "__main__":
    sys.exit(main())

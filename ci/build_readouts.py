"""
Generates (and caches) the output of the documentation's marked examples, a local build step like
``build_stubs.py``. The result is a committed store, ``ci/docs/readouts``; ``build_docs.py`` only embeds it,
so CI never runs example code.

    python ci/build_readouts.py                     # run examples that have no stored output
    python ci/build_readouts.py --status            # report what is stored, run nothing
    python ci/build_readouts.py --refresh 'water-*' # also re-run examples whose id matches
    python ci/build_readouts.py --refresh stale     # re-run entries made with older library revisions
    python ci/build_readouts.py --refresh all
    python ci/build_readouts.py --prune [--dry-run] # delete stored entries no example refers to

An example is run when its key (a hash of its code, options and the blocks before it on the page) has no
stored entry, so editing an example regenerates it and nothing else does. Failures are stored too, so a broken
example is reported once and not re-run until its code changes or it is refreshed.
"""

import argparse, collections, contextlib, fnmatch, importlib.util, io, os, subprocess, sys, tempfile, shutil

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
if root not in sys.path:
    sys.path.insert(0, root)


def load_doc_config():
    """The same configuration ``build_docs.py`` uses, so the examples found are the ones the docs embed."""
    spec = importlib.util.spec_from_file_location("_build_docs_config", os.path.join(here, "build_docs.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return dict(module.doc_config)


def git_revision(path):
    try:
        out = subprocess.run(["git", "-C", path, "rev-parse", "--short", "HEAD"], capture_output=True, text=True,
                             check=True)
        return out.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def collect_pages(config, verbose=False):
    """Walks the docs exactly as ``build_docs.py`` does, into a scratch directory, recording marked examples."""
    from McUtils.Docs import DocBuilder, ExampleCollector, ExamplesParser
    ExamplesParser.IGNORE_UNHANDLED_STATEMENTS = True
    collector = ExampleCollector()

    class CollectingBuilder(DocBuilder):
        def load_embedder(self):
            self.embedder = None
            return collector

    scratch = tempfile.mkdtemp(prefix="readout-collect-")
    try:
        cfg = dict(config)
        cfg["target"] = scratch
        cfg.pop("readouts", None)
        sink = sys.stdout if verbose else io.StringIO()
        with contextlib.redirect_stdout(sink):
            CollectingBuilder(**cfg).build()
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    return collector


def parse_args(argv, store_default):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--store", default=store_default, help="store directory (default: %(default)s)")
    ap.add_argument("--status", action="store_true", help="report the state of every marked example; run nothing")
    ap.add_argument("--refresh", action="append", metavar="WHAT",
                    help="re-run examples as well: 'all', 'stale', or an id glob (repeatable globs)")
    ap.add_argument("--only", action="append", metavar="GLOB", help="only pages whose object name matches")
    ap.add_argument("--prune", action="store_true", help="delete stored entries that no example refers to")
    ap.add_argument("--dry-run", action="store_true", help="with --prune: list what would be deleted")
    ap.add_argument("--strict", action="store_true", help="exit with status 1 if any example is missing or failed")
    ap.add_argument("--timeout", type=float, default=120.0, help="per-example limit in seconds (default: %(default)s)")
    ap.add_argument("--css", choices=("inline", "stylesheet"), default="inline")
    ap.add_argument("--in-process", action="store_true", help="run examples in this process (debugging only)")
    ap.add_argument("-v", "--verbose", action="store_true", help="show the docs walk and per-example progress")
    args = ap.parse_args(argv)
    if args.prune and args.only:
        ap.error("--prune needs every page, so it can't be combined with --only")
    args.refresh_plan = False
    if args.refresh:
        flags = set(args.refresh)
        globs = [r for r in args.refresh if r not in ("all", "stale")]
        if "all" in flags:
            args.refresh_plan = True
        elif "stale" in flags and globs:
            ap.error("combine --refresh stale with id globs by running twice")
        elif "stale" in flags:
            args.refresh_plan = "stale"
        else:
            args.refresh_plan = globs
    return args


def select_pages(collector, only):
    pages = collector.parsed_pages()
    if only:
        pages = [(o, p) for o, p in pages if any(fnmatch.fnmatchcase(o or "", g) for g in only)]
    return pages


def report_status(store, cache, pages, out=print):
    counts = collections.Counter()
    for owner, parsed in pages:
        for b in parsed.blocks:
            status = cache.status(b)
            counts[status] += 1
            out("  {:8s} {}  [{}]".format(status, b.id, b.key[:8]))
            if status == "error":
                err = (store.read_meta(b.key) or {}).get("error") or {}
                out("           {}: {}".format(err.get("type", "error"), err.get("message", "")))
    css_now = store.stylesheet_md5()
    mismatched = []
    for owner, parsed in pages:
        for b in parsed.blocks:
            meta = store.read_meta(b.key) or {}
            if meta.get("css_md5") and meta["css_md5"] != css_now:
                mismatched.append(b.id)
    out("{} example(s): {}".format(sum(counts.values()), ", ".join(
        "{} {}".format(counts[s], s) for s in ("ok", "stale", "error", "missing") if counts[s]) or "none"))
    if mismatched:
        out("{} example(s) were built against a different mcr.css than the one stored: {}".format(
            len(mismatched), ", ".join(mismatched)))
    return counts, mismatched


def main(argv=None):
    config = load_doc_config()
    store_default = os.path.join(config.get("target", os.path.join(root, "ci", "docs")), "readouts")
    args = parse_args(argv, store_default)

    from McUtils.Docs import ReadoutStore, ExampleCache, ExampleRunner, SubprocessExampleRunner
    store = ReadoutStore(args.store)
    revisions = {p["id"] if isinstance(p, dict) else p: git_revision(root) for p in config.get("packages", [])}
    cache = ExampleCache(store, revisions)

    print("collecting examples from the documentation ...")
    collector = collect_pages(config, verbose=args.verbose)
    pages = select_pages(collector, args.only)
    nblocks = sum(len(p.blocks) for _, p in pages)
    print("{} marked example(s) on {} page(s)".format(nblocks, len(pages)))

    failures = 0
    if args.status:
        counts, mismatched = report_status(store, cache, pages)
        failures = counts["missing"] + counts["error"]
    elif pages:
        Runner = ExampleRunner if args.in_process else SubprocessExampleRunner
        kwargs = dict(revisions=revisions, css=args.css, timeout=args.timeout)
        if not args.in_process:
            kwargs.update(verbose=args.verbose, stream=sys.stdout, cwd=root)
        runner = Runner(store, **kwargs)
        for owner, parsed in pages:
            todo = runner.plan(parsed, args.refresh_plan)
            if not todo:
                continue
            print("{}: running {} example(s)".format(owner, len(todo)))
            for result in runner.run_page(parsed, refresh=args.refresh_plan):
                note = ""
                if result.status == "error":
                    err = result.meta["error"]
                    note = "  {}: {}".format(err["type"], err["message"].splitlines()[0] if err["message"] else "")
                    failures += 1
                elif result.status == "blocked":
                    note = "  (blocked by `{}`)".format(result.blocked_by)
                    failures += 1
                print("  {:8s} {} ({}){}".format(result.status, result.block.id, result.reason, note))
        cache.sync_manifest([b for _, p in pages for b in p.blocks])
        if not any(True for _ in pages):
            pass
    if args.prune:
        keep = [b.key for _, p in pages for b in p.blocks]
        doomed = store.prune(keep, dry_run=args.dry_run)
        live_ids = {b.id for _, p in pages for b in p.blocks}
        stale_ids = [i for i in store.load_manifest().get("entries", {}) if i not in live_ids]
        if not args.dry_run:
            store.update_manifest({}, drop=stale_ids)
        print("{} {} stored entr{}{}".format(
            "would remove" if args.dry_run else "removed", len(doomed), "y" if len(doomed) == 1 else "ies",
            ": " + ", ".join(k[:8] for k in doomed) if doomed else ""))
    if failures:
        print("{} example(s) missing, failed or blocked".format(failures))
    return 1 if (failures and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())

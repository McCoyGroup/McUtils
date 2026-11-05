"""``python -m McUtils.Readouts.Reports REPORT.md --sources MODULE`` serves the report over MCP (stdio)."""
import argparse

from .Serve import serve_report


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m McUtils.Readouts.Reports", description=__doc__)
    p.add_argument("report", help="the report's Markdown file (created if missing, rewritten after every change)")
    p.add_argument("--sources", required=True, help="a .py file or module defining build_catalog() -> SourceCatalog")
    p.add_argument("--out-dir", help="where the render tool writes (default: <report>_out beside the file)")
    p.add_argument("--policy", default="grounded", choices=["grounded", "unchecked", "structure_only"])
    p.add_argument("--rel-tol", type=float, default=1e-3,
                   help="relative tolerance of the number check (default 1e-3; a number also matches within half a "
                        "unit of its last written digit)")
    p.add_argument("--small-int-max", type=int, default=10, help="integers up to this are not checked (default 10)")
    p.add_argument("--check-years", action="store_true",
                   help="also check four-digit numbers between 1900 and 2100 (by default they are taken to be years; "
                        "they overlap frequencies such as 2000 cm-1)")
    p.add_argument("--lock", nargs="+", default=(), metavar="ID", help="lock these blocks against the tools")
    p.add_argument("--unlock", nargs="+", default=(), metavar="ID", help="unlock these blocks")
    p.add_argument("--call-log", metavar="FILE", help="append one JSON line per tool call (tool, arguments, ok, error code)")
    p.add_argument("--title", help="title of a new report")
    a = p.parse_args(argv)
    serve_report(a.report, a.sources, out_dir=a.out_dir, policy=a.policy, rel_tol=a.rel_tol, small_int_max=a.small_int_max,
                 year_range=None if a.check_years else (1900, 2100), title=a.title, lock=a.lock, unlock=a.unlock, call_log=a.call_log)


if __name__ == "__main__":
    main()

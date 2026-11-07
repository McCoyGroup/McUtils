"""``python -m McUtils.Readouts.Reports REPORT.md --sources MODULE`` serves the report over MCP (stdio)."""
import argparse

from .Serve import serve_report


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m McUtils.Readouts.Reports", description=__doc__)
    p.add_argument("report", help="the report's Markdown file (created if missing, rewritten after every change)")
    p.add_argument("--sources", required=True, help="a .py file or module defining build_catalog() -> SourceCatalog")
    p.add_argument("--out-dir", help="where the render tool writes (default: <report>_out beside the file)")
    p.add_argument("--policy", default="unchecked", choices=["grounded", "unchecked", "structure_only"],
                   help="unchecked (default): typed numbers are accepted, counted and commented on; grounded: a typed "
                        "number must be in the cited data and text must cite; structure_only: the model writes no text")
    p.add_argument("--autolink", action="store_true",
                   help="rewrite typed numbers that are exactly a value of the data into placeholders (off by default)")
    p.add_argument("--no-advice", action="store_true",
                   help="leave the notes about typed numbers out of text results (on by default)")
    p.add_argument("--rel-tol", type=float, default=1e-3,
                   help="relative tolerance of the number check and the notes (default 1e-3; a number also matches "
                        "within half a unit of its last written digit)")
    p.add_argument("--small-int-max", type=int, default=10, help="integers up to this are not checked (default 10)")
    p.add_argument("--check-years", action="store_true",
                   help="also check four-digit numbers between 1900 and 2100 (by default they are taken to be years; "
                        "they overlap frequencies such as 2000 cm-1)")
    p.add_argument("--lock", nargs="+", default=(), metavar="ID", help="lock these blocks against the tools")
    p.add_argument("--unlock", nargs="+", default=(), metavar="ID", help="unlock these blocks")
    p.add_argument("--call-log", metavar="FILE", help="append one JSON line per tool call (tool, arguments, ok, error code)")
    p.add_argument("--title", help="title of a new report")
    p.add_argument("--context-level", default="standard", choices=["1", "2", "3", "compact", "standard", "full"],
                   help="how much the model is told and which conveniences it gets: 1/compact for small models "
                        "(short instructions with the sources listed, block order in every receipt), 2/standard "
                        "(default), 3/full (adds the reasons behind the rules); the checks are the same at every level")
    p.add_argument("--tools", nargs="+", default=None, metavar="NAME", help="offer these tools on top of the level's")
    p.add_argument("--no-tools", nargs="+", default=None, metavar="NAME", help="leave these tools out")
    p.add_argument("--derived", action="store_true",
                   help="allow computed values in text ({mean(r3.frequency[2], r3.frequency[3])}); off by default "
                        "(single placeholders like {r3.frequency[2]} are always filled in)")
    p.add_argument("--apply-edits", action="store_true",
                   help="offer the apply_edits tool (several edits in one atomic call); off by default, at every "
                        "context level")
    p.add_argument("--unit-style", choices=["unicode", "ascii", "latex"], default=None,
                   help="how filled values write their unit: unicode (3803.3 cm⁻¹), ascii (3803.3 cm-1) or latex "
                        "($3803.3\\,\\mathrm{cm^{-1}}$); stored in the report (default: the UnitsData label style)")
    a = p.parse_args(argv)
    serve_report(a.report, a.sources, out_dir=a.out_dir, policy=a.policy, rel_tol=a.rel_tol, small_int_max=a.small_int_max,
                 year_range=None if a.check_years else (1900, 2100), title=a.title, lock=a.lock, unlock=a.unlock, call_log=a.call_log,
                 allow_derived=a.derived, apply_edits=a.apply_edits, context_level=a.context_level, include_tools=a.tools,
                 exclude_tools=a.no_tools, unit_style=a.unit_style, autolink=a.autolink, advice=not a.no_advice)


if __name__ == "__main__":
    main()

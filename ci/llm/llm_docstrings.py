#!/usr/bin/env python3
"""
llm_docstrings.py
=================

Add LLM-written docstrings to the functions/methods of a Python file *safely*.

The content of each docstring must be written by a human or an LLM that has
actually read the function -- this tool does NOT generate prose. What it does
is the mechanical, error-prone plumbing around that:

  * find every function/method that lacks a docstring,
  * dump their source so a model can read them,
  * insert supplied docstrings at exactly the right indentation, and
  * verify that *only* docstrings changed (the executable code is untouched).

Typical loop (see the accompanying PROMPTS.md):

    python llm_docstrings.py scan   mymod.py
    python llm_docstrings.py dump   mymod.py --batch 0 --batch-size 20
    #   ... model reads the dump and writes docs.json ...
    python llm_docstrings.py insert mymod.py docs.json
    python llm_docstrings.py verify mymod.py

`insert` writes a `<file>.docbak` backup the first time it runs; `verify` uses
that backup to prove code-identity after docstrings are stripped from both.

Design notes / hard-won lessons baked in:
  * Body indentation is read from the AST's first body statement, NOT assumed
    to be `def`-column + 4 (some code indents bodies unusually, e.g. 8 spaces).
  * The end of a (possibly multi-line) signature is found by tokenizing, so
    default arguments containing ':' or brackets don't confuse placement.
  * A docstring is applied to *every* function matching a qualified name, so
    property/setter pairs (which share a qualname) are both handled.
  * Code-identity is checked by parsing both versions, stripping all
    docstrings, and comparing the `ast.unparse` output.
"""

import argparse
import ast
import io
import json
import os
import sys
import tokenize

DEFAULT_HEADER = "**LLM Docstring**"


# --------------------------------------------------------------------------- #
# AST helpers
# --------------------------------------------------------------------------- #
def _iter_funcs(tree):
    """Yield (qualname, node) for every function/method, in source order."""
    out = []

    class V(ast.NodeVisitor):
        def __init__(self):
            self.stack = []

        def visit_ClassDef(self, n):
            self.stack.append(n.name)
            self.generic_visit(n)
            self.stack.pop()

        def _f(self, n):
            out.append((".".join(self.stack + [n.name]), n))
            self.stack.append(n.name)
            self.generic_visit(n)
            self.stack.pop()

        visit_FunctionDef = _f
        visit_AsyncFunctionDef = _f

    V().visit(tree)
    return out


def _missing(src):
    """Return list of dicts describing functions with no docstring."""
    tree = ast.parse(src)
    res = []
    for qual, n in _iter_funcs(tree):
        if ast.get_docstring(n) is None:
            res.append(
                {
                    "qualname": qual,
                    "lineno": n.lineno,
                    "end_lineno": n.end_lineno,
                    "body_indent": n.body[0].col_offset,
                }
            )
    return res


def _header_end_line(lines, start_line):
    """1-based line where the def signature's closing ':' lives."""
    sub = "\n".join(lines[start_line - 1:])
    toks = tokenize.generate_tokens(io.StringIO(sub).readline)
    depth = 0
    opened = False
    for tok in toks:
        if tok.type == tokenize.OP:
            if tok.string in "([{":
                depth += 1
                opened = True
            elif tok.string in ")]}":
                depth -= 1
            elif tok.string == ":" and depth == 0 and opened:
                return start_line - 1 + tok.end[0]
    raise RuntimeError(f"couldn't find signature end from line {start_line}")


def _strip_docstrings(src):
    """Parse, drop every module/class/function docstring, return unparsed code."""
    tree = ast.parse(src)

    class R(ast.NodeTransformer):
        def _s(self, n):
            self.generic_visit(n)
            b = n.body
            if (
                b
                and isinstance(b[0], ast.Expr)
                and isinstance(getattr(b[0], "value", None), ast.Constant)
                and isinstance(b[0].value.value, str)
            ):
                n.body = b[1:] or [ast.Pass()]
            return n

        visit_FunctionDef = _s
        visit_AsyncFunctionDef = _s
        visit_ClassDef = _s
        visit_Module = _s

    return ast.unparse(ast.fix_missing_locations(R().visit(tree)))


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
def cmd_scan(args):
    src = open(args.file).read()
    miss = _missing(src)
    total = len(_iter_funcs(ast.parse(src)))
    print(f"# {args.file}: {total} functions, {len(miss)} missing docstrings")
    for m in miss:
        print(f"{m['lineno']:6}  {m['qualname']}")
    if args.batch_size:
        n = args.batch_size
        nb = (len(miss) + n - 1) // n
        print(f"\n# {nb} batch(es) of {n} (use: dump --batch N --batch-size {n})")
    return 0


def cmd_dump(args):
    src = open(args.file).read()
    lines = src.splitlines()
    miss = _missing(src)
    if args.batch is not None:
        n = args.batch_size
        miss = miss[args.batch * n:(args.batch + 1) * n]
    for i, m in enumerate(miss):
        s, e = m["lineno"], m["end_lineno"]
        print(f"\n########## {m['qualname']}  (L{s}-{e}) ##########")
        print("\n".join(lines[s - 1:e]))
    return 0


def cmd_keys(args):
    """Print the exact JSON skeleton the model must fill in."""
    src = open(args.file).read()
    skel = {m["qualname"]: "" for m in _missing(src)}
    print(json.dumps(skel, indent=2))
    return 0


def cmd_insert(args):
    path = args.file
    src = open(path).read()
    lines = src.split("\n")

    docs = json.load(open(args.docs))
    header = "" if args.no_header else (args.header + "\n\n")

    miss = _missing(src)
    mset = {m["qualname"] for m in miss}
    dset = set(docs)

    if not args.allow_partial and mset != dset:
        print("ERROR: docs.json keys don't match the missing-docstring set.", file=sys.stderr)
        if mset - dset:
            print("  missing from docs.json:", sorted(mset - dset), file=sys.stderr)
        if dset - mset:
            print("  extra in docs.json (already-documented or unknown):",
                  sorted(dset - mset), file=sys.stderr)
        print("  (pass --allow-partial to insert only the provided subset)", file=sys.stderr)
        return 2

    # backup once
    bak = path + ".docbak"
    if not os.path.exists(bak):
        with open(bak, "w") as f:
            f.write(src)

    ins = []
    applied = 0
    for m in miss:
        q = m["qualname"]
        if q not in docs:
            continue
        body = docs[q]
        if not body.strip():
            continue  # skip empty entries (not yet written)
        bi = " " * m["body_indent"]
        hedln = _header_end_line(lines, m["lineno"])
        text = header + body
        out = [bi + '"""']
        out += [((bi + dl).rstrip() if dl else "") for dl in text.split("\n")]
        out += [bi + '"""']
        ins.append((hedln, out))
        applied += 1

    # apply bottom-up so line numbers stay valid
    for after, out in sorted(ins, key=lambda x: x[0], reverse=True):
        lines[after:after] = out

    # sanity: must still parse
    new_src = "\n".join(lines)
    try:
        ast.parse(new_src)
    except SyntaxError as ex:
        print(f"ERROR: result does not parse ({ex}); file NOT written.", file=sys.stderr)
        return 3

    with open(path, "w") as f:
        f.write(new_src)
    print(f"{path}: inserted {applied} docstring(s); backup at {bak}")
    return 0


def cmd_verify(args):
    path = args.file
    new = open(path).read()

    # 1) parses
    try:
        tree = ast.parse(new)
    except SyntaxError as ex:
        print(f"FAIL parse: {ex}")
        return 1

    # 2) coverage + 3) header
    header = None if args.no_header else args.header
    funcs = _iter_funcs(tree)
    missing = [q for q, n in funcs if ast.get_docstring(n) is None]

    # Only hold the header check against functions we actually documented.
    # If --docs is given, scope to those qualnames; otherwise header mismatches
    # are reported as an informational note (they may be pre-existing human
    # docstrings) and do NOT fail the run.
    scoped = None
    if args.docs and os.path.exists(args.docs):
        scoped = set(json.load(open(args.docs)))
    badhdr = []
    if header is not None:
        for q, n in funcs:
            if scoped is not None and q not in scoped:
                continue
            d = ast.get_docstring(n)
            if d is not None and not d.lstrip().startswith(header):
                badhdr.append(q)
    header_fails_run = scoped is not None

    # 4) code-identity vs backup (or --original)
    ref = args.original or (path + ".docbak")
    code_same = None
    if os.path.exists(ref):
        code_same = _strip_docstrings(open(ref).read()) == _strip_docstrings(new)
    else:
        print(f"NOTE: no reference ({ref}) for code-identity check; skipping it.")

    total = len(funcs)
    ok = (not missing) and (code_same in (True, None)) and (not (header_fails_run and badhdr))
    hdr_label = "non_llm_header" if header_fails_run else "non_llm_header(info)"
    print(f"{path}: total={total} missing={len(missing)} "
          f"{hdr_label}={len(badhdr)} code_identical={code_same}")
    if missing and args.show:
        print("  missing:", missing)
    if badhdr and args.show:
        note = "" if header_fails_run else "  (informational; likely pre-existing human docstrings)"
        print("  header-not-matching:", badhdr, note)
    print("PASS" if ok else "REVIEW NEEDED")
    return 0 if ok else 1


def cmd_restore(args):
    bak = args.file + ".docbak"
    if not os.path.exists(bak):
        print(f"no backup at {bak}", file=sys.stderr)
        return 1
    with open(args.file, "w") as f:
        f.write(open(bak).read())
    print(f"restored {args.file} from {bak}")
    return 0


# --------------------------------------------------------------------------- #
def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_common(sp):
        sp.add_argument("file")

    s = sub.add_parser("scan", help="list functions missing docstrings")
    add_common(s)
    s.add_argument("--batch-size", type=int, default=0)
    s.set_defaults(func=cmd_scan)

    s = sub.add_parser("dump", help="print source of missing functions")
    add_common(s)
    s.add_argument("--batch", type=int, default=None)
    s.add_argument("--batch-size", type=int, default=20)
    s.set_defaults(func=cmd_dump)

    s = sub.add_parser("keys", help="print JSON skeleton of missing qualnames")
    add_common(s)
    s.set_defaults(func=cmd_keys)

    s = sub.add_parser("insert", help="insert docstrings from a JSON file")
    add_common(s)
    s.add_argument("docs", help="JSON mapping qualname -> docstring body")
    s.add_argument("--header", default=DEFAULT_HEADER,
                   help=f"header line prepended to each docstring (default: {DEFAULT_HEADER!r})")
    s.add_argument("--no-header", action="store_true", help="don't prepend any header")
    s.add_argument("--allow-partial", action="store_true",
                   help="allow docs.json to cover only some of the missing functions")
    s.set_defaults(func=cmd_insert)

    s = sub.add_parser("verify", help="check parse/coverage/header/code-identity")
    add_common(s)
    s.add_argument("--header", default=DEFAULT_HEADER)
    s.add_argument("--no-header", action="store_true")
    s.add_argument("--original", default=None,
                   help="reference file for code-identity (default: <file>.docbak)")
    s.add_argument("--docs", default=None,
                   help="scope the header check to the qualnames in this JSON "
                        "(otherwise header mismatches are only informational)")
    s.add_argument("--show", action="store_true", help="list any offending qualnames")
    s.set_defaults(func=cmd_verify)

    s = sub.add_parser("restore", help="restore the file from its .docbak backup")
    add_common(s)
    s.set_defaults(func=cmd_restore)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

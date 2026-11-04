#!/usr/bin/env python
"""
Installs the ActiveHTMLWidget frontend extension (JupyterLab and the classic notebook) for the Python that runs
this script. It needs only the standard library, so run it with the Python that launched Jupyter, which is not
necessarily the notebook's kernel:

    !/path/to/jupyter/python /path/to/McUtils/Jupyter/JHTML/ActiveHTMLWidget/install_extension.py

``JHTML.install_command()`` (and the message shown when the extension is missing or out of date) prints that line
with both paths filled in.

Options:
    --prefix DIR    install under DIR/share/jupyter instead of ``sys.prefix``
    --source DIR    the folder holding ``labextension`` and ``nbextension`` (default: next to this script)
    --dry-run       say what would be done and change nothing

An existing copy is replaced (the old one is kept until the new one is in place and put back if that fails). Reload
the browser page afterwards (hard reload: Cmd+Shift+R or Ctrl+Shift+R); no kernel restart is needed.
"""
import argparse
import os
import shutil
import sys
import tempfile

NAME = "ActiveHTMLWidget"
KINDS = ("labextension", "nbextension")


def install(source, target, dry_run=False):
    """Copies ``source`` to ``target``, replacing what is there. Returns a one-line description of what happened."""
    replaced = os.path.exists(target)
    if dry_run:
        return "would {} {}".format("replace" if replaced else "install", target)
    parent = os.path.dirname(target)
    os.makedirs(parent, exist_ok=True)
    staging = tempfile.mkdtemp(prefix=".activehtml-", dir=parent)
    try:
        fresh = os.path.join(staging, "new")
        shutil.copytree(source, fresh)
        backup = os.path.join(staging, "old")
        try:
            if replaced:
                os.replace(target, backup)
            os.replace(fresh, target)
        except BaseException:
            if os.path.exists(backup) and not os.path.exists(target):
                os.replace(backup, target)
            raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    return "{} {}".format("replaced" if replaced else "installed", target)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Install the {} extension for this Python.".format(NAME))
    parser.add_argument("--prefix", default=sys.prefix)
    parser.add_argument("--source", default=os.path.dirname(os.path.abspath(__file__)))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    print("python: {}\nprefix: {}".format(sys.executable, args.prefix))
    done = 0
    for kind in KINDS:
        source = os.path.join(args.source, kind)
        if not os.path.isdir(source):
            print("skipped {}: {} not found".format(kind, source))
            continue
        target = os.path.join(args.prefix, "share", "jupyter", kind + "s", NAME)
        try:
            print(install(source, target, args.dry_run))
        except OSError as e:
            print("FAILED {}: {}".format(kind, e))
            return 1
        done += 1
    if not done:
        print("nothing installed: no extension folders under {}".format(args.source))
        return 1
    if not args.dry_run:
        print("Done. Hard-reload the browser page (Cmd+Shift+R / Ctrl+Shift+R); no kernel restart is needed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

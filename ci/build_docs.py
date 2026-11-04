
import os, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
target = os.path.join(root, "ci", "docs")
sys.path.insert(0, root)
doc_config = {
    "config": {
        "title": "McUtils Dev Branch Documentation",
        "path": "McUtils",
        "url": "https://mccoygroup.github.io/McUtils/",
        "gh_username": "McCoyGroup",
        "gh_repo": "McUtils",
        "gh_branch": "master",
        "footer": "Brought to you by the McCoy Group"
    },
    "packages": [
        {
            "id": "McUtils",
            'tests_root': os.path.join(root, "ci", "tests")
        }
    ],
    "root": root,
    "target": target,
    "readme": os.path.join(root, "README.md"),
    'templates_directory': os.path.join(root, 'ci', 'docs', 'templates'),
    'examples_directory': os.path.join(root, 'ci',  'docs', 'examples')
}

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(
        description="Builds the documentation pages into ci/docs. Stored example output (made by "
                    "ci/build_readouts.py) is embedded when the store exists; no example code is run here."
    )
    ap.add_argument("--target", default=target,
                    help="where to write the site (default: %(default)s); use a scratch directory to keep the repo clean")
    ap.add_argument("--readouts", default=os.path.join(target, "readouts"), help="the readout store (default: %(default)s)")
    ap.add_argument("--no-readouts", action="store_true", help="don't embed stored example output")
    ap.add_argument("--strict-readouts", action="store_true",
                    help="fail the build if a marked example has no stored output or a failed one")
    ap.add_argument("--readout-debug", action="store_true",
                    help="add a badge to each page showing how many readouts loaded (for checking the built site)")
    args = ap.parse_args()

    from McUtils.Docs import *
    ExamplesParser.IGNORE_UNHANDLED_STATEMENTS = True
    config = dict(doc_config, target=os.path.abspath(args.target))
    if not args.no_readouts and os.path.isdir(args.readouts):
        config["readouts"] = {"store": args.readouts, "strict": args.strict_readouts, "debug": args.readout_debug}
    DocBuilder(**config).build()

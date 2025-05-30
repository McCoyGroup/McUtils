
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
    from McUtils.Docs import *
    ExamplesParser.IGNORE_UNHANDLED_STATEMENTS = True
    DocBuilder(**doc_config).build()
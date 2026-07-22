"""Extracted from DocsTests.test_McUtilsDoc via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest DocsTests.test_McUtilsDoc"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Docs import *
import os, inspect

class DocsTests(TestCase):
    """
    Sample documentation generator tests
    """

    @validationTest
    def test_McUtilsDoc(self):
        """
        Builds sample documentation for the Peeves package

        :return:
        :rtype:
        """
        import os, tempfile
        root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        td = '/var/folders/9t/tqc70b7d61v753jkdbjkvd640000gp/T/tmpo3b4ztrq/'
        target = os.path.join(td, 'docs')
        doc_config = {'config': {'title': 'McUtils Dev Branch Documentation', 'path': 'McUtils', 'url': 'https://mccoygroup.github.io/McUtils/', 'gh_username': 'McCoyGroup', 'gh_repo': 'McUtils', 'gh_branch': 'master', 'footer': 'Brought to you by the McCoy Group'}, 'packages': [{'id': 'McUtils', 'tests_root': os.path.join(root, 'ci', 'tests')}], 'root': root, 'target': target, 'readme': os.path.join(root, 'README.md'), 'templates_directory': os.path.join(root, 'ci', 'docs', 'templates'), 'examples_directory': os.path.join(root, 'ci', 'docs', 'examples')}
        DocBuilder(**doc_config).build()

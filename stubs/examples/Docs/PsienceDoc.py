"""Extracted from DocsTests.test_PsienceDoc via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest DocsTests.test_PsienceDoc"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Docs import *
import os, inspect

class DocsTests(TestCase):
    """
    Sample documentation generator tests
    """

    @debugTest
    def test_PsienceDoc(self):
        """
        Builds sample documentation for the Peeves package

        :return:
        :rtype:
        """
        import os, tempfile
        root = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'Psience')
        td = '/var/folders/9t/tqc70b7d61v753jkdbjkvd640000gp/T/tmpo3b4ztrq/'
        target = os.path.join(td, 'docs')
        doc_config = {'config': {'title': 'Psience Dev Branch Documentation', 'path': 'McUtils', 'url': 'https://mccoygroup.github.io/McUtils/', 'gh_username': 'McCoyGroup', 'gh_repo': 'Psience', 'gh_branch': 'master', 'footer': 'Brought to you by the McCoy Group'}, 'packages': [{'id': 'Psience', 'tests_root': os.path.join(root, 'ci', 'tests')}], 'root': root, 'target': target, 'readme': os.path.join(root, 'README.md'), 'templates_directory': os.path.join(root, 'ci', 'docs', 'templates'), 'examples_directory': os.path.join(root, 'ci', 'docs', 'examples')}
        DocBuilder(**doc_config).build()

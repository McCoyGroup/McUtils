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
        # with tempfile.TemporaryDirectory() as td:
        td = '/var/folders/9t/tqc70b7d61v753jkdbjkvd640000gp/T/tmpo3b4ztrq/'
        target = os.path.join(td, "docs")
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
            'examples_directory': os.path.join(root, 'ci', 'docs', 'examples')
        }
        DocBuilder(**doc_config).build()

    @debugTest
    def test_PsienceDoc(self):
        """
        Builds sample documentation for the Peeves package

        :return:
        :rtype:
        """

        import os, tempfile

        root = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'Psience'
        )
        # with tempfile.TemporaryDirectory() as td:
        td = '/var/folders/9t/tqc70b7d61v753jkdbjkvd640000gp/T/tmpo3b4ztrq/'
        target = os.path.join(td, "docs")
        doc_config = {
            "config": {
                "title": "Psience Dev Branch Documentation",
                "path": "McUtils",
                "url": "https://mccoygroup.github.io/McUtils/",
                "gh_username": "McCoyGroup",
                "gh_repo": "Psience",
                "gh_branch": "master",
                "footer": "Brought to you by the McCoy Group"
            },
            "packages": [
                {
                    "id": "Psience",
                    'tests_root': os.path.join(root, "ci", "tests")
                }
            ],
            "root": root,
            "target": target,
            "readme": os.path.join(root, "README.md"),
            'templates_directory': os.path.join(root, 'ci', 'docs', 'templates'),
            'examples_directory': os.path.join(root, 'ci', 'docs', 'examples')
        }
        DocBuilder(**doc_config).build()

    @validationTest
    def test_ParseExamples(self):
        parser = ExamplesParser.from_file(os.path.abspath(__file__))
        self.assertTrue(hasattr(parser.functions, 'items'))
        # tests = ExamplesParser.parse_tests(os.path.abspath(__file__))
        # print(tests.format_tex())

    @validationTest
    def test_FormatSpec(self):
        fmt = inspect.cleandoc("""
        ### My Data

        {$:b=loop(add_temp, l1, l2, slots=['l1', 'l2'])}
        {$:len(b) ** 2}


        """)

        print("",
              TemplateFormatter().format(fmt, param=2, l1=[1, 2, 3], l2=[4, 5, 6], add_temp='{l1} + {l2}', p1=1, p2=0),
              sep="\n"
              )


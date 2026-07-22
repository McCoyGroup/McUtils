# <a id="McUtils.Docs">McUtils.Docs</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/__init__.py#L1?message=Update%20Docs)]
</div>
    
Adapted from the Peeves documentation system but tailored for more interactive usage.

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[DocBuilder](Docs/DocsBuilder/DocBuilder.md)   
</div>
   <div class="col" markdown="1">
[DocWalker](Docs/DocWalker/DocWalker.md)   
</div>
   <div class="col" markdown="1">
[ModuleWriter](Docs/DocWalker/ModuleWriter.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ClassWriter](Docs/DocWalker/ClassWriter.md)   
</div>
   <div class="col" markdown="1">
[FunctionWriter](Docs/DocWalker/FunctionWriter.md)   
</div>
   <div class="col" markdown="1">
[MethodWriter](Docs/DocWalker/MethodWriter.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ObjectWriter](Docs/DocWalker/ObjectWriter.md)   
</div>
   <div class="col" markdown="1">
[IndexWriter](Docs/DocWalker/IndexWriter.md)   
</div>
   <div class="col" markdown="1">
[jdoc](Docs/DocWalker/jdoc.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[JHTMLDocumentationEngine](Docs/HTMLDocs/JHTMLDocumentationEngine.md)   
</div>
   <div class="col" markdown="1">
[static_doc](Docs/HTMLDocs/static_doc.md)   
</div>
   <div class="col" markdown="1">
[StubSummaryBuilder](Docs/Stubs/StubSummaryBuilder.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ExamplesParser](Docs/ExamplesParser/ExamplesParser.md)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>





## Examples
**LLM Examples**

### Display rich API documentation in Jupyter

```python
from McUtils.Docs import jdoc
from McUtils.Zachary import FiniteDifferenceDerivative

documentation = jdoc(
    FiniteDifferenceDerivative,
    max_depth=2,
    verbose=False
)
documentation.display()
```

### Extract examples from a test module

```python
from McUtils.Docs import ExamplesParser

examples = ExamplesParser.from_file("ci/tests/ZacharyTests.py")
names = list(examples.functions)
finite_difference_examples = [name for name in names if "Deriv" in name]
print("all documented functions:", len(names))
print("finite-difference examples:", finite_difference_examples)
```

### Build package stubs and summaries

```python
from McUtils.Docs import StubSummaryBuilder

builder = StubSummaryBuilder(
    root_src_dir="McUtils",
    out_dir="stubs"
)
summary = builder.generate_all("McUtils")
print("stub bytes:", summary["stub_size"])
print("summary bytes:", summary["summary_size"])
```

### Render static HTML documentation

```python
from McUtils.Docs import static_doc
from McUtils.Combinatorics import UniquePermutations

html = static_doc(
    UniquePermutations, max_depth=2,
    title="Unique permutation API", return_string=True
)
print("generated HTML characters:", len(html))
```

### Walk an object hierarchy

```python
from McUtils.Docs import DocWalker
from McUtils import Numputils

walker = DocWalker(description="Numerical utility API")
documentation = walker.visit_root(Numputils, max_depth=1)
print(documentation)
```

### Build a documentation site

```python
from McUtils.Docs import DocBuilder

builder = DocBuilder(
    root=".", target="build/docs", readme="README.md",
    packages=[{"id": "McUtils", "tests_root": "ci/tests"}],
    config={"title": "McUtils API", "path": "McUtils"}
)
builder.build()
```













<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#Tests-d098e6" markdown="1"> Tests</a> <a class="float-right" data-toggle="collapse" href="#Tests-d098e6"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Tests-d098e6" markdown="1">
 - [McUtilsDoc](#McUtilsDoc)
- [PsienceDoc](#PsienceDoc)
- [ParseExamples](#ParseExamples)

<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
### <a class="collapse-link" data-toggle="collapse" href="#Setup-f43f27" markdown="1"> Setup</a> <a class="float-right" data-toggle="collapse" href="#Setup-f43f27"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Setup-f43f27" markdown="1">
 
Before we can run our examples we should get a bit of setup out of the way.
Since these examples were harvested from the unit tests not all pieces
will be necessary for all situations.

All tests are wrapped in a test class
```python
class DocsTests(TestCase):
    """
    Sample documentation generator tests
    """
```

 </div>
</div>

#### <a name="McUtilsDoc">McUtilsDoc</a>
```python
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
```

#### <a name="PsienceDoc">PsienceDoc</a>
```python
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
```

#### <a name="ParseExamples">ParseExamples</a>
```python
    def test_ParseExamples(self):
        parser = ExamplesParser.from_file(os.path.abspath(__file__))
        self.assertTrue(hasattr(parser.functions, 'items'))
```

 </div>
</div>






---


<div markdown="1" class="text-secondary">
<div class="container">
  <div class="row">
   <div class="col" markdown="1">
**Feedback**   
</div>
   <div class="col" markdown="1">
**Examples**   
</div>
   <div class="col" markdown="1">
**Templates**   
</div>
   <div class="col" markdown="1">
**Documentation**   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Bug](https://github.com/McCoyGroup/McUtils/issues/new?title=Documentation%20Improvement%20Needed)/[Request](https://github.com/McCoyGroup/McUtils/issues/new?title=Example%20Request)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/__init__.py#L1?message=Update%20Docs)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>
</div>
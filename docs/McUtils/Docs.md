# <a id="McUtils.Docs">McUtils.Docs</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Docs/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Docs/__init__.py#L1?message=Update%20Docs)]
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
[ExamplesParser](Docs/ExamplesParser/ExamplesParser.md)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>





## Examples













<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#Tests-6f187d" markdown="1"> Tests</a> <a class="float-right" data-toggle="collapse" href="#Tests-6f187d"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Tests-6f187d" markdown="1">
 - [McUtilsDoc](#McUtilsDoc)
- [PsienceDoc](#PsienceDoc)
- [ParseExamples](#ParseExamples)
- [FormatSpec](#FormatSpec)

<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
### <a class="collapse-link" data-toggle="collapse" href="#Setup-665cd4" markdown="1"> Setup</a> <a class="float-right" data-toggle="collapse" href="#Setup-665cd4"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Setup-665cd4" markdown="1">
 
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

#### <a name="FormatSpec">FormatSpec</a>
```python
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Docs/__init__.py#L1?message=Update%20Docs)   
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
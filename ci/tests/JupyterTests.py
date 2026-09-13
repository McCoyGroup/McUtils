
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Jupyter import *
import McUtils.Jupyter as interactive
import numpy as np
import os, tempfile

class JupyterTests(TestCase):

    @validationTest
    def test_HTML(self):
        Div = JHTML.HTML.Div
        JHTML.Bootstrap.Panel(
            JHTML.Bootstrap.Grid(np.random.rand(5, 5).round(3).tolist()),
            header='Test Panel',
            variant='primary'
        ).tostring()

    @validationTest
    def test_Styles(self):
        JHTML.CSS.parse("""
a {
  text-variant:none;
}
        """)[0].tostring()

    @validationTest
    def test_WidgetConstruction(self):
        from Psience.Molecools import Molecule
        water = Molecule.from_string('O', 'smi')
        widg = interactive.JHTML.Div(water.plot(backend='x3d').figure.to_x3d(), dynamic=True)
        print(widg.elem.children[0].children)

    @validationTest
    def test_WidgetInteractivity(self):
        import McUtils.Jupyter as interactive
        from Psience.Molecools import Molecule

        reactant = Molecule.from_string("CCO", "smi")

        p = reactant.plot(backend='x3d')

        print(type(
            interactive.Grid([[
                p, p
            ]], dynamic=False).to_jhtml()
        ))

        print(type(
            interactive.Carousel([
                p, p
            ], dynamic=False).to_jhtml()
        ))

    @validationTest
    def test_SVG(self):
        SVG = JHTML.SVGContext

        uuh = SVG.Svg(
                SVG.Rect(x=0, y=0, width=10, height=10),
            )
        uuh.display()
        # print(uuh.tostring(prettify=True))

    simple_markdown = """# Title
Some description text.

```python
import numpy as np
x = np.arange(10)
print(x)
```

More text after.

```bash
echo hello
```
"""

    # --- add near the top of JupyterTests.py ---
    # import os, tempfile as tmpf

    # --- add inside class JupyterTests(TestCase): ---

    @validationTest
    def test_NotebookWriterFromMarkdownBlocks(self):
        blocks = NotebookWriter.from_markdown(self.simple_markdown)

        self.assertEqual([b[0] for b in blocks], ['markdown', 'code', 'markdown', 'markdown'])
        self.assertTrue(blocks[0][1].startswith('# Title'))
        self.assertEqual(blocks[1][1], 'import numpy as np\nx = np.arange(10)\nprint(x)')
        self.assertIn('More text after.', blocks[2][1])
        self.assertIn('```bash', blocks[3][1])

    @validationTest
    def test_NotebookWriterToJSON(self):
        writer = NotebookWriter(NotebookWriter.from_markdown(self.simple_markdown))
        nb = writer.to_json()

        self.assertEqual(nb['nbformat'], 4)
        self.assertIn('kernelspec', nb['metadata'])

        cells = nb['cells']
        self.assertEqual(len(cells), 4)

        self.assertEqual(cells[0]['cell_type'], 'markdown')
        self.assertTrue(''.join(cells[0]['source']).startswith('# Title'))

        self.assertEqual(cells[1]['cell_type'], 'code')
        self.assertEqual(
            ''.join(cells[1]['source']),
            'import numpy as np\nx = np.arange(10)\nprint(x)'
        )
        self.assertIsNone(cells[1]['execution_count'])
        self.assertEqual(cells[1]['outputs'], [])

        self.assertEqual(cells[2]['cell_type'], 'markdown')
        self.assertIn('More text after.', ''.join(cells[2]['source']))

    @debugTest
    def test_NotebookWriterNonPythonFenceStaysMarkdown(self):
        writer = NotebookWriter(NotebookWriter.from_markdown(self.simple_markdown))
        cells = writer.to_json()['cells']

        # the `bash` fence isn't a recognized code language, so it should
        # remain inline inside a markdown cell rather than becoming a code cell
        last_cell = cells[-1]
        self.assertEqual(last_cell['cell_type'], 'markdown')
        self.assertIn('```bash', ''.join(last_cell['source']))
        self.assertEqual(sum(1 for c in cells if c['cell_type'] == 'code'), 1)

        nb_dir = os.path.expanduser('~/Documents/Notebooks/tmp')
        root_dir = os.path.expanduser('~/Documents/')
        os.makedirs(nb_dir, exist_ok=True)
        writer.open_temp(8844, notebook_directory=nb_dir, root_dir=root_dir, browser='safari')

    @validationTest
    def test_NotebookWriterNoCodeFences(self):
        blocks = NotebookWriter.from_markdown("# Just Text\n\nNo code here, just prose.\n")
        cells = NotebookWriter(blocks).to_json()['cells']
        self.assertEqual(len(cells), 1)
        self.assertEqual(cells[0]['cell_type'], 'markdown')

    @validationTest
    def test_NotebookWriterCustomCodeLanguages(self):
        md = """# Header

```julia
println("hi")
```
"""
        blocks = NotebookWriter.from_markdown(md, code_languages=['julia'])
        cells = NotebookWriter(blocks).to_json()['cells']
        code_cells = [c for c in cells if c['cell_type'] == 'code']
        self.assertEqual(len(code_cells), 1)
        self.assertEqual(''.join(code_cells[0]['source']), 'println("hi")')

    @validationTest
    def test_NotebookWriterWriteToDisk(self):
        with tempfile.NamedTemporaryFile(suffix=".ipynb") as nb_file:
            nb_path = nb_file.name
        try:
            writer = NotebookWriter(NotebookWriter.from_markdown(self.simple_markdown))
            ret = writer.write(nb_path)
            self.assertEqual(ret, nb_path)
            self.assertTrue(os.path.exists(nb_path))

            reader = NotebookReader(nb_path)
            self.assertEqual(len(reader.cell_list()), 4)
            self.assertEqual(reader.get_notebook_name(), "Title")
        finally:
            if os.path.exists(nb_path):
                os.remove(nb_path)
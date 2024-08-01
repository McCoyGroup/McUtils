## <a id="McUtils.GaussianInterface.GaussianImporter.GaussianFChkReader">GaussianFChkReader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/GaussianInterface/GaussianImporter.py#L151)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/GaussianInterface/GaussianImporter.py#L151?message=Update%20Docs)]
</div>

Implements a stream based reader for a Gaussian .fchk file. Pretty generall I think. Should be robust-ish.
One place to change things up is convenient parsers for specific commonly pulled parts of the fchk







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse " id="methods" markdown="1">
 ```python
GaussianFChkReaderException: GaussianFChkReaderException
registered_components: dict
common_names: dict
to_common_name: dict
fchk_re_pattern: str
fchk_re: Pattern
```
<a id="McUtils.GaussianInterface.GaussianImporter.GaussianFChkReader.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, file, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/GaussianInterface/GaussianImporter/GaussianFChkReader.py#L162)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/GaussianInterface/GaussianImporter/GaussianFChkReader.py#L162?message=Update%20Docs)]
</div>


<a id="McUtils.GaussianInterface.GaussianImporter.GaussianFChkReader.read_header" class="docs-object-method">&nbsp;</a> 
```python
read_header(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/GaussianInterface/GaussianImporter/GaussianFChkReader.py#L167)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/GaussianInterface/GaussianImporter/GaussianFChkReader.py#L167?message=Update%20Docs)]
</div>
Reads the header and skips the stream to where we want to be
  - `:returns`: `str`
    > t
h
e
 
h
e
a
d
e
r


<a id="McUtils.GaussianInterface.GaussianImporter.GaussianFChkReader.get_next_block_params" class="docs-object-method">&nbsp;</a> 
```python
get_next_block_params(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/GaussianInterface/GaussianImporter/GaussianFChkReader.py#L177)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/GaussianInterface/GaussianImporter/GaussianFChkReader.py#L177?message=Update%20Docs)]
</div>
Pulls the tag of the next block, the type, the number of bytes it'll be,
and if it's a single-line block it'll also spit back the block itself
  - `:returns`: `dict`
    >


<a id="McUtils.GaussianInterface.GaussianImporter.GaussianFChkReader.get_block" class="docs-object-method">&nbsp;</a> 
```python
get_block(self, name=None, dtype=None, byte_count=None, value=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/GaussianInterface/GaussianImporter/GaussianFChkReader.py#L243)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/GaussianInterface/GaussianImporter/GaussianFChkReader.py#L243?message=Update%20Docs)]
</div>
Pulls the next block by first pulling the block tag
  - `:returns`: `_`
    >


<a id="McUtils.GaussianInterface.GaussianImporter.GaussianFChkReader.skip_block" class="docs-object-method">&nbsp;</a> 
```python
skip_block(self, name=None, dtype=None, byte_count=None, value=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/GaussianInterface/GaussianImporter/GaussianFChkReader.py#L270)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/GaussianInterface/GaussianImporter/GaussianFChkReader.py#L270?message=Update%20Docs)]
</div>
Skips the next block
  - `:returns`: `_`
    >


<a id="McUtils.GaussianInterface.GaussianImporter.GaussianFChkReader.num_atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
num_atoms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/GaussianInterface/GaussianImporter/GaussianFChkReader.py#L280)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/GaussianInterface/GaussianImporter/GaussianFChkReader.py#L280?message=Update%20Docs)]
</div>


<a id="McUtils.GaussianInterface.GaussianImporter.GaussianFChkReader.parse" class="docs-object-method">&nbsp;</a> 
```python
parse(self, keys=None, default='raise'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/GaussianInterface/GaussianImporter/GaussianFChkReader.py#L285)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/GaussianInterface/GaussianImporter/GaussianFChkReader.py#L285?message=Update%20Docs)]
</div>


<a id="McUtils.GaussianInterface.GaussianImporter.GaussianFChkReader.read_props" class="docs-object-method">&nbsp;</a> 
```python
read_props(file, keys): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/GaussianInterface/GaussianImporter/GaussianFChkReader.py#L355)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/GaussianInterface/GaussianImporter/GaussianFChkReader.py#L355?message=Update%20Docs)]
</div>
 </div>
</div>




## Examples
```python

def test_Fchk(self):
    with GaussianFChkReader(self.test_fchk) as reader:
        parse = reader.parse()
    key = next(iter(parse.keys()))
    self.assertIsInstance(key, str)


def test_ForceConstants(self):
    n = 3 # water
    with GaussianFChkReader(self.test_fchk) as reader:
        parse = reader.parse("ForceConstants")
    fcs = parse["ForceConstants"]
    self.assertEquals(fcs.n, n)
    self.assertEquals(fcs.array.shape, (3*n, 3*n))


def test_ForceThirdDerivatives(self):
    n = 3 # water
    with GaussianFChkReader(self.test_fchk) as reader:
        parse = reader.parse("ForceDerivatives")
    fcs = parse["ForceDerivatives"]
    tds = fcs.third_deriv_array
    self.assertEquals(fcs.n, n)
    self.assertEquals(tds.shape, ((3*n-6), (3*n), 3*n))
    a = tds[0]
    self.assertTrue(
        np.allclose(tds[0], tds[0].T, rtol=1e-08, atol=1e-08)
    )
    self.assertTrue(
        np.allclose(tds[1], tds[1].T, rtol=1e-08, atol=1e-08)
    )
    self.assertTrue(
        np.allclose(tds[2], tds[2].T, rtol=1e-08, atol=1e-08)
    )


def test_ForceFourthDerivatives(self):
    n = 3 # water
    with GaussianFChkReader(self.test_fchk) as reader:
        parse = reader.parse("ForceDerivatives")
    fcs = parse["ForceDerivatives"]
    tds = fcs.fourth_deriv_array
    self.assertEquals(fcs.n, n)
    self.assertEquals(tds.shape, ((3*n-6), (3*n-6), (3*n), 3*n)) # it's a SparseTensor now
    slice_0 = tds[0, 0].toarray()
    slice_1 = tds[1, 1].toarray()
    slice_2 = tds[2, 2].toarray()
    self.assertTrue(
        np.allclose(slice_0, slice_0.T, rtol=1e-08, atol=1e-08)
    )
    self.assertTrue(
        np.allclose(slice_1, slice_1.T, rtol=1e-08, atol=1e-08)
    )
    self.assertTrue(
        np.allclose(slice_2, slice_2.T, rtol=1e-08, atol=1e-08)
    )


def test_FchkMasses(self):
    n = 3 # water
    with GaussianFChkReader(self.test_fchk) as reader:
        parse = reader.parse("AtomicMasses")
    masses = parse["AtomicMasses"]
    self.assertEquals(len(masses), n)
```






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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/GaussianInterface/GaussianImporter/GaussianFChkReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/GaussianInterface/GaussianImporter/GaussianFChkReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/GaussianInterface/GaussianImporter/GaussianFChkReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/GaussianInterface/GaussianImporter/GaussianFChkReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/GaussianInterface/GaussianImporter.py#L151?message=Update%20Docs)   
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
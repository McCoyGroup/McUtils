## <a id="McUtils.ExternalPrograms.Parsers.GaussianImporter.GaussianLogReader">GaussianLogReader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/Parsers/GaussianImporter.py#L23)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/Parsers/GaussianImporter.py#L23?message=Update%20Docs)]
</div>

Implements a stream based reader for a Gaussian .log file.
This is inherits from the `FileStreamReader` base, and takes a two pronged approach to getting data.
First, a block is found in a log file based on a pair of tags.
Next, a function (usually based on a `StringParser`) is applied to this data to convert it into a usable data format.
The goal is to move toward wrapping all returned data in a `QuantityArray` so as to include data type information, too.

You can see the full list of available keys in the `GaussianLogComponents` module, but currently they are:
* `"Header"`: the header for the Gaussian job
* `"InputZMatrix"`: the string of the input Z-matrix
* `"CartesianCoordinates"`: all the Cartesian coordinates in the file
* `"ZMatCartesianCoordinates"`: all of the Cartesian coordinate in Z-matrix orientation
* `"StandardCartesianCoordinates"`: all of the Cartesian coordinates in 'standard' orientation
* `"InputCartesianCoordinates"`: all of the Cartesian coordinates in 'input' orientation
* `"ZMatrices"`: all of the Z-matrices
* `"OptimizationParameters"`: all of the optimization parameters
* `"MullikenCharges"`: all of the Mulliken charges
* `"MultipoleMoments"`: all of the multipole moments
* `"DipoleMoments"`: all of the dipole moments
* `"OptimizedDipoleMoments"`: all of the dipole moments from an optimized scan
* `"ScanEnergies"`: the potential surface information from a scan
* `"OptimizedScanEnergies"`: the PES from an optimized scan
* `"XMatrix"`: the anharmonic X-matrix from Gaussian's style of perturbation theory
* `"Footer"`: the footer from a calculation

You can add your own types, too.
If you need something we don't have, give `GaussianLogComponents` a look to see how to add it in.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
registered_components: OrderedDict
default_keys: tuple
default_ordering: dict
job_default_keys: dict
```
<a id="McUtils.ExternalPrograms.Parsers.GaussianImporter.GaussianLogReader.parse" class="docs-object-method">&nbsp;</a> 
```python
parse(self, keys=None, num=None, reset=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/Parsers/GaussianImporter/GaussianLogReader.py#L58)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/Parsers/GaussianImporter/GaussianLogReader.py#L58?message=Update%20Docs)]
</div>
The main function we'll actually use. Parses bits out of a .log file.
  - `keys`: `str or list(str)`
    > the keys we'd like to read from the log file
  - `num`: `int or None`
    > for keys with multiple entries, the number of entries to pull
  - `:returns`: `dict`
    > t
h
e
 
d
a
t
a
 
p
u
l
l
e
d
 
f
r
o
m
 
t
h
e
 
l
o
g
 
f
i
l
e
,
 
s
t
r
u
n
g
 
t
o
g
e
t
h
e
r
 
a
s
 
a
 
`
d
i
c
t
`
 
a
n
d
 
k
e
y
e
d
 
b
y
 
t
h
e
 
_
k
e
y
s
_


<a id="McUtils.ExternalPrograms.Parsers.GaussianImporter.GaussianLogReader.get_default_keys" class="docs-object-method">&nbsp;</a> 
```python
get_default_keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/ExternalPrograms/Parsers/GaussianImporter/GaussianLogReader.py#L107)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/Parsers/GaussianImporter/GaussianLogReader.py#L107?message=Update%20Docs)]
</div>
Tries to get the default keys one might be expected to want depending on the type of job as determined from the Header
Currently only supports 'opt', 'scan', and 'popt' as job types.
  - `:returns`: `tuple(str)`
    > k
e
y
 
l
i
s
t
i
n
g


<a id="McUtils.ExternalPrograms.Parsers.GaussianImporter.GaussianLogReader.read_props" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
read_props(cls, file, keys): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L136)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L136?message=Update%20Docs)]
</div>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianLogReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianLogReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianLogReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Parsers/GaussianImporter/GaussianLogReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ExternalPrograms/Parsers/GaussianImporter.py#L23?message=Update%20Docs)   
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
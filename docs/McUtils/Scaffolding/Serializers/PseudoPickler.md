## <a id="McUtils.McUtils.Scaffolding.Serializers.PseudoPickler">PseudoPickler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L23)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L23?message=Update%20Docs)]
</div>

A simple plugin to work _like_ pickle, in that it should
hopefully support serializing arbitrary python objects, but which
doesn't attempt to put stuff down to a single `bytearray`, instead
supporting objects with `to_state` and `from_state` methods by converting
them to more primitive serializble types like arrays, strings, numbers,
etc.
Falls back to naive pickling when necessary.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.McUtils.Scaffolding.Serializers.PseudoPickler.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, allow_pickle=False, protocol=1, b64encode=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/PseudoPickler.py#L35)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/PseudoPickler.py#L35?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Scaffolding.Serializers.PseudoPickler.to_state" class="docs-object-method">&nbsp;</a> 
```python
to_state(self, obj, cache=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/PseudoPickler.py#L130)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/PseudoPickler.py#L130?message=Update%20Docs)]
</div>
Tries to extract state from `obj`, first through its `to_state`
interface, but that failing by recursively walking the object
tree
  - `obj`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Scaffolding.Serializers.PseudoPickler.serialize" class="docs-object-method">&nbsp;</a> 
```python
serialize(self, obj, cache=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/PseudoPickler.py#L161)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/PseudoPickler.py#L161?message=Update%20Docs)]
</div>
Serializes an object first by checking for a `to_state`
method, and that missing, by converting to primitive-ish types
in a recursive strategy if the object passes `is_simple`, otherwise
falling back to `pickle`
  - `obj`: `Any`
    > object to be serialized
  - `:returns`: `dict`
    > s
p
e
c
 
f
o
r
 
t
h
e
 
p
s
e
u
d
o
-
p
i
c
k
l
e
d
 
d
a
t
a


<a id="McUtils.McUtils.Scaffolding.Serializers.PseudoPickler.deserialize" class="docs-object-method">&nbsp;</a> 
```python
deserialize(self, spec): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/PseudoPickler.py#L205)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/PseudoPickler.py#L205?message=Update%20Docs)]
</div>
Deserializes from an object spec, dispatching
to regular pickle where necessary
  - `object`: `Any`
    > 
  - `:returns`: `_`
    >
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Serializers/PseudoPickler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Serializers/PseudoPickler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Serializers/PseudoPickler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Serializers/PseudoPickler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L23?message=Update%20Docs)   
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
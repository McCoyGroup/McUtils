## <a id="McUtils.Plots.Plots.CompositePlot">CompositePlot</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots.py#L672)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots.py#L672?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Plots.Plots.CompositePlot.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, main, other, *rest, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots.py#L673)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots.py#L673?message=Update%20Docs)]
</div>
**LLM Docstring**

Hold several plots to be merged onto a shared figure.
  - `main`: `Any`
    > the first plot
  - `other`: `Any`
    > the second plot
  - `rest`: `Any`
    > additional plots
  - `kwargs`: `Any`
    > options applied when merging


<a id="McUtils.Plots.Plots.CompositePlot.merge" class="docs-object-method">&nbsp;</a> 
```python
merge(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots/CompositePlot.py#L686)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots/CompositePlot.py#L686?message=Update%20Docs)]
</div>
**LLM Docstring**

Merge the held plots onto a shared new figure (re-hosting each onto the first's
figure).
  - `kwargs`: `Any`
    > options for the shared figure
  - `:returns`: `Graphics`
    > the merged base plot


<a id="McUtils.Plots.Plots.CompositePlot.show" class="docs-object-method">&nbsp;</a> 
```python
show(self, interactive=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots/CompositePlot.py#L701)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots/CompositePlot.py#L701?message=Update%20Docs)]
</div>
**LLM Docstring**

Merge the plots and display the result.
  - `interactive`: `bool`
    > show interactively
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Plots/CompositePlot.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Plots/CompositePlot.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Plots/CompositePlot.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Plots/CompositePlot.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots.py#L672?message=Update%20Docs)   
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
### <a id="sobol_sequence">sobol_sequence</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/sobol_sequence.py#L)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/sobol_sequence.py#L?message=Update%20Docs)]
</div>
First N points of the d-dimensional Sobol sequence (Bratley-Fox
direction numbers), via the direct formula

x_n = XOR_{c : bit c of gray(n+1) is set} V[:, c]     (n = 0..N-1)

where gray(k) = k XOR (k >> 1). This 0-indexed convention matches the
classic Fortran/MATLAB/Python reference implementations (Burkardt et
al.) exactly -- validated against that reference in __main__ below.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/sobol_sequence.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/sobol_sequence.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/sobol_sequence.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/sobol_sequence.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/sobol_sequence.py#L?message=Update%20Docs)   
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


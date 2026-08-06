# <a id="McUtils.Iterators.Subsequences.find_overlaps">find_overlaps</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Iterators/Subsequences.py#L38)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/Subsequences.py#L38?message=Update%20Docs)]
</div>

```python
find_overlaps(s1: 'Sequence[Any]', s2: 'Sequence[Any]', *, equals: 'Callable[..., bool] | None' = None, contextual: 'bool' = False, require_contiguous=True) -> 'list[Overlap]': 
```
Find a longest common subsequence and divide it into contiguous runs.

In ordinary mode, ``equals`` has the signature::

    equals(s1_value, s2_value) -> bool

In contextual mode, it has the signature::

    equals(
        s1_value,
        s2_value,
        previous_s1_value,
        previous_s2_value,
    ) -> bool

The previous values are ``None`` when testing whether a pair can
begin a subsequence.

Contextual mode assumes equality depends only on the immediately
preceding matched pair, not the entire preceding subsequence.

Parameters
----------
s1, s2
    Input sequences.
equals
    Equality or compatibility function.
contextual
    If true, use the more expensive contextual LCS algorithm.

Returns
-------
list[list[tuple[int, int, Any]]]
    Contiguous runs forming one deterministic longest common
    subsequence.












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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Iterators/Subsequences/find_overlaps.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Iterators/Subsequences/find_overlaps.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Iterators/Subsequences/find_overlaps.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Iterators/Subsequences/find_overlaps.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/Subsequences.py#L38?message=Update%20Docs)   
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
# <a id="McUtils.Misc">McUtils.Misc</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Misc/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Misc/__init__.py#L1?message=Update%20Docs)]
</div>
    
Defines a set of miscellaneous helper utilities that are commonly used across projects.

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[SBatchJob](Misc/SBatchHelper/SBatchJob.md)   
</div>
   <div class="col" markdown="1">
[njit](Misc/NumbaTools/njit.md)   
</div>
   <div class="col" markdown="1">
[jit](Misc/NumbaTools/jit.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[type_spec](Misc/NumbaTools/type_spec.md)   
</div>
   <div class="col" markdown="1">
[without_numba](Misc/NumbaTools/without_numba.md)   
</div>
   <div class="col" markdown="1">
[numba_decorator](Misc/NumbaTools/numba_decorator.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[import_from_numba](Misc/NumbaTools/import_from_numba.md)   
</div>
   <div class="col" markdown="1">
[ModificationTracker](Misc/DebugTools/ModificationTracker.md)   
</div>
   <div class="col" markdown="1">
[mixedmethod](Misc/Decorators/mixedmethod.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Abstract](Misc/Symbolics/Abstract.md)   
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
## <a class="collapse-link" data-toggle="collapse" href="#Tests-c82b05" markdown="1"> Tests</a> <a class="float-right" data-toggle="collapse" href="#Tests-c82b05"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Tests-c82b05" markdown="1">
 - [Symbolics](#Symbolics)
- [TeXWriter](#TeXWriter)

<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
### <a class="collapse-link" data-toggle="collapse" href="#Setup-db08ab" markdown="1"> Setup</a> <a class="float-right" data-toggle="collapse" href="#Setup-db08ab"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Setup-db08ab" markdown="1">
 
Before we can run our examples we should get a bit of setup out of the way.
Since these examples were harvested from the unit tests not all pieces
will be necessary for all situations.

All tests are wrapped in a test class
```python
class MiscTests(TestCase):
```

 </div>
</div>

#### <a name="Symbolics">Symbolics</a>
```python
    def test_Symbolics(self):
        x, y, z, some = Abstract.vars('x', 'y', 'z', 'some')
        lexpr = Abstract.Lambda(x, *y, some=1, **z)(
            x*some
        )

        # print(ast.dump(lexpr.to_eval_expr()))

        lfun = lexpr.compile()

        self.assertEquals([1, 2, 3]*3, lfun([1, 2, 3], this=1, has=0, some=3, effect=4))

        x, np = Abstract.vars('x', 'np')
        npexpr = Abstract.Lambda(x)(
            np.array(x)[..., 0] + 1
        )

        # print(
        #     ast.dump(
        #         npexpr.to_eval_expr()
        #     )
        # )

        self.assertTrue(
            numpy.all(
                npexpr.compile({'np':numpy})([[1], [2], [3]])
                == numpy.array([[1], [2], [3]])[..., 0] + 1
            )
        )
```

#### <a name="TeXWriter">TeXWriter</a>
```python
    def test_TeXWriter(self):

        array = [[1, 2, 3], [4, 500000, 6]]
        arr_tex = TeX.wrap_parens(TeX.Array(array))
        print(
            arr_tex.format_tex()
        )

        o = TeX.Symbol('omega')
        i = TeX.Symbol('i')
        f = TeX.Symbol(TeX.bold('f'))

        sum = TeX.Symbol('sum')
        expr = sum[i:0:5] | o**2
        expr = f.Eq(arr_tex)

        print(
            TeX.Equation(expr, label='fmat').format_tex()
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Misc.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Misc.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Misc.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Misc.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Misc/__init__.py#L1?message=Update%20Docs)   
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
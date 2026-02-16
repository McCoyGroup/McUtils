# <a id="McUtils.Extensions">McUtils.Extensions</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Extensions/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/__init__.py#L1?message=Update%20Docs)]
</div>
    
A package for managing extension modules.
The existing `ExtensionLoader` will be moving here, and will be supplemented by classes for dealing with compiled extensions

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[CLoader](Extensions/CLoader/CLoader.md)   
</div>
   <div class="col" markdown="1">
[ModuleLoader](Extensions/ModuleLoader/ModuleLoader.md)   
</div>
   <div class="col" markdown="1">
[ArgumentType](Extensions/ArgumentSignature/ArgumentType.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ArrayType](Extensions/ArgumentSignature/ArrayType.md)   
</div>
   <div class="col" markdown="1">
[PointerType](Extensions/ArgumentSignature/PointerType.md)   
</div>
   <div class="col" markdown="1">
[PrimitiveType](Extensions/ArgumentSignature/PrimitiveType.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Argument](Extensions/ArgumentSignature/Argument.md)   
</div>
   <div class="col" markdown="1">
[FunctionSignature](Extensions/ArgumentSignature/FunctionSignature.md)   
</div>
   <div class="col" markdown="1">
[SharedLibrary](Extensions/SharedLibraryManager/SharedLibrary.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[SharedLibraryFunction](Extensions/SharedLibraryManager/SharedLibraryFunction.md)   
</div>
   <div class="col" markdown="1">
[FFIModule](Extensions/FFI/Module/FFIModule.md)   
</div>
   <div class="col" markdown="1">
[FFIMethod](Extensions/FFI/Module/FFIMethod.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[FFIArgument](Extensions/FFI/Module/FFIArgument.md)   
</div>
   <div class="col" markdown="1">
[FFIType](Extensions/FFI/Module/FFIType.md)   
</div>
   <div class="col" markdown="1">
[FFILoader](Extensions/FFI/Loader/FFILoader.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[DynamicFFIFunctionLoader](Extensions/FFI/DynamicFFILibrary/DynamicFFIFunctionLoader.md)   
</div>
   <div class="col" markdown="1">
[DynamicFFIFunction](Extensions/FFI/DynamicFFILibrary/DynamicFFIFunction.md)   
</div>
   <div class="col" markdown="1">
[DynamicFFILibrary](Extensions/FFI/DynamicFFILibrary/DynamicFFILibrary.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
   
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
## <a class="collapse-link" data-toggle="collapse" href="#Tests-c2a966" markdown="1"> Tests</a> <a class="float-right" data-toggle="collapse" href="#Tests-c2a966"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Tests-c2a966" markdown="1">
 - [BasicTypeSig](#BasicTypeSig)
- [SOSig](#SOSig)
- [SharedLibraryFunction](#SharedLibraryFunction)
- [SharedLibrary](#SharedLibrary)
- [FFI](#FFI)
- [FFI_threaded](#FFI_threaded)

<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
### <a class="collapse-link" data-toggle="collapse" href="#Setup-f7ea4b" markdown="1"> Setup</a> <a class="float-right" data-toggle="collapse" href="#Setup-f7ea4b"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Setup-f7ea4b" markdown="1">
 
Before we can run our examples we should get a bit of setup out of the way.
Since these examples were harvested from the unit tests not all pieces
will be necessary for all situations.

All tests are wrapped in a test class
```python
class ExtensionsTests(TestCase):
```

 </div>
</div>

#### <a name="BasicTypeSig">BasicTypeSig</a>
```python
    def test_BasicTypeSig(self):
        sig = FunctionSignature(
            "my_func",
            Argument("num_1", RealType),
            Argument("num_2", RealType, default=5),
            Argument("some_int", IntType)
        )
        self.assertEquals(sig.cpp_signature, "void my_func(double num_1, double num_2, int some_int)")
```

#### <a name="SOSig">SOSig</a>
```python
    def test_SOSig(self):
        lib_file = TestManager.test_data('libmbpol.so')
        mbpol = SharedLibraryFunction(lib_file,
                                      FunctionSignature(
                                          "calcpot_",
                                          Argument("nw", PointerType(IntType)),
                                          Argument("energy", PointerType(RealType)),
                                          Argument("coords", ArrayType(RealType))
                                      )
                                      )
        self.assertTrue("SharedLibraryFunction(FunctionSignature(calcpot_(Argument('nw', PointerType(PrimitiveType(int)))" in repr(mbpol))
```

#### <a name="SharedLibraryFunction">SharedLibraryFunction</a>
```python
    def test_SharedLibraryFunction(self):
        lib_file = TestManager.test_data('libmbpol.so')
        mbpol = SharedLibraryFunction(lib_file,
                                      FunctionSignature(
                                          "calcpot_",
                                          Argument("nwaters", PointerType(IntType)),
                                          Argument("energy", PointerType(RealType)),
                                          Argument("coords", ArrayType(RealType)),
                                          return_type=None,
                                          defaults={'energy':0}
                                      ),
                                      return_handler=lambda r,kw:SharedLibraryFunction.uncast(kw['energy']) / 627.5094740631
                                      )
        water = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0]
        ])

        # print(mbpol(nwaters=1, coords=water))
        self.assertGreater(mbpol(nwaters=1, coords=water), .005)

        water = np.array([  # some random structure Mathematica got from who knows where...
            [-0.063259, -0.25268,    0.2621],
            [ 0.74277,   0.26059,    0.17009],
            [-0.67951,  -0.0079118, -0.43219]
        ])

        # print(mbpol(nwaters=1, coords=water))
        self.assertGreater(mbpol(nwaters=1, coords=water), .0006)

        water = np.array([  # some structure from the MBX tests...
            [-0.0044590985, -0.0513425796,  0.0000158138],
            [ 0.9861302114, -0.0745730984,  0.0000054324],
            [-0.1597470923,  0.8967180895, -0.0000164932]
        ])

        # print(mbpol(nwaters=1, coords=water))
        self.assertGreater(mbpol(nwaters=1, coords=water), .001)
```

#### <a name="SharedLibrary">SharedLibrary</a>
```python
    def test_SharedLibrary(self):
        lib_file = TestManager.test_data('libmbpol.so')
        mbpol = SharedLibrary(
            lib_file,
            get_pot=dict(
                name='calcpot_',
                nwaters=(int,),
                energy=(float,),
                coords=[float],
                return_type=None,
                defaults={'energy': 0},
                return_handler=lambda r, kw: SharedLibraryFunction.uncast(kw['energy']) / 627.5094740631
            ),
            get_pot_grad = dict(
                name='calcpotg_',
                nwaters=(int,),
                energy=(float,),
                coords=[float],
                grad=[float],
                return_type=None,
                prep_args=lambda kw:[kw.__setitem__('grad', np.zeros(kw['nwaters']*9)), kw][1],
                defaults={'grad':None, 'energy': 0},
                return_handler=lambda r, kw: {
                    'grad':kw['grad'].reshape(-1, 3) / 627.5094740631,
                    'energy':SharedLibraryFunction.uncast(kw['energy']) / 627.5094740631
                }
            )
        )

        water = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0]
        ])

        # print(mbpol(nwaters=1, coords=water))
        self.assertGreater(mbpol.get_pot_grad(nwaters=1, coords=water)['energy'], .005)
        self.assertEquals(mbpol.get_pot_grad(nwaters=1, coords=water)['grad'].shape, (3, 3))

        water = np.array([  # some random structure Mathematica got from who knows where...
            [-0.063259, -0.25268,    0.2621],
            [ 0.74277,    0.26059,   0.17009],
            [-0.67951,  -0.0079118, -0.43219]
        ])

        # print(mbpol(nwaters=1, coords=water))
        self.assertGreater(mbpol.get_pot_grad(nwaters=1, coords=water)['energy'], .0006)
        self.assertEquals(mbpol.get_pot_grad(nwaters=1, coords=water)['grad'].shape, (3, 3))

        water = np.array([  # some structure from the MBX tests...
            [-0.0044590985, -0.0513425796, 0.0000158138],
            [0.9861302114, -0.0745730984, 0.0000054324],
            [-0.1597470923, 0.8967180895, -0.0000164932]
        ])

        # print(mbpol(nwaters=1, coords=water))
        self.assertGreater(mbpol.get_pot_grad(nwaters=1, coords=water)['energy'], .001)
        self.assertEquals(mbpol.get_pot_grad(nwaters=1, coords=water)['grad'].shape, (3, 3))
```

#### <a name="FFI">FFI</a>
```python
    def test_FFI(self):
        lib_dir = TestManager.test_data('LegacyMBPol')
        mbpol = FFIModule.from_lib(lib_dir, extra_link_args=['-mmacosx-version-min=12.0'])

        water = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 0]
        ])

        # print(mbpol.get_pot_grad(nwaters=1, coords=water))
        self.assertGreater(mbpol.get_pot_grad(nwaters=1, coords=water)['energy'], .005)

        water = np.array([  # some random structure Mathematica got from who knows where...
            [-0.063259, -0.25268,    0.2621],
            [ 0.74277,   0.26059,    0.17009],
            [-0.67951,  -0.0079118, -0.43219]
        ])

        # print(mbpol.get_pot_grad(nwaters=1, coords=water))
        self.assertGreater(mbpol.get_pot_grad(nwaters=1, coords=water)['energy'], .0006)

        water = np.array([  # some structure from the MBX tests...
            [-0.0044590985, -0.0513425796, 0.0000158138],
            [0.9861302114, -0.0745730984, 0.0000054324],
            [-0.1597470923, 0.8967180895, -0.0000164932]
        ])

        # print(mbpol.get_pot_grad(nwaters=1, coords=water))
        self.assertGreater(mbpol.get_pot_grad(nwaters=1, coords=water)['energy'], .001)
```

#### <a name="FFI_threaded">FFI_threaded</a>
```python
    def test_FFI_threaded(self): # More detailed testing in test_mbpol.py
        lib_dir = TestManager.test_data('LegacyMBPol')
        mbpol = FFIModule.from_lib(lib_dir,
                                   extra_link_args=['-mmacosx-version-min=12.0']
                                   # , threaded=True
                                   # , recompile=True
                                   )

        from Peeves.Timer import Timer
        waters = np.array([
                              [
                                  [0, 0, 0],
                                  [1, 0, 0],
                                  [0, 1, 0]
                              ],
                              [  # some random structure Mathematica got from who knows where...
                                  [-0.063259, -0.25268, 0.2621],
                                  [0.74277, 0.26059, 0.17009],
                                  [-0.67951, -0.0079118, -0.43219]
                              ],
                              [  # some structure from the MBX tests...
                                  [-0.0044590985, -0.0513425796, 0.0000158138],
                                  [0.9861302114, -0.0745730984, 0.0000054324],
                                  [-0.1597470923, 0.8967180895, -0.0000164932]
                              ]
                          ] * 2500
                          )

        with Timer(tag="Threaded"):
            res = mbpol.get_pot(nwaters=1, coords=waters, threading_var='coords')
            print(np.mean(res))
        # print("="*100)
        # print(waters[0])
        # print(mbpol.get_pot(nwaters=1, coords=waters[0]))
        with Timer(tag="Unthreaded"):
            res = np.array([mbpol.get_pot(nwaters=1, coords=w) for w in waters])
            print(np.mean(res))
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Extensions.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Extensions.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Extensions.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Extensions.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Extensions/__init__.py#L1?message=Update%20Docs)   
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
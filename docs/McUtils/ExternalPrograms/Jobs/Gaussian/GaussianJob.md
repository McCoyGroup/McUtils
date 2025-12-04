## <a id="McUtils.ExternalPrograms.Jobs.Gaussian.GaussianJob">GaussianJob</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Gaussian.py#L277)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Gaussian.py#L277?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
job_template: str
blocks: list
non_blank_line_terminated: set
```
<a id="McUtils.ExternalPrograms.Jobs.Gaussian.GaussianJob.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *strs, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Gaussian.py#L287)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Gaussian.py#L287?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Jobs.Gaussian.GaussianJob.get_extra_keys" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_extra_keys(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L296)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L296?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Jobs.Gaussian.GaussianJob.get_block_types" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_block_types(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L302)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L302?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Jobs.Gaussian.GaussianJob.load_template" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load_template(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L306)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L306?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.Jobs.Gaussian.GaussianJob.get_params" class="docs-object-method">&nbsp;</a> 
```python
get_params(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Gaussian/GaussianJob.py#L311)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Gaussian/GaussianJob.py#L311?message=Update%20Docs)]
</div>
 </div>
</div>




## Examples













<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#Tests-b5d4f2" markdown="1"> Tests</a> <a class="float-right" data-toggle="collapse" href="#Tests-b5d4f2"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Tests-b5d4f2" markdown="1">
 - [GaussianJobWriter](#GaussianJobWriter)
- [LinkedModeScan](#LinkedModeScan)

<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
### <a class="collapse-link" data-toggle="collapse" href="#Setup-ad0de0" markdown="1"> Setup</a> <a class="float-right" data-toggle="collapse" href="#Setup-ad0de0"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Setup-ad0de0" markdown="1">
 
Before we can run our examples we should get a bit of setup out of the way.
Since these examples were harvested from the unit tests not all pieces
will be necessary for all situations.

All tests are wrapped in a test class
```python
class GaussianJobTests(TestCase):
    def setUp(self):
        self.test_log_water = TestManager.test_data("water_OH_scan.log")
        self.test_log_freq = TestManager.test_data("water_freq.log")
        self.test_log_opt = TestManager.test_data("water_dimer_test.log")
        self.test_fchk = TestManager.test_data("water_freq.fchk")
        self.test_log_h2 = TestManager.test_data("outer_H2_scan_new.log")
        self.test_scan = TestManager.test_data("water_OH_scan.log")
        self.test_rel_scan = TestManager.test_data("tbhp_030.log")
```

 </div>
</div>

#### <a name="GaussianJobWriter">GaussianJobWriter</a>
```python
    def test_GaussianJobWriter(self):
        job = GaussianJob(
            "water scan",
            description="Simple water scan",
            config= GaussianJob.Config(
                NProc = 4,
                Mem = '1000MB'
            ),
            job= GaussianJob.Job(
                'Scan'
            ),
            system = GaussianJob.System(
                charge=0,
                molecule=[
                    ["O", "H", "H"],
                    [
                        [0, 0, 0],
                        [.987, 0, 0],
                        [0, .987, 0]
                    ]
                ],
                vars=[
                    GaussianJob.System.Variable("y1", 0., 10., .1),
                    GaussianJob.System.Constant("x1", 10)
                ]
            ),

            footer="""
                C,O,H, 0
                6-31G(d,p)

                Rh 0
                lanl2dz
                """
        )
        # print(job.format())
        self.assertIsInstance(job.format(), str)
```

#### <a name="LinkedModeScan">LinkedModeScan</a>
```python
    def test_LinkedModeScan(self):
        """
        Set up a Linked array of Gaussian jobs
        """
        import itertools as ip

        struct = np.array([
            [0,    0,    0],
            [.987, 0,    0],
            [0,    .987, 0]
        ])
        oh_modes = np.array([
            [
                [0, 0, 0],
                [1, 0, 0],
                [0, 0, 0]
            ],
            [
                [0, 0, 0],
                [0, 0, 0],
                [0, 1, 0]
            ],
        ])
        displacements = ip.product(
            [-.05, 0, .05],
            [-.05, 0, .05]
        )

        job = GaussianJobArray(
            GaussianJob(
                "normal mode scan",
                description="Simple normal mode scan",
                config=GaussianJob.Config(
                    NProc=4,
                    Mem='1000MB',
                    Chk="displacement_{}.chk".format(i)
                ),
                job=GaussianJob.Job(
                    'SinglePoint'
                ),
                system=GaussianJob.System(
                    charge=0,
                    molecule=[
                        ["O", "H", "H"],
                        struct + np.tensordot(d, oh_modes, axes=[0, 0])
                    ]
                ),
                footer="""
                        C,O,H, 0
                        6-31G(d,p)
                        
                        Rh 0
                        lanl2dz
                        """
            )
            for i, d in enumerate(displacements)
        )
        job_str = job.format()
        self.assertIsInstance(job_str, str)
        self.assertIn("--Link1--", job_str)
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Jobs/Gaussian/GaussianJob.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Jobs/Gaussian/GaussianJob.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Jobs/Gaussian/GaussianJob.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Jobs/Gaussian/GaussianJob.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Gaussian.py#L277?message=Update%20Docs)   
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
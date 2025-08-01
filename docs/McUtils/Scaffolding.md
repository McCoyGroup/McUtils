# <a id="McUtils.Scaffolding">McUtils.Scaffolding</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/__init__.py#L1?message=Update%20Docs)]
</div>
    
Provides development utilities.
Each utility attempts to be almost entirely standalone (although there is
a small amount of cross-talk within the packages).
In order of usefulness, the design is:
1. `Logging` provides a flexible logging interface where the log data can be
reparsed and loggers can be passed around
2. `Serializers`/`Checkpointing` provides interfaces for writing/loading data
to file and allows for easy checkpoint loading
3. `Jobs` provides simpler interfaces for running jobs using the existing utilities
4. `CLIs` provides simple command line interface helpers

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[Cache](Scaffolding/Caches/Cache.md)   
</div>
   <div class="col" markdown="1">
[MaxSizeCache](Scaffolding/Caches/MaxSizeCache.md)   
</div>
   <div class="col" markdown="1">
[ObjectRegistry](Scaffolding/Caches/ObjectRegistry.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[PseudoPickler](Scaffolding/Serializers/PseudoPickler.md)   
</div>
   <div class="col" markdown="1">
[BaseSerializer](Scaffolding/Serializers/BaseSerializer.md)   
</div>
   <div class="col" markdown="1">
[JSONSerializer](Scaffolding/Serializers/JSONSerializer.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[NumPySerializer](Scaffolding/Serializers/NumPySerializer.md)   
</div>
   <div class="col" markdown="1">
[NDarrayMarshaller](Scaffolding/Serializers/NDarrayMarshaller.md)   
</div>
   <div class="col" markdown="1">
[HDF5Serializer](Scaffolding/Serializers/HDF5Serializer.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[YAMLSerializer](Scaffolding/Serializers/YAMLSerializer.md)   
</div>
   <div class="col" markdown="1">
[ModuleSerializer](Scaffolding/Serializers/ModuleSerializer.md)   
</div>
   <div class="col" markdown="1">
[LogParser](Scaffolding/Logging/LogParser.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Checkpointer](Scaffolding/Checkpointing/Checkpointer.md)   
</div>
   <div class="col" markdown="1">
[CheckpointerKeyError](Scaffolding/Checkpointing/CheckpointerKeyError.md)   
</div>
   <div class="col" markdown="1">
[DumpCheckpointer](Scaffolding/Checkpointing/DumpCheckpointer.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[JSONCheckpointer](Scaffolding/Checkpointing/JSONCheckpointer.md)   
</div>
   <div class="col" markdown="1">
[NumPyCheckpointer](Scaffolding/Checkpointing/NumPyCheckpointer.md)   
</div>
   <div class="col" markdown="1">
[HDF5Checkpointer](Scaffolding/Checkpointing/HDF5Checkpointer.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[DictCheckpointer](Scaffolding/Checkpointing/DictCheckpointer.md)   
</div>
   <div class="col" markdown="1">
[NullCheckpointer](Scaffolding/Checkpointing/NullCheckpointer.md)   
</div>
   <div class="col" markdown="1">
[PersistenceLocation](Scaffolding/Persistence/PersistenceLocation.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[PersistenceManager](Scaffolding/Persistence/PersistenceManager.md)   
</div>
   <div class="col" markdown="1">
[ResourceManager](Scaffolding/Persistence/ResourceManager.md)   
</div>
   <div class="col" markdown="1">
[BaseObjectManager](Scaffolding/ObjectBackers/BaseObjectManager.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[FileBackedObjectManager](Scaffolding/ObjectBackers/FileBackedObjectManager.md)   
</div>
   <div class="col" markdown="1">
[Config](Scaffolding/Configurations/Config.md)   
</div>
   <div class="col" markdown="1">
[ParameterManager](Scaffolding/Configurations/ParameterManager.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Job](Scaffolding/Jobs/Job.md)   
</div>
   <div class="col" markdown="1">
[JobManager](Scaffolding/Jobs/JobManager.md)   
</div>
   <div class="col" markdown="1">
[CLI](Scaffolding/CLIs/CLI.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[CommandGroup](Scaffolding/CLIs/CommandGroup.md)   
</div>
   <div class="col" markdown="1">
[Command](Scaffolding/CLIs/Command.md)   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>





## Examples













<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#Tests-50b306" markdown="1"> Tests</a> <a class="float-right" data-toggle="collapse" href="#Tests-50b306"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Tests-50b306" markdown="1">
 - [Schema](#Schema)
- [Pseudopickle](#Pseudopickle)
- [HDF5Serialization](#HDF5Serialization)
- [JSONSerialization](#JSONSerialization)
- [JSONPseudoPickleSerialization](#JSONPseudoPickleSerialization)
- [HDF5PseudoPickleSerialization](#HDF5PseudoPickleSerialization)
- [NumPySerialization](#NumPySerialization)
- [JSONCheckpointing](#JSONCheckpointing)
- [JSONCheckpointingKeyed](#JSONCheckpointingKeyed)
- [JSONCheckpointingCanonicalKeyed](#JSONCheckpointingCanonicalKeyed)
- [NumPyCheckpointing](#NumPyCheckpointing)
- [HDF5Checkpointing](#HDF5Checkpointing)
- [HDF5CheckpointingPsuedopickle](#HDF5CheckpointingPsuedopickle)
- [HDF5Problems](#HDF5Problems)
- [BasicLogging](#BasicLogging)
- [InformedLogging](#InformedLogging)
- [Persistence](#Persistence)
- [Jobbing](#Jobbing)
- [CLI](#CLI)
- [JobInit](#JobInit)
- [CurrentJob](#CurrentJob)
- [CurrentJobDiffFile](#CurrentJobDiffFile)

<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
### <a class="collapse-link" data-toggle="collapse" href="#Setup-6dde10" markdown="1"> Setup</a> <a class="float-right" data-toggle="collapse" href="#Setup-6dde10"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Setup-6dde10" markdown="1">
 
Before we can run our examples we should get a bit of setup out of the way.
Since these examples were harvested from the unit tests not all pieces
will be necessary for all situations.

All tests are wrapped in a test class
```python
class ScaffoldingTests(TestCase):
    class DataHolderClass:
        def __init__(self, **keys):
            self.data = keys
        def to_state(self, serializer=None):
            return self.data
        @classmethod
        def from_state(cls, state, serializer=None):
            return cls(**state)
```

 </div>
</div>

#### <a name="Schema">Schema</a>
```python
    def test_Schema(self):
        data = {
            'file': 'test.txt',
            'filesystem': {
                'os':'macOS'
            }
        }

        # schema = dev.Schema(['file'], ['filesystem'])
        # self.assertTrue(schema.validate(data))
        # #
        # schema = dev.Schema(['file', 'filesystem'])
        # self.assertFalse(schema.validate(data, throw=False))
        #
        # schema = dev.Schema({'file':'number'}, ['filesystem'])
        # self.assertFalse(schema.validate(data, throw=False))
        #
        schema = dev.Schema(
            {'file':'str'},
            {'filesystem':str}
        )
        self.assertFalse(schema.validate(data, throw=False))

        schema = dev.Schema(
            {'file': 'str'},
            {
                'filesystem': {
                    'os': {
                        'type': 'str',
                        'enum': ['macOS', 'linux', 'windows']
                    }
                }
            }
        )
        self.assertTrue(schema.validate(data))


        data = {
            'file': 'test.txt',
            'filesystem': {
                'os':'OSX'
            }
        }
        self.assertFalse(schema.validate(data, throw=False))
```

#### <a name="Pseudopickle">Pseudopickle</a>
```python
    def test_Pseudopickle(self):

        from McUtils.Numputils import SparseArray

        pickler = PseudoPickler()
        spa = SparseArray.from_diag([1, 2, 3, 4])
        serial = pickler.serialize(spa)
        deserial = pickler.deserialize(serial)
        self.assertTrue(np.allclose(spa.asarray(), deserial.asarray()))
```

#### <a name="HDF5Serialization">HDF5Serialization</a>
```python
    def test_HDF5Serialization(self):
        tmp = io.BytesIO()
        serializer = HDF5Serializer()

        data = [1, 2, 3]
        serializer.serialize(tmp, data)
        loaded = serializer.deserialize(tmp)
        self.assertEquals(loaded.tolist(), data)

        serializer.serialize(tmp, {
            "blebby": {
                "frebby": {
                    "clebby":data
                }
            }
        })
        loaded = serializer.deserialize(tmp, key='blebby')
        self.assertEquals(loaded['frebby']['clebby'].tolist(), data)

        mixed_data = [
            [1, 2, 3],
            "garbage",
            {"temps":[1., 2., 3.]}
            ]
        serializer.serialize(tmp, dict(mixed_data=mixed_data))

        loaded = serializer.deserialize(tmp, key='mixed_data')
        self.assertEquals(mixed_data, [
            loaded[0].tolist(),
            loaded[1].tolist().decode('utf-8'),
            {k:v.tolist() for k,v in loaded[2].items()}
        ])
```

#### <a name="JSONSerialization">JSONSerialization</a>
```python
    def test_JSONSerialization(self):
        tmp = io.StringIO()
        serializer = JSONSerializer()

        data = [1, 2, 3]
        serializer.serialize(tmp, data)
        tmp.seek(0)
        loaded = serializer.deserialize(tmp)
        self.assertEquals(loaded, data)

        tmp = io.StringIO()
        serializer.serialize(tmp, {
            "blebby": {
                "frebby": {
                    "clebby":data
                }
            }
        })
        tmp.seek(0)
        loaded = serializer.deserialize(tmp, key='blebby')
        self.assertEquals(loaded['frebby']['clebby'], data)

        tmp = io.StringIO()
        mixed_data = [
            [1, 2, 3],
            "garbage",
            {"temps":[1., 2., 3.]}
            ]
        serializer.serialize(tmp, dict(mixed_data=mixed_data))
        tmp.seek(0)
        loaded = serializer.deserialize(tmp, key='mixed_data')
        self.assertEquals(mixed_data, loaded)
```

#### <a name="JSONPseudoPickleSerialization">JSONPseudoPickleSerialization</a>
```python
    def test_JSONPseudoPickleSerialization(self):

        from McUtils.Numputils import SparseArray

        tmp = io.StringIO()
        serializer = JSONSerializer()

        data = SparseArray.from_diag([1, 2, 3, 4])

        serializer.serialize(tmp, data)
        tmp.seek(0)
        loaded = serializer.deserialize(tmp)

        self.assertTrue(np.allclose(loaded.asarray(), data.asarray()))
```

#### <a name="HDF5PseudoPickleSerialization">HDF5PseudoPickleSerialization</a>
```python
    def test_HDF5PseudoPickleSerialization(self):

        from McUtils.Numputils import SparseArray

        tmp = io.BytesIO()
        serializer = HDF5Serializer()

        data = SparseArray.from_diag([1, 2, 3, 4])

        serializer.serialize(tmp, data)
        tmp.seek(0)
        loaded = serializer.deserialize(tmp)

        self.assertTrue(np.allclose(loaded.asarray(), data.asarray()))
```

#### <a name="NumPySerialization">NumPySerialization</a>
```python
    def test_NumPySerialization(self):
        tmp = io.BytesIO()
        serializer = NumPySerializer()

        data = [1, 2, 3]
        serializer.serialize(tmp, data)
        tmp.seek(0)
        loaded = serializer.deserialize(tmp)
        self.assertEquals(loaded.tolist(), data)

        tmp = io.BytesIO()
        serializer.serialize(tmp, {
            "blebby": {
                "frebby": {
                    "clebby": data
                }
            }
        })
        tmp.seek(0)
        loaded = serializer.deserialize(tmp, key='blebby')
        self.assertEquals(loaded['frebby']['clebby'].tolist(), data)

        tmp = io.BytesIO()
        mixed_data = [
            [1, 2, 3],
            "garbage",
            {"temps": [1., 2., 3.]}
        ]
        serializer.serialize(tmp, dict(mixed_data=mixed_data))
        tmp.seek(0)
        loaded = serializer.deserialize(tmp, key='mixed_data')
        self.assertEquals(mixed_data, [
            loaded[0].tolist(),
            loaded[1].tolist(),
            {k: v.tolist() for k, v in loaded[2].items()}
        ])
```

#### <a name="JSONCheckpointing">JSONCheckpointing</a>
```python
    def test_JSONCheckpointing(self):
        with tmpf.NamedTemporaryFile() as chk_file:
            my_file = chk_file.name
        try:
            with JSONCheckpointer(my_file) as chk:
                # do something
                data = [1, 2, 3]
                chk['step_1'] = data
                # do something else
                chk['step_2_params'] = {
                    'steps': 500,
                    'step_size': .1,
                    'method': 'implicit euler'
                }

                # blobby
                data_2 = np.random.rand(100)
                chk['step_2'] = data_2

            # do some other stuff, maybe need to reload from checkpoint?
            with JSONCheckpointer(my_file) as chk:
                self.assertEquals(len(chk['step_2']), 100)
        finally:
            os.remove(my_file)
```

#### <a name="JSONCheckpointingKeyed">JSONCheckpointingKeyed</a>
```python
    def test_JSONCheckpointingKeyed(self):
        with tmpf.NamedTemporaryFile() as chk_file:
            my_file = chk_file.name
        try:
            with JSONCheckpointer(my_file, allowed_keys=['step_1', 'step_2']) as chk:
                # do something
                data = [1, 2, 3]
                chk['step_1'] = data
                # do something else
                try:
                    chk['step_2_params'] = {
                        'steps': 500,
                        'step_size': .1,
                        'method': 'implicit euler'
                    }
                except KeyError:
                    # blobby
                    data_2 = np.random.rand(100)
                    chk['step_2'] = data_2


            # do some other stuff, maybe need to reload from checkpoint?
            with JSONCheckpointer(my_file) as chk:
                self.assertEquals(len(chk['step_2']), 100)
        finally:
            os.remove(my_file)
```

#### <a name="JSONCheckpointingCanonicalKeyed">JSONCheckpointingCanonicalKeyed</a>
```python
    def test_JSONCheckpointingCanonicalKeyed(self):
        with tmpf.NamedTemporaryFile() as chk_file:
            my_file = chk_file.name + ".json"
        try:
            with Checkpointer.build_canonical({'file':my_file, 'keys':['step_1', 'step_2']}) as chk:
                # do something
                data = [1, 2, 3]
                chk['step_1'] = data
                # do something else
                try:
                    chk['step_2_params'] = {
                        'steps': 500,
                        'step_size': .1,
                        'method': 'implicit euler'
                    }
                except KeyError:
                    # blobby
                    data_2 = np.random.rand(100)
                    chk['step_2'] = data_2

            # do some other stuff, maybe need to reload from checkpoint?
            with JSONCheckpointer(my_file) as chk:
                self.assertEquals(len(chk['step_2']), 100)
                try:
                    self.assertEquals(len(chk['step_2_params']), 100)
                except KeyError as e:
                    pass
                else:
                    self.assertFalse(True, msg="key shouldn't be there")

        finally:
            os.remove(my_file)
```

#### <a name="NumPyCheckpointing">NumPyCheckpointing</a>
```python
    def test_NumPyCheckpointing(self):

        with tmpf.NamedTemporaryFile() as chk_file:
            my_file = chk_file.name

        try:
            with NumPyCheckpointer(my_file) as chk:
                # do something
                data = [1, 2, 3]
                chk['step_1'] = data
                # do something else
                chk['step_2_params'] = {
                    'steps': 500,
                    'step_size': .1,
                    'method': 'implicit euler'
                }

                # blobby
                data_2 = np.random.rand(100)
                chk['step_2'] = data_2

            # do some other stuff, maybe need to reload from checkpoint?
            with NumPyCheckpointer(my_file) as chk:
                self.assertEquals(len(chk['step_2']), 100)
        finally:
            os.remove(my_file)
```

#### <a name="HDF5Checkpointing">HDF5Checkpointing</a>
```python
    def test_HDF5Checkpointing(self):

        with tmpf.NamedTemporaryFile(mode="w+b") as chk_file:
            my_file = chk_file.name
        try:
            with HDF5Checkpointer(my_file) as chk:
                # do something
                data = [1, 2, 3]
                chk['step_1'] = data
                # do something else
                chk['step_2_params'] = {
                    'steps': 500,
                    'step_size': .1,
                    'method': 'implicit euler'
                }

                # blobby
                data_2 = np.random.rand(100)
                chk['step_2'] = data_2

            # do some other stuff, maybe need to reload from checkpoint?
            with HDF5Checkpointer(my_file) as chk:
                self.assertEquals(len(chk['step_2']), 100)
        finally:
            os.remove(my_file)
```

#### <a name="HDF5CheckpointingPsuedopickle">HDF5CheckpointingPsuedopickle</a>
```python
    def test_HDF5CheckpointingPsuedopickle(self):

        with tmpf.NamedTemporaryFile(mode="w+b") as chk_file:
            my_file = chk_file.name
        try:
            with HDF5Checkpointer(my_file) as chk:
                # do something
                data = [1, 2, 3]
                chk['step_1'] = data
                # do something else
                keys = {
                    'steps': 500,
                    'step_size': .1,
                    'method': 'implicit euler'
                }
                woop = self.DataHolderClass(**keys)
                chk['step_2_params'] = woop

                # blobby
                data_2 = np.random.rand(100)
                chk['step_2'] = data_2

            # do some other stuff, maybe need to reload from checkpoint?
            with HDF5Checkpointer(my_file) as chk:
                self.assertEquals(len(chk['step_2']), 100)
                self.assertEquals(chk['step_2_params'].data, keys)
        finally:
            os.remove(my_file)
```

#### <a name="HDF5Problems">HDF5Problems</a>
```python
    def test_HDF5Problems(self):

        test = os.path.expanduser('~/Desktop/woof.hdf5')
        os.remove(test)
        checkpointer = Checkpointer.from_file(test)
        with checkpointer:
            checkpointer['why'] = [
                np.random.rand(1000, 5, 5),
                np.array(0),
                np.array(0)
            ]
        with checkpointer:
            checkpointer['why'] = [
                np.random.rand(1001, 5, 5),
                np.array(0),
                np.array(0)
            ]
        with checkpointer:
            checkpointer['why2'] = [
                np.random.rand(1001, 5, 5),
                np.array(0),
                np.array(0)
            ]

        with checkpointer as chk:
            self.assertEquals(list(chk.keys()), ['why', 'why2'])
```

#### <a name="BasicLogging">BasicLogging</a>
```python
    def test_BasicLogging(self):
        stdout = io.StringIO()
        logger = Logger(stdout)
        with logger.block(tag='Womp Womp'):
            logger.log_print('wompy dompy domp')

            logger.log_print('Some other useful info?')
            with logger.block(tag="Calling into subprogram"):
                logger.log_print('actually this is fake -_-')
                logger.log_print('took {timing:.5f}s', timing=121.01234)

            logger.log_print('I guess following up on that?')
            with logger.block(tag="Calling into subprogram"):
                logger.log_print('this is also fake! :yay:')
                logger.log_print('took {timing:.5f}s', timing=212.01234)

            logger.log_print('done for now; took {timing:.5f}s', timing=-1)

        with logger.block(tag='Surprise second block!'):
            logger.log_print('just kidding')
            with logger.block(tag="JK on that JK"):
                with logger.block(tag="Doubly nested block!"):
                    logger.log_print('woopy doopy doo bitchez')
                logger.log_print('(all views are entirely my own and do not reflect on my employer in any way)')

            logger.log_print('okay done for real; took {timing:.0f} years', timing=10000)

        with tmpf.NamedTemporaryFile(mode="w+b") as temp:
            log_dump = temp.name
        try:
            with open(log_dump, "w+") as dump:
                dump.write(stdout.getvalue())
            with LogParser(log_dump) as parser:
                blocks = list(parser.get_blocks())
                self.assertEquals(blocks[1].lines[1].lines[1], " (all views are entirely my own and do not reflect on my employer in any way)")
                self.assertEquals(blocks[1].lines[1].lines[0].tag, "Doubly nested block!")
        finally:
            os.remove(log_dump)
```

#### <a name="InformedLogging">InformedLogging</a>
```python
    def test_InformedLogging(self):
        import random

        with tmpf.NamedTemporaryFile(mode="w+b") as temp:
            log_dump = temp.name
        try:
            logger = Logger(log_dump)
            for i in range(100):
                with logger.block(tag="Step {}".format(i)):
                    logger.log_print("Did X")
                    logger.log_print("Did Y")
                    with logger.block(tag="Fake Call".format(i)):
                        logger.log_print("Took {timing:.5f}s", timing=random.random())

            number_puller = parsers.StringParser(parsers.Capturing(parsers.Number))
            with LogParser(log_dump) as parser:
                time_str = ""
                for block in parser.get_blocks(tag="Fake Call", level=1):
                    time_str += block.lines[0]
                timings = number_puller.parse_all(time_str).array
                self.assertEquals(len(timings), 100)
                self.assertGreater(np.average(timings), .35)
                self.assertLess(np.average(timings), .65)

            with LogParser(log_dump) as parser:
                time_str = ""
                for line in parser.get_lines(tag="Took ", level=1):
                    time_str += line
                timings = number_puller.parse_all(time_str).array
                self.assertEquals(len(timings), 100)
                self.assertGreater(np.average(timings), .35)
                self.assertLess(np.average(timings), .65)

        finally:
            os.remove(log_dump)
```

#### <a name="Persistence">Persistence</a>
```python
    def test_Persistence(self):
        persist_dir = TestManager.test_data("persistence_tests")

        class PersistentMock:
            """
            A fake object that supports the persistence interface we defined
            """

            def __init__(self, name, sample_val):
                self.name = name
                self.val = sample_val
            @classmethod
            def from_config(cls, name="wat", sample_val=None):
                return cls(name, sample_val)

        manager = PersistenceManager(PersistentMock, persist_dir)

        obj = manager.load("obj1", strict=False)

        self.assertEquals(obj.val, 'test_val')
```

#### <a name="Jobbing">Jobbing</a>
```python
    def test_Jobbing(self):

        import time

        with tmpf.TemporaryDirectory() as temp_dir:

            manager = JobManager(temp_dir)
            with manager.job("test") as job:
                logger = job.logger
                with logger.block(tag="Sleeping"):
                    logger.log_print("Goodnight!")
                    time.sleep(.2)
                    logger.log_print("Okee I'm back up")

            self.assertEquals(os.path.basename(job.dir), "test")
            self.assertEquals(set(job.checkpoint.backend.keys()), {'start', 'runtime'})
            with open(job.logger.log_file) as doopy:
                doop_str = doopy.read()
                self.assertNotEqual("", doop_str)
```

#### <a name="CLI">CLI</a>
```python
    def test_CLI(self):
        import McUtils.Plots as plt
        class PlottingInterface(CommandGroup):
            _tag = "plot"
            @classmethod
            def random(cls, npts:int = 100, file:str = None):
                """Makes a random plot of however many points you want"""
                xy = np.random.rand(npts, npts)
                ploot = plt.ArrayPlot(xy)
                if file is None:
                    ploot.show()
                else:
                    ploot.savefig(file)
            @classmethod
            def contour(cls, npts: int = 100, file: str = None):
                """Makes a random contour plot of however many points you want"""
                xy = np.random.rand(npts, npts)
                ploot = plt.ListContourPlot(xy)
                if file is None:
                    ploot.show()
                else:
                    ploot.savefig(file)

        import McUtils.Data as data
        class DataInterface(CommandGroup):
            _tag = "data"
            @classmethod
            def mass(cls, elem:str):
                """Gets the mass for the passed element spec"""
                print(data.AtomData[elem]['Mass'])

        mccli = CLI(
            "McUtils",
            "defines a simple CLI interface to various bits of McUtils",
            PlottingInterface,
            DataInterface,
            cmd_name='mcutils'
        )
        print()

        with tmpf.NamedTemporaryFile() as out:
            argv = sys.argv
            try:
                sys.argv = ['mccli', '--help']
                mccli.run()

                sys.argv = ['mccli', 'plot', 'contour', '--npts=100']
                mccli.run()

                sys.argv = ['mccli', 'data', 'mass', 'T']
                mccli.run()
            finally:
                sys.argv = argv
```

#### <a name="JobInit">JobInit</a>
```python
    def test_JobInit(self):

        import time

        with tmpf.TemporaryDirectory() as temp_dir:
            manager = JobManager(temp_dir)
            with manager.job(TestManager.test_data("persistence_tests/test_job")) as job:
                logger = job.logger

                with logger.block(tag="Sleeping"):
                    logger.log_print("Goodnight!")
                    time.sleep(.2)
                    logger.log_print("Okee I'm back up")

            self.assertEquals(os.path.basename(job.dir), "test_job")
            self.assertEquals(set(Config(job.dir).opt_dict.keys()), {'logger', 'parallelizer', 'config_location'})
            self.assertEquals(set(job.checkpoint.backend.keys()), {'start', 'runtime'})
            with open(job.logger.log_file) as doopy:
                doop_str = doopy.read()
                self.assertNotEqual("", doop_str)
```

#### <a name="CurrentJob">CurrentJob</a>
```python
    def test_CurrentJob(self):

        import time

        with tmpf.TemporaryDirectory() as temp_dir:
            jobby = JobManager.job_from_folder(temp_dir)
            with jobby as job:
                logger = job.logger

                with logger.block(tag="Sleeping"):
                    logger.log_print("Goodnight!")
                    time.sleep(.2)
                    logger.log_print("Okee I'm back up")

            with open(job.logger.log_file) as doopy:
                doop_str = doopy.read()
                self.assertNotEqual("", doop_str)
```

#### <a name="CurrentJobDiffFile">CurrentJobDiffFile</a>
```python
    def test_CurrentJobDiffFile(self):

        import time

        curdir = os.getcwd()
        try:
            with tmpf.TemporaryDirectory() as temp_dir:
                os.chdir(temp_dir)
                with JobManager.current_job(job_file='woof.json') as job:
                    self.assertEquals(os.path.basename(job.checkpoint.checkpoint_file), 'woof.json')
                    logger = job.logger

                    with logger.block(tag="Sleeping"):
                        logger.log_print("Goodnight!")
                        time.sleep(.2)
                        logger.log_print("Okee I'm back up")

                with open(job.logger.log_file) as doopy:
                    doop_str = doopy.read()
                    self.assertNotEqual("", doop_str)
        finally:
            os.chdir(curdir)
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/__init__.py#L1?message=Update%20Docs)   
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
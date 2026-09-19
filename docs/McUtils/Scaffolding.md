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
[flatten_tree](Scaffolding/Serializers/flatten_tree.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[unflatten_tree](Scaffolding/Serializers/unflatten_tree.md)   
</div>
   <div class="col" markdown="1">
[write_flat_tree](Scaffolding/Serializers/write_flat_tree.md)   
</div>
   <div class="col" markdown="1">
[read_flat_tree](Scaffolding/Serializers/read_flat_tree.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[NumpyTreeArchive](Scaffolding/Serializers/NumpyTreeArchive.md)   
</div>
   <div class="col" markdown="1">
[LineIndexedSupplier](Scaffolding/Serializers/LineIndexedSupplier.md)   
</div>
   <div class="col" markdown="1">
[SerializedObjectSupplier](Scaffolding/Serializers/SerializedObjectSupplier.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[JSONLSupplier](Scaffolding/Serializers/JSONLSupplier.md)   
</div>
   <div class="col" markdown="1">
[NPZLSupplier](Scaffolding/Serializers/NPZLSupplier.md)   
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

**LLM Examples**

### Serialize and restore a sparse scientific object

```python
import numpy as np
from McUtils.Numputils import SparseArray
from McUtils.Scaffolding import PseudoPickler

matrix = SparseArray.from_diag([.4, .8, 1.2, 1.6])
serializer = PseudoPickler()
payload = serializer.serialize(matrix)
restored = serializer.deserialize(payload)
assert np.allclose(restored.asarray(), matrix.asarray())
print("protocol:", payload["pseudopickle_protocol"])
```

### Checkpoint an iterative calculation

```python
import numpy as np
from McUtils.Scaffolding import JSONCheckpointer

with JSONCheckpointer("optimization.json") as checkpoint:
    checkpoint["iteration"] = 12
    checkpoint["energy"] = -76.2413
    checkpoint["gradient_norm"] = float(np.linalg.norm([.001, -.002, .0005]))

with JSONCheckpointer("optimization.json") as checkpoint:
    print("restart at iteration", checkpoint["iteration"] + 1)
```

### Use structured logging blocks

```python
from McUtils.Scaffolding import Logger

logger = Logger(log_file="calculation.log")
logger.log_print("Starting {method}/{basis}", method="CCSD(T)", basis="cc-pVTZ")
with logger.block(tag="Optimization step {step}", step=1):
    logger.log_print("Energy: {energy:.8f}", energy=-76.2413123)
    logger.log_print("Gradient norm: {norm:.3e}", norm=2.3e-4)
logger.log_print("Calculation complete")
```

### Cache an expensive calculation

```python
from McUtils.Scaffolding import MaxSizeCache

cache = MaxSizeCache(max_items=3)
for key, value in [("HF", -75.98), ("MP2", -76.23),
                   ("CCSD", -76.24), ("CCSD(T)", -76.25)]:
    cache[key] = value
print("retained keys:", list(cache.keys()))
```

### Persist a nested tree in HDF5

```python
import numpy as np
from McUtils.Scaffolding import HDF5Serializer

data = {"atoms": ["O", "H", "H"],
        "coordinates": np.array([[0, 0, 0], [.958, 0, 0], [-.240, .927, 0]])}
serializer = HDF5Serializer()
serializer.serialize("structure.hdf5", data)
restored = serializer.deserialize("structure.hdf5")
assert np.allclose(restored["coordinates"], data["coordinates"])
```

### Load a file-backed configuration

```python
from McUtils.Scaffolding import Config

config = Config.new("calculation", init={"method": "CCSD(T)", "basis": "cc-pVTZ"})
config.update(memory="16GB", cores=8)
options = config.opt_dict
print(config.name, options)
```

### Store Conformer Libraries

```
import numpy as np
from McUtils.ExternalPrograms import RDMolecule
from McUtils.Scaffolding import HDF5Checkpointer

mol = RDMolecule.from_smiles(
    "O=C(O)C(O)C", add_implicit_hydrogens=True,
    num_confs=50, optimize=True, take_min=True
)
# In a conformer-search workflow, `conformers` can instead come from CREST,
# an RDKit conformer-id loop, or a trajectory. Here we make a small local
# ensemble around the optimized minimum so the storage pattern is explicit.
rng = np.random.default_rng(8)
conformers = mol.coords + rng.normal(0, 0.03, size=(40,) + mol.coords.shape)
energies = np.asarray(mol.calculate_energy(conformers))
order = np.argsort(energies)[:10]
tags = [mol.conformer_smiles_tag(coords=conformers[i], include_zmatrix=True)
        for i in order]

with HDF5Checkpointer("conformer_archive.hdf5") as chk:
    chk["smiles"] = mol.to_smiles(canonical=True)
    chk["energies"] = energies[order]
    chk["coordinates"] = conformers[order]
    chk["geometry_tags"] = tags

print("saved energy span:", energies[order[-1]] - energies[order[0]])
```












<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#Tests-b9d729" markdown="1"> Tests</a> <a class="float-right" data-toggle="collapse" href="#Tests-b9d729"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Tests-b9d729" markdown="1">
 - [Schema](#Schema)
- [TreeFlattening](#TreeFlattening)
- [TreeArchiveJumps](#TreeArchiveJumps)
- [Pseudopickle](#Pseudopickle)
- [HDF5Serialization](#HDF5Serialization)
- [JSONSerialization](#JSONSerialization)
- [JSONPseudoPickleSerialization](#JSONPseudoPickleSerialization)
- [HDF5PseudoPickleSerialization](#HDF5PseudoPickleSerialization)
- [NumPySerialization](#NumPySerialization)
- [LineIndexedSupplier](#LineIndexedSupplier)
- [JSONLSupplier](#JSONLSupplier)
- [JSONLSupplierCreateDatabaseFolder](#JSONLSupplierCreateDatabaseFolder)
- [NPZLSupplier](#NPZLSupplier)
- [IterativeJSONL](#IterativeJSONL)
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
### <a class="collapse-link" data-toggle="collapse" href="#Setup-f46c19" markdown="1"> Setup</a> <a class="float-right" data-toggle="collapse" href="#Setup-f46c19"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Setup-f46c19" markdown="1">
 
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

#### <a name="TreeFlattening">TreeFlattening</a>
```python
    def test_TreeFlattening(self):
        data = {
            'file': 'test.txt',
            'filesystem': {'file':[['a'], ['b', 'c']]},
            'coords': 123,
            'initial': {
                'coords':np.random.rand(5, 3)
            },
            'final':{
                'coords':np.random.rand(1, 2)
            },
            'a':{'thing':{'b':1, 'c':2, "_type":"A", 'other':None}, 'other':None},
            'c':{'thing':None, 'other':9.1},
            'g':{"c":np.full(5, None)}
        }
        flat = flatten_tree(data)
        print(flat)
        rev = unflatten_tree(flat)
        print(rev)
        buf = io.BytesIO()
        write_flat_tree(buf, data)
        buf.seek(0)
        rev2 = read_flat_tree(buf)
        print(rev2)
```

#### <a name="TreeArchiveJumps">TreeArchiveJumps</a>
```python
    def test_TreeArchiveJumps(self):
        data = {
            'file': 'test.txt',
            'filesystem': {'file': [['a'], ['b', 'c']]},
            'coords': 123,
            'initial': {
                'coords': np.random.rand(5, 3)
            },
            'final': {
                'coords': np.random.rand(1, 2)
            },
            'a': {'thing': {'b': 1, 'c': 2, "_type": "A", 'other': None}, 'other': None},
            'c': {'thing': None, 'other': 9.1},
            'g': {"c": np.full(5, None)}
        }

        archive = NumpyTreeArchive.from_tree(data)

        buf = io.BytesIO()
        archive.save(buf)
        buf.seek(0)

        new_archive = NumpyTreeArchive.load(buf)
        print(new_archive)

        print(new_archive['a'])

        big_data = {
            f'entry_{i}':{
                'state_index':i,
                'energy':np.random.rand(1, 2),
                'coords':np.random.rand(1000, 3)
            }
            for i in range(30000)
        }

        archive = NumpyTreeArchive.from_tree(big_data)

        buf = io.BytesIO()
        archive.save(buf, save_jump_table=False)
        buf.seek(0)
        print(buf.getbuffer().nbytes)

        buf = io.BytesIO()
        archive.save(buf, save_jump_table=True)
        buf.seek(0)
        print(buf.getbuffer().nbytes)

        new_archive = NumpyTreeArchive.load(buf)
        print(new_archive)

        NumpyTreeArchive.from_tree(big_data)
        archive.save('/Users/Mark/Desktop/tree_save.npz')
        new_archive = NumpyTreeArchive.load('/Users/Mark/Desktop/tree_save.npz')
        print(new_archive['entry_100'])

        import orjson
        huh = orjson.dumps(big_data, option=orjson.OPT_SERIALIZE_NUMPY)
        print(len(huh))
        print(huh.decode()[:1000])

        with open('/Users/Mark/Desktop/tree_save.json', 'w+') as jsdump:
            jsdump.write(huh.decode())
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

#### <a name="LineIndexedSupplier">LineIndexedSupplier</a>
```python
    def test_LineIndexedSupplier(self):
        def deserialize(line):
            index, value = line.decode("utf-8").strip().split("|", 1)
            return {"index": int(index), "value": value}

        rows = [
            {"index": 0, "value": "alpha"},
            {"index": 1, "value": "beta"},
            {"index": 2, "value": "gamma"}
        ]
        with tmpf.TemporaryDirectory() as temp_dir:
            data_file = os.path.join(temp_dir, "rows.dat")
            index_file = os.path.join(temp_dir, "rows.idx.npy")
            archive_file = os.path.join(temp_dir, "rows.tar")
            expanded_dir = os.path.join(temp_dir, "expanded")
            with open(data_file, "wb") as stream:
                for row in rows:
                    stream.write(f"{row['index']}|{row['value']}\n".encode("utf-8"))

            supplier = LineIndexedSupplier(
                data_file,
                deserialization_function=deserialize
            )
            self.assertEqual(supplier.find_object(2), rows[2])
            self.assertEqual(list(supplier.consume_iter()), rows)

            line_indices = supplier.create_line_index()
            supplier.save_line_index(index_file, line_indices)
            indexed = LineIndexedSupplier(
                data_file,
                line_indices=index_file,
                deserialization_function=deserialize
            )
            self.assertEqual(len(indexed), len(rows))
            self.assertEqual(indexed.find_object(0), rows[0])

            LineIndexedSupplier.build_jump_database(
                data_file,
                archive_file,
                line_indices=line_indices,
                stored_file_name="custom.rows",
                metadata_arrays={"source_id": np.arange(len(rows))}
            )
            archived = LineIndexedSupplier.from_jump_database(
                archive_file,
                deserialization_function=deserialize
            )
            obj, metadata = archived.find_object(1)
            self.assertEqual(obj, rows[1])
            self.assertEqual(metadata["source_id"], 1)

            with tarfile.open(archive_file, "r:") as archive:
                self.assertIn("custom.rows", archive.getnames())
                archive.extractall(expanded_dir)
            expanded = LineIndexedSupplier.from_jump_database(
                expanded_dir,
                deserialization_function=deserialize
            )
            self.assertEqual(expanded.find_object(2)[0], rows[2])
```

#### <a name="JSONLSupplier">JSONLSupplier</a>
```python
    def test_JSONLSupplier(self):
        records = [
            {"id": 0, "text": "first"},
            {"id": 1, "text": "a value with\na newline"},
            {"id": 2, "text": "third"}
        ]
        with tmpf.TemporaryDirectory() as temp_dir:
            data_file = os.path.join(temp_dir, "records.jsonl")
            index_file = data_file + ".line_indices.npy"
            supplier = JSONLSupplier.write_objects(records[:1], data_file)
            supplier.append(records[1]).extend(records[2:])

            self.assertEqual(len(supplier), len(records))
            self.assertEqual(list(supplier.consume_iter()), records)
            self.assertEqual(supplier.find_object(1), records[1])
            self.assertEqual(len(np.load(index_file)), len(records))

            original_size = os.path.getsize(data_file)
            original_indices = np.load(index_file).copy()
            with self.assertRaises(TypeError):
                supplier.append({"not_json": object()})
            self.assertEqual(os.path.getsize(data_file), original_size)
            np.testing.assert_array_equal(np.load(index_file), original_indices)

            archive_file = os.path.join(temp_dir, "records.tar")
            JSONLSupplier.create_jump_database(
                records,
                archive_file,
                stored_file_name="objects.jsonl",
                metadata_arrays={"quality": np.array([.1, .2, .3])}
            )
            # create=True remains a no-op for an existing packaged database.
            archived = JSONLSupplier.from_jump_database(archive_file, create=True)
            obj, metadata = archived.find_object(2)
            self.assertEqual(obj, records[2])
            self.assertAlmostEqual(metadata["quality"], .3)
            with self.assertRaises(ValueError):
                archived.append({"id": 3})

            with tarfile.open(archive_file, "r:") as archive:
                self.assertIn("objects.jsonl", archive.getnames())
```

#### <a name="JSONLSupplierCreateDatabaseFolder">JSONLSupplierCreateDatabaseFolder</a>
```python
    def test_JSONLSupplierCreateDatabaseFolder(self):
        class CustomJSONLSupplier(JSONLSupplier):
            STORED_FILE_NAME = "dataset.jsonl"

        with tmpf.TemporaryDirectory() as temp_dir:
            database_dir = os.path.join(temp_dir, "dataset")
            supplier = CustomJSONLSupplier.from_jump_database(
                database_dir,
                create=True,
                name="example"
            )
            self.assertEqual(len(supplier), 0)
            self.assertEqual(
                set(os.listdir(database_dir)),
                {"dataset.jsonl", "line_indices.npy", "meta.json"}
            )
            with open(os.path.join(database_dir, "meta.json"), encoding="utf-8") as stream:
                self.assertEqual(json.load(stream), {
                    "name": "example",
                    "stored_file_name": "dataset.jsonl"
                })

            supplier.append({"row": 0}).extend(
                {"row": i} for i in range(1, 4)
            )
            reopened = CustomJSONLSupplier.from_jump_database(
                database_dir,
                create=True
            )
            self.assertEqual(len(reopened), 4)
            self.assertEqual(reopened.find_object(3), {"row": 3})

            broken_dir = os.path.join(temp_dir, "broken")
            os.mkdir(broken_dir)
            with open(
                os.path.join(broken_dir, CustomJSONLSupplier.STORED_FILE_NAME),
                "w",
                encoding="utf-8"
            ) as stream:
                stream.write('{"unindexed":true}\n')
            with self.assertRaises(ValueError):
                CustomJSONLSupplier.from_jump_database(broken_dir, create=True)
```

#### <a name="NPZLSupplier">NPZLSupplier</a>
```python
    def test_NPZLSupplier(self):
        records = [
            {
                "coords": np.arange(12).reshape(4, 3),
                "label": np.array("first")
            },
            {
                "coords": np.eye(3),
                "bytes": np.frombuffer(b"embedded\nnewlines\n", dtype=np.uint8)
            }
        ]
        with tmpf.TemporaryDirectory() as temp_dir:
            data_file = os.path.join(temp_dir, "records.npzl")
            supplier = NPZLSupplier.write_objects(records[:1], data_file)
            supplier.append(records[1]).extend([
                {"coords": np.full((2, 2), 4)},
                {"coords": np.full((1, 3), 5)}
            ])
            self.assertEqual(len(supplier), 4)
            np.testing.assert_array_equal(
                supplier.find_object(1)["bytes"],
                records[1]["bytes"]
            )
            np.testing.assert_array_equal(
                supplier.find_object(3)["coords"],
                np.full((1, 3), 5)
            )

            rescanned = NPZLSupplier(data_file)
            rebuilt_indices = rescanned.create_line_index()
            self.assertEqual(len(rebuilt_indices), 4)
            np.testing.assert_array_equal(
                rescanned.find_object(0)["coords"],
                records[0]["coords"]
            )

            archive_file = os.path.join(temp_dir, "records.tar")
            NPZLSupplier.create_jump_database(
                records,
                archive_file,
                stored_file_name="arrays.npzl"
            )
            archived = NPZLSupplier.from_jump_database(archive_file)
            np.testing.assert_array_equal(
                archived.find_object(1)["coords"],
                records[1]["coords"]
            )
            with tarfile.open(archive_file, "r:") as archive:
                self.assertIn("arrays.npzl", archive.getnames())
```

#### <a name="IterativeJSONL">IterativeJSONL</a>
```python
    def test_IterativeJSONL(self):
        from Psience.Molecools import Molecule
        from McUtils.Scaffolding import JSONLSupplier, JSONSerializer

        smis = [
            'COC(=O)c1ccc(C(=O)OC)c(NC(=S)NC(=O)c2ccc(OC)c(c2)[N+]([O-])=O)c1',
            'CCn1nccc1C(=O)Nc1cccc(N)c1',
            'CC(C(=O)c1ccc(C)cc1)n1c(CC#N)nc2cc3CCCCc3cc12',
            'Cc1ccc(C(=O)Nc2nc3c(C)cccn3n2)c(Cl)n1',
            'CSc1cccc(c1)C(=O)Nc1c(C)cc(cc1C(C)=C)C#N',
            'CCc1ccccc1OCC(=O)N(Cc1ccccc1)Cc1ccc2ccccc2c1',
            'CC(C)(C)C(=O)N(Cc1ccccc1F)Cc1ccccc1Br',
            'Cc1ccnc(SCC(=O)Nc2cc(Cl)c(Cl)cc2Cl)n1',
        ]

        database_dir = os.path.expanduser("~/Desktop/smiles_npz_data")
        database = NPZLSupplier.from_jump_database(database_dir, create=True)
        serializer = NumPySerializer()
        for _ in range(20):
            for smi in smis:
                mol = Molecule.from_string(smi, 'smi', num_confs=5)
                data_dict = {
                    'smi':mol[0].to_string('smi', remove_hydrogens=True),
                    'inchi':mol[0].to_string('inchi', remove_hydrogens=True),
                    'atoms':mol[0].atoms,
                    'coords':[m.coords for m in mol]
                }
                clean_dict = serializer.convert(data_dict).data # wrapped by default
                database.append(clean_dict)

        print(
            database.find_object(100)
        )
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
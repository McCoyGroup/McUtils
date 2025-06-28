from Peeves.TestUtils import *
import McUtils.Devutils as dev
from McUtils.Scaffolding import *
import McUtils.Parsers as parsers
from unittest import TestCase
import numpy as np, io, os, sys, tempfile as tmpf

class ScaffoldingTests(TestCase):

    @debugTest
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

    #region Checkpointing
    @validationTest
    def test_Pseudopickle(self):

        from McUtils.Numputils import SparseArray

        pickler = PseudoPickler()
        spa = SparseArray.from_diag([1, 2, 3, 4])
        serial = pickler.serialize(spa)
        deserial = pickler.deserialize(serial)
        self.assertTrue(np.allclose(spa.asarray(), deserial.asarray()))

    @validationTest
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
    @validationTest
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

    @validationTest
    def test_JSONPseudoPickleSerialization(self):

        from McUtils.Numputils import SparseArray

        tmp = io.StringIO()
        serializer = JSONSerializer()

        data = SparseArray.from_diag([1, 2, 3, 4])

        serializer.serialize(tmp, data)
        tmp.seek(0)
        loaded = serializer.deserialize(tmp)

        self.assertTrue(np.allclose(loaded.asarray(), data.asarray()))

    @validationTest
    def test_HDF5PseudoPickleSerialization(self):

        from McUtils.Numputils import SparseArray

        tmp = io.BytesIO()
        serializer = HDF5Serializer()

        data = SparseArray.from_diag([1, 2, 3, 4])

        serializer.serialize(tmp, data)
        tmp.seek(0)
        loaded = serializer.deserialize(tmp)

        self.assertTrue(np.allclose(loaded.asarray(), data.asarray()))

    @validationTest
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
    @validationTest
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
    @validationTest
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

    @validationTest
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

    @validationTest
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
    @validationTest
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

    class DataHolderClass:
        def __init__(self, **keys):
            self.data = keys
        def to_state(self, serializer=None):
            return self.data
        @classmethod
        def from_state(cls, state, serializer=None):
            return cls(**state)
    @validationTest
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

    @validationTest
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

    #endregion

    #region Logging
    @validationTest
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
    @validationTest
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

    #endregion

    #region Jobs
    @validationTest
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
    @validationTest
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
    @validationTest
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

    @validationTest
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

    @validationTest
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

    @validationTest
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

    #endregion
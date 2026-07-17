
import subprocess, os, tempfile as tf

__all__ = [
    "ExternalProgramRunner"
]

class ExternalProgramRunner:

    default_opts = {}
    def __init__(self, binary,
                 parser=None, prefix=None, suffix=None, delete=True,
                 **runtime_opts
                 ):
        """
        **LLM Docstring**

        Configure an external-program wrapper around a binary and persistent runtime defaults.

        :param binary: the executable path or command name
        :type binary: object

        :param parser: an optional result parser retained on the runner
        :type parser: object

        :param prefix: the temporary input-file prefix
        :type prefix: object

        :param suffix: the temporary input-file suffix
        :type suffix: object

        :param delete: whether temporary inputs and discovered outputs should be read and removed
        :type delete: object

        :param runtime_opts: default options forwarded to job execution
        :type runtime_opts: object

        :return: No value is returned.
        :rtype: None
        """
        if os.path.isfile(binary):
            binary = os.path.abspath(binary)
        self.binary = binary
        self.parser = parser
        self.opts = dict(self.default_opts, prefix=prefix, suffix=suffix, delete=delete, **runtime_opts)

    class _write_dir:
        def __init__(self, dir=None, dir_prefix=None, dir_suffix=None, delete=True):
            """
            **LLM Docstring**

            Store either a caller-supplied working directory or the options needed to create a temporary one.

            :param dir: the working directory, or `None` to allocate a temporary directory
            :type dir: object

            :param dir_prefix: prefix for an automatically created temporary directory
            :type dir_prefix: object

            :param dir_suffix: suffix for an automatically created temporary directory
            :type dir_suffix: object

            :param delete: whether temporary inputs and discovered outputs should be read and removed
            :type delete: object

            :return: No value is returned.
            :rtype: None
            """
            self.dir = dir
            self._temp_dirs = []
            self.delete = delete
            self.opts = {'prefix':dir_prefix, 'suffix':dir_suffix}
        def __enter__(self):
            """
            **LLM Docstring**

            Return the fixed directory, or create and enter a `TemporaryDirectory` when no directory was supplied.

            :return: return the fixed directory, or create and enter a `TemporaryDirectory` when no directory was supplied.
            :rtype: str
            """
            if self.dir is None:
                td = tf.TemporaryDirectory(**self.opts)
                self._temp_dirs.append(td)
                return td.__enter__()
            else:
                return self.dir
        def __exit__(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Exit and discard the most recently created temporary directory; fixed directories are left untouched.

            :param exc_type: the exception class leaving the context
            :type exc_type: object

            :param exc_val: the exception instance leaving the context
            :type exc_val: object

            :param exc_tb: the exception traceback leaving the context
            :type exc_tb: object

            :return: No value is returned.
            :rtype: None
            """
            if self.dir is None:
                td = self._temp_dirs.pop()
                td.__exit__(exc_type, exc_val, exc_tb)

    def prep_dir(self, dir):
        """
        **LLM Docstring**

        Placeholder hook for subclasses to populate a working directory before launching the external program.

        :param dir: the working directory, or `None` to allocate a temporary directory
        :type dir: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    @classmethod
    def subprocess_run(cls, binary, input_file, **subprocess_opts):
        """
        **LLM Docstring**

        Run `binary input_file`, resolving a local binary to an absolute path before calling `subprocess.run`.

        :param binary: the executable path or command name
        :type binary: object

        :param input_file: the generated input-file path
        :type input_file: object

        :param subprocess_opts: options forwarded to `subprocess.run`
        :type subprocess_opts: object

        :return: run `binary input_file`, resolving a local binary to an absolute path before calling `subprocess.run`.
        :rtype: subprocess.CompletedProcess
        """
        if os.path.isfile(binary):
            binary = os.path.abspath(binary)
        res = subprocess.run([binary, input_file], **subprocess_opts)
        return res

    text_file_extensions = ['.out', '.txt', '.log']
    @classmethod
    def _load_aux_file(cls, dir, file, delete):
        """
        **LLM Docstring**

        Resolve an auxiliary path relative to the work directory and either read it or return its filename. Text-like extensions are decoded as text; other files are read as bytes.

        :param dir: the working directory, or `None` to allocate a temporary directory
        :type dir: object

        :param file: an auxiliary filename or path
        :type file: object

        :param delete: whether temporary inputs and discovered outputs should be read and removed
        :type delete: object

        :return: resolve an auxiliary path relative to the work directory and either read it or return its filename. Text-like extensions are decoded as text; other files are read as bytes.
        :rtype: str | bytes | None
        """
        test = os.path.join(dir, file)
        if os.path.isfile(test):
            file = test
        if os.path.isfile(file):
            if delete:
                if os.path.splitext(file)[1] in cls.text_file_extensions:
                    mode = 'r'
                else:
                    mode = 'rb'
                with open(file, mode) as data:
                    # can't be sure if it's a binary file or not
                    return data.read()
            else:
                return file

    blacklist_files = [".DS_Store", ".git"]
    @classmethod
    def run_job(cls,
                binary, job,
                dir=None, dir_prefix=None, dir_suffix=None,
                mode='w',
                runner=None, prep_dir=None, prep_job=None, prep_results=None,
                return_auxiliary_files=True,
                prefix=None, suffix=None, delete=True,
                raise_errors=True,
                **subprocess_opts
                ):
        """
        **LLM Docstring**

        Materialize a job in a named temporary input file, execute the external binary in the work directory, collect requested output files, and optionally remove all temporary artifacts. Stderr is decoded and treated as an error whenever `raise_errors` is true.

        :param binary: the executable path or command name
        :type binary: object

        :param job: the job text or formattable job object
        :type job: object

        :param dir: the working directory, or `None` to allocate a temporary directory
        :type dir: object

        :param dir_prefix: prefix for an automatically created temporary directory
        :type dir_prefix: object

        :param dir_suffix: suffix for an automatically created temporary directory
        :type dir_suffix: object

        :param mode: the mode used to create the input file
        :type mode: object

        :param runner: an optional replacement process-launch function
        :type runner: object

        :param prep_dir: an optional callback that populates the work directory
        :type prep_dir: object

        :param prep_job: an optional callback that transforms the job text
        :type prep_job: object

        :param prep_results: an optional callback that extracts additional results from the work directory
        :type prep_results: object

        :param return_auxiliary_files: whether and how newly created output files should be collected
        :type return_auxiliary_files: object

        :param prefix: the temporary input-file prefix
        :type prefix: object

        :param suffix: the temporary input-file suffix
        :type suffix: object

        :param delete: whether temporary inputs and discovered outputs should be read and removed
        :type delete: object

        :param raise_errors: whether nonempty stderr should raise `IOError`
        :type raise_errors: object

        :param subprocess_opts: options forwarded to `subprocess.run`
        :type subprocess_opts: object

        :return: materialize a job in a named temporary input file, execute the external binary in the work directory, collect requested output files, and optionally remove all temporary artifacts. Stderr is decoded and treated as an error whenever `raise_errors` is true.
        :rtype: dict | tuple
        """

        results = {}
        with cls._write_dir(dir=dir, dir_prefix=dir_prefix, dir_suffix=dir_suffix) as dir:
            if prep_dir is not None:
                prep_dir(dir)
            with tf.NamedTemporaryFile(dir=dir, mode=mode, prefix=prefix, suffix=suffix, delete=False) as inp:
                if not isinstance(job, str) and hasattr(job, 'format'):
                    job = job.format()
                if prep_job is not None:
                    job = prep_job(job)
                results['input_file'] = job
                inp.write(results['input_file'])
            try:
                if return_auxiliary_files is True:
                    existing_files = set(os.listdir(dir))
                else:
                    existing_files = set()
                if runner is None:
                    runner = cls.subprocess_run
                res = runner(binary, inp.name, **dict(capture_output=True, cwd=dir, **subprocess_opts))
                results['process_output'] = res
                if prep_results is not None:
                    results.update(prep_results(dir))
                if return_auxiliary_files is True:
                    for file in os.listdir(dir):
                        if file not in existing_files and file not in cls.blacklist_files:
                            results[file] = cls._load_aux_file(dir, file, delete)
                elif isinstance(return_auxiliary_files, dict):
                    for k,v in return_auxiliary_files.items():
                        data = cls._load_aux_file(dir, v.format(name=inp.name), delete)
                        if data is not None:
                            results[k] = data
                elif return_auxiliary_files:
                    if isinstance(return_auxiliary_files, str):
                        return_auxiliary_files = [return_auxiliary_files]
                    for v in return_auxiliary_files:
                        data = cls._load_aux_file(dir, v.format(name=inp.name), delete)
                        if data is not None:
                            results[v] = data
                err = res.stderr.decode().strip()
                if raise_errors and len(err) > 0:
                    raise IOError(err)

                if not delete:
                    return inp, results
                else:
                    return results

            finally:
                if delete:
                    try:
                        os.remove(inp.name)
                    except OSError:
                        pass
        # if dir is not None:

    def run(self, job,
            dir=None, dir_prefix=None, dir_suffix=None,
            mode=None,
            runner=None, prep_dir=None, prep_job=None, prep_results=None,
            return_auxiliary_files=None,
            prefix=None, suffix=None, delete=None,
            raise_errors=None,
            **job_opts):
        """
        **LLM Docstring**

        Merge per-call overrides with the runner defaults and invoke `run_job` using this instance’s binary and directory-preparation hook.

        :param job: the job text or formattable job object
        :type job: object

        :param dir: the working directory, or `None` to allocate a temporary directory
        :type dir: object

        :param dir_prefix: prefix for an automatically created temporary directory
        :type dir_prefix: object

        :param dir_suffix: suffix for an automatically created temporary directory
        :type dir_suffix: object

        :param mode: the mode used to create the input file
        :type mode: object

        :param runner: an optional replacement process-launch function
        :type runner: object

        :param prep_dir: an optional callback that populates the work directory
        :type prep_dir: object

        :param prep_job: an optional callback that transforms the job text
        :type prep_job: object

        :param prep_results: an optional callback that extracts additional results from the work directory
        :type prep_results: object

        :param return_auxiliary_files: whether and how newly created output files should be collected
        :type return_auxiliary_files: object

        :param prefix: the temporary input-file prefix
        :type prefix: object

        :param suffix: the temporary input-file suffix
        :type suffix: object

        :param delete: whether temporary inputs and discovered outputs should be read and removed
        :type delete: object

        :param raise_errors: whether nonempty stderr should raise `IOError`
        :type raise_errors: object

        :param job_opts: per-call execution overrides
        :type job_opts: object

        :return: merge per-call overrides with the runner defaults and invoke `run_job` using this instance’s binary and directory-preparation hook.
        :rtype: dict | tuple
        """

        defaults = {
            k: v
            for k,v in dict(
                dir=dir, dir_prefix=dir_prefix, dir_suffix=dir_suffix,
                mode=mode,
                runner=runner, prep_dir=prep_dir, prep_job=prep_job, prep_results=prep_results,
                return_auxiliary_files=return_auxiliary_files,
                prefix=prefix, suffix=suffix, delete=delete,
                raise_errors=raise_errors
            ).items() if v is not None
        }
        return self.run_job(
            self.binary,
            job,
            **{
                **self.opts,
                'prep_dir':self.prep_dir,
                **defaults,
                **job_opts
            }
        )

        # with open(os.path.join(dir, 'atomicMasses.xml'), 'w+') as mass_file:
        #     mass_file.write(self.format_masses_file(self.atom_map) + "\n\n")

        # for key, ext in {"parallel": ".spectrum_parallel", "duschinsky": '.spectrum_dushinsky'}.items():
        #     test = inp.name + ext
        #     if os.path.isfile(test):
        #         with open(test) as strm:
        #             results[key] = strm.read()
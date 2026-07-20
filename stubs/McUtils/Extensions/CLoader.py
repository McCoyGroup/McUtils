import shutil, os, sys, subprocess, importlib, platform
__all__ = ['CLoader']

class CLoader:
    """
    A general loader for C++ extensions to python, based off of the kind of thing that I have had to do multiple times
    """

    def __init__(self, lib_name, lib_dir=None, load_path=None, src_ext='src', libs_ext='libs', description='An extension module', version='1.0.0', include_dirs=None, runtime_dirs=None, linked_libs=None, macros=None, extra_link_args=None, extra_compile_args=None, extra_objects=None, source_files=None, build_script=None, requires_make=True, out_dir=None, cleanup_build=True, recompile=False):
        """
        **LLM Docstring**

        Configure discovery, compilation, linking, and cleanup for a C++ extension module.

        If `lib_dir` is omitted, `lib_name` must name an existing directory, whose basename becomes the extension name.

        :param lib_name: extension module name or, when `lib_dir` is omitted, its project directory
        :type lib_name: str

        :param lib_dir: project root containing source and auxiliary-library directories
        :type lib_dir: str | None

        :param load_path: directories searched for an already-built extension
        :type load_path: Iterable[str] | None

        :param src_ext: source-directory name relative to `lib_dir`
        :type src_ext: str

        :param libs_ext: auxiliary-library directory name relative to `lib_dir`
        :type libs_ext: str

        :param description: package description passed to the build system
        :type description: str

        :param version: package version passed to the build system
        :type version: str

        :param include_dirs: header/library search directories
        :type include_dirs: Iterable[str] | None

        :param runtime_dirs: runtime library search directories
        :type runtime_dirs: Iterable[str] | None

        :param linked_libs: library names supplied to the linker
        :type linked_libs: Iterable[str] | None

        :param macros: preprocessor macro definitions
        :type macros: Iterable[tuple] | None

        :param extra_link_args: additional linker arguments
        :type extra_link_args: Iterable[str] | None

        :param extra_compile_args: additional compiler arguments
        :type extra_compile_args: Iterable[str] | None

        :param extra_objects: prebuilt object files to link
        :type extra_objects: Iterable[str] | None

        :param source_files: C/C++ source files; defaults to `<lib_name>.cpp`
        :type source_files: Iterable[str] | None

        :param build_script: custom build script or command specification
        :type build_script: str | dict | None

        :param requires_make: whether and how auxiliary libraries should be built
        :type requires_make: bool | str | dict

        :param out_dir: directory receiving the finished extension
        :type out_dir: str | None

        :param cleanup_build: whether to remove the temporary build directory
        :type cleanup_build: bool

        :param recompile: whether to bypass discovery and force recompilation
        :type recompile: bool

        :return: no value is returned
        :rtype: None
        """
        ...

    def load(self):
        """
        **LLM Docstring**

        Find or compile the configured extension and import it.

        The loaded module is cached on the loader. During import, the extension directory is temporarily inserted at the front of `sys.path`.

        :return: loaded extension module
        :rtype: types.ModuleType
        """
        ...

    def find_extension(self):
        """
        Tries to find the extension in the top-level directory

        :return:
        :rtype:
        """
        ...

    def compile_extension(self):
        """
        Compiles and loads a C++ extension

        :return:
        :rtype:
        """
        ...

    @property
    def src_dir(self):
        """
        **LLM Docstring**

        Return the configured source directory.

        :return: `lib_dir/src_ext`
        :rtype: str
        """
        ...

    @property
    def lib_lib_dir(self):
        """
        **LLM Docstring**

        Return the configured auxiliary-library directory.

        :return: `lib_dir/libs_ext`
        :rtype: str
        """
        ...

    def get_extension(self):
        """
        Gets the Extension module to be compiled

        :return:
        :rtype:
        """
        ...

    def configure_make_command(self, make_file):
        """
        **LLM Docstring**

        Translate a make configuration dictionary into compiler and linker command argument lists.

        Creates the build directory, derives object-file paths, prefixes compiler/linker flags, and appends a platform-specific shared-library suffix. The read `python_dir` entry is not otherwise used.

        :param make_file: build configuration containing at least `python_dir`, `compiler`, and `linker`
        :type make_file: dict

        :return: one compile command per source followed by one link command
        :rtype: list[list[str]]
        """
        ...

    def custom_make(self, make_file, make_dir):
        """
        A way to call a custom make file either for building the helper lib or for building the proper lib

        :param make_file:
        :type make_file:
        :param make_dir:
        :type make_dir:
        :return:
        :rtype:
        """
        ...

    def make_required_libs(self, library_types=('.so', '.pyd', '.dll')):
        """
        Makes any libs required by the current one

        :return:
        :rtype:
        """
        ...

    def build_lib(self):
        """
        **LLM Docstring**

        Build the extension in its source directory.

        Runs a custom build when configured, otherwise invokes `distutils.setup` with `build_ext --inplace`. On macOS it also rewrites dependent library install names to use `@rpath`.

        :return: no value is returned
        :rtype: None
        """
        ...

    @classmethod
    def locate_library(cls, libname, roots, extensions, library_types=('.so', '.pyd', '.dll')):
        """
        Tries to locate the library file (if it exists)

        :return:
        :rtype:
        """
        ...

    def locate_lib(self, name=None, roots=None, extensions=None, library_types=('.so', '.pyd', '.dll')):
        """
        Tries to locate the build library file (if it exists)

        :return:
        :rtype:
        """
        ...

    def cleanup(self):
        """
        **LLM Docstring**

        Move the built extension to its output directory and optionally remove build artifacts.

        The implementation locates the built library, replaces any existing target, and renames the library into place. The build-directory test uses `os.path.isdir` without calling it, so cleanup is attempted whenever `cleanup_build` is true.

        :return: target extension path, or `None` if no built library was found
        :rtype: str | None
        """
        ...
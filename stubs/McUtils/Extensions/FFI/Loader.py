"""
Provides a Loader object to load a potential from a C++ extension
"""
import os, numpy as np
import platform
import shutil
from .. import CLoader, ModuleLoader
from .Module import FFIModule
__all__ = ['FFILoader']
import os
import platform
import shutil
import subprocess
from pathlib import Path

def brew_prefix_for_arch(pkg):
    """
    **LLM Docstring**

    Locate a Homebrew package prefix by probing architecture-preferred Homebrew installations.

    :param pkg: Homebrew package name
    :type pkg: Any

    :return: the first successful `brew --prefix` result, or `None`
    :rtype: str | None
    """
    ...

def find_libffi():
    """Return (include_dir, lib_dir) for a user-installed libffi, or None."""
    ...

class FFILoader:
    """
    Provides a standardized way to load and compile a potential using a potential template
    """
    __props__ = ['src_ext', 'description', 'version', 'include_dirs', 'linked_libs', 'macros', 'source_files', 'build_script', 'requires_make', 'out_dir', 'cleanup_build', 'build_kwargsnodebug', 'threaded', 'extra_compile_args', 'extra_link_args', 'recompile']
    libs_folder = os.path.join(os.path.dirname(__file__), 'libs')
    cpp_std = '-std=c++17'

    def __init__(self, name, src=None, src_ext='src', load_path=None, description='A compiled potential', version='1.0.0', include_dirs=None, linked_libs=None, runtime_dirs=None, macros=None, source_files=None, build_script=None, requires_make=True, out_dir=None, cleanup_build=True, pointer_name=None, build_kwargs=None, nodebug=False, threaded=False, manage_threading_flags=True, manage_libffi_flags=True, extra_compile_args=None, extra_link_args=None, recompile=False, debug_level=False):
        """
        **LLM Docstring**

        Configure compilation and loading of the FFI extension, including NumPy, libffi, OpenMP, macro, and linker settings.

        :param name: extension module name
        :type name: Any

        :param src: source root
        :type src: Any

        :param src_ext: source subdirectory name
        :type src_ext: Any

        :param load_path: locations searched for an existing extension
        :type load_path: Any

        :param description: package description
        :type description: Any

        :param version: package version
        :type version: Any

        :param include_dirs: additional include directories
        :type include_dirs: Any

        :param linked_libs: additional linked libraries
        :type linked_libs: Any

        :param runtime_dirs: runtime library directories
        :type runtime_dirs: Any

        :param macros: compiler macro definitions
        :type macros: Any

        :param source_files: extension source files
        :type source_files: Any

        :param build_script: optional custom build script
        :type build_script: Any

        :param requires_make: whether helper libraries require a make step
        :type requires_make: Any

        :param out_dir: output directory
        :type out_dir: Any

        :param cleanup_build: whether build products are removed
        :type cleanup_build: Any

        :param pointer_name: stored legacy pointer attribute
        :type pointer_name: Any

        :param build_kwargs: additional `CLoader` arguments
        :type build_kwargs: Any

        :param nodebug: whether to define `_NODEBUG`
        :type nodebug: Any

        :param threaded: whether OpenMP support is enabled
        :type threaded: Any

        :param manage_threading_flags: whether platform OpenMP flags are added
        :type manage_threading_flags: Any

        :param manage_libffi_flags: whether libffi paths are discovered
        :type manage_libffi_flags: Any

        :param extra_compile_args: additional compiler flags
        :type extra_compile_args: Any

        :param extra_link_args: additional linker flags
        :type extra_link_args: Any

        :param recompile: whether to force recompilation
        :type recompile: Any

        :param debug_level: debug selector used by the wrapped module
        :type debug_level: Any

        :return: nothing; creates the configured `CLoader`
        :rtype: None
        """
        ...

    @classmethod
    def _check_install_lib_ffi(cls):
        """
        **LLM Docstring**

        Ensure a bundled `libffi` source directory exists, downloading the latest release when absent.

        :return: the bundled libffi target directory
        :rtype: str
        """
        ...

    @property
    def lib(self):
        """
        **LLM Docstring**

        Load and cache the compiled extension module.

        :return: the loaded Python extension
        :rtype: module
        """
        ...

    @property
    def caller_api_version(self):
        """
        **LLM Docstring**

        Detect the extension calling API from the presence of `_FFIModule`.

        :return: `2` for capsule-based modules, otherwise `1`
        :rtype: int
        """
        ...

    @property
    def call_obj(self):
        """
        The object that defines how to call the potential.
        Can either be a pure python function, an FFIModule, or a PyCapsule

        :return:
        :rtype:
        """
        ...
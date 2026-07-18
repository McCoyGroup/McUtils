"""
Provides a Loader object to load a potential from a C++ extension
"""

import os, numpy as np
import platform
import shutil

from .. import CLoader, ModuleLoader
from .Module import FFIModule

__all__ = [
    "FFILoader"
]

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
    machine = platform.machine()  # 'arm64' or 'x86_64'
    candidates = ["/opt/homebrew", "/usr/local"] if machine == "arm64" else ["/usr/local", "/opt/homebrew"]
    for prefix in candidates:
        brew_bin = f"{prefix}/bin/brew"
        try:
            out = subprocess.check_output([brew_bin, "--prefix", pkg], text=True).strip()
            return out
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    return None

def find_libffi():
    """Return (include_dir, lib_dir) for a user-installed libffi, or None."""
    system = platform.system()

    # 1. pkg-config is the most reliable source on macOS/Linux if available
    if system == "Linux" and shutil.which("pkg-config"):
        try:
            cflags = subprocess.check_output(
                ["pkg-config", "--cflags-only-I", "libffi"], text=True
            ).strip()
            libs = subprocess.check_output(
                ["pkg-config", "--libs-only-L", "libffi"], text=True
            ).strip()
            if cflags:
                inc = cflags.replace("-I", "").split()[0]
                lib = libs.replace("-L", "").split()[0] if libs else None
                return inc, lib
        except subprocess.CalledProcessError:
            pass

    # 2. conda environment (cross-platform, checked before OS-specific paths)
    conda_prefix = os.environ.get("CONDA_PREFIX")
    if conda_prefix:
        if system == "Windows":
            inc = Path(conda_prefix) / "Library" / "include"
            lib = Path(conda_prefix) / "Library" / "lib"
        else:
            inc = Path(conda_prefix) / "include"
            lib = Path(conda_prefix) / "lib"
        if (inc / "ffi.h").exists():
            return str(inc), str(lib)

    # 3. platform-specific fallbacks
    candidates = []
    if system == "Darwin":
        if shutil.which("brew"):

            try:
                prefix = brew_prefix_for_arch("libffi")
                candidates.append((f"{prefix}/include", f"{prefix}/lib"))
            except subprocess.CalledProcessError:
                pass
        candidates += [
            ("/opt/homebrew/opt/libffi/include", "/opt/homebrew/opt/libffi/lib"),
            ("/usr/local/opt/libffi/include", "/usr/local/opt/libffi/lib"),
            ("/opt/local/include", "/opt/local/lib"),
        ]
    elif system == "Linux":
        multiarch = subprocess.run(
            ["dpkg-architecture", "-qDEB_HOST_MULTIARCH"],
            capture_output=True, text=True
        )
        triplet = multiarch.stdout.strip() if multiarch.returncode == 0 else None
        if triplet:
            candidates.append((f"/usr/include/{triplet}", f"/usr/lib/{triplet}"))
        candidates += [
            ("/usr/include", "/usr/lib64"),
            ("/usr/include", "/usr/lib"),
            ("/usr/local/include", "/usr/local/lib"),
        ]
    elif system == "Windows":
        vcpkg_root = os.environ.get("VCPKG_ROOT")
        if vcpkg_root:
            triplet = "x64-windows"  # adjust as needed, or detect via platform.machine()
            base = Path(vcpkg_root) / "installed" / triplet
            candidates.append((str(base / "include"), str(base / "lib")))
        msys_root = os.environ.get("MSYSTEM_PREFIX", "C:/msys64/mingw64")
        candidates.append((f"{msys_root}/include", f"{msys_root}/lib"))

    for inc, lib in candidates:
        if inc and (Path(inc) / "ffi.h").exists():
            return inc, lib

    return None

class FFILoader:
    """
    Provides a standardized way to load and compile a potential using a potential template
    """
    __props__ = [
        "src_ext",
        "description",
        "version",
        "include_dirs",
        "linked_libs",
        "macros",
        "source_files",
        "build_script",
        "requires_make",
        "out_dir",
        "cleanup_build",
        'build_kwargs'
        'nodebug',
        'threaded',
        'extra_compile_args',
        'extra_link_args',
        'recompile'
    ]

    # src_folder = os.path.join(os.path.dirname(__file__), "src")
    libs_folder = os.path.join(os.path.dirname(__file__), "libs")
    cpp_std = '-std=c++17'
    def __init__(self,
                 name,
                 src=None,
                 src_ext='src',
                 load_path=None,
                 description="A compiled potential",
                 version="1.0.0",
                 include_dirs=None,
                 linked_libs=None,
                 runtime_dirs=None,
                 macros=None,
                 source_files=None,
                 build_script=None,
                 requires_make=True,
                 out_dir=None,
                 cleanup_build=True,
                 pointer_name=None,
                 build_kwargs=None,
                 nodebug=False,
                 threaded=False,
                 manage_threading_flags=True,
                 manage_libffi_flags=True,
                 extra_compile_args=None,
                 extra_link_args=None,
                 recompile=False,
                 debug_level=False
                 ):
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
        # if python_potential is False:

        if include_dirs is None:
            include_dirs = []
        include_dirs = (
                               tuple(include_dirs)
                               + (self.libs_folder, np.get_include())
                               # + (PotentialCaller.TBB_CentOS, PotentialCaller.TBB_Ubutu)
        )
        if linked_libs is None:
            linked_libs = []
        linked_libs = ("ffi",) + tuple(linked_libs) #+ ("plzffi", )

        self.threaded = threaded
        if macros is None:
            macros = []
        if nodebug:
            macros = list(macros) + [('_NODEBUG', True)]

        threading_flags = (["-fopenmp"] if self.threaded else [])

        if extra_compile_args is None:
            extra_compile_args = []
        else:
            extra_compile_args = list(extra_compile_args)

        if extra_link_args is None:
            extra_link_args = []
        else:
            extra_link_args = list(extra_link_args)

        if threaded and manage_threading_flags:
            # # Apple clang needs -Xpreprocessor to accept -fopenmp,
            # # since it doesn't ship libomp itself.
            threading_flags = ["-Xpreprocessor"] + threading_flags
            extra_link_args += ["-lomp"]

            # Homebrew's libomp is keg-only, so it's not on default paths.
            # Path differs between Apple Silicon and Intel Homebrew installs.
            if platform.machine() == "arm64":
                omp_prefix = "/opt/homebrew/opt/libomp"
            else:
                omp_prefix = "/usr/local/opt/libomp"

            include_dirs += (f"{omp_prefix}/include",)

            # extra_compile_args += [f"-I{omp_prefix}/include"]
            extra_link_args += [f"-L{omp_prefix}/lib"]

        if manage_libffi_flags:
            ffi_incl, ffi_lib = find_libffi()
            if ffi_incl is not None:
                include_dirs += (ffi_incl,)
                # extra_compile_args += [f"-I{ffi_incl}"]
            if ffi_lib is not None:
                extra_link_args += [f"-L{ffi_lib}"]

        extra_compile_args = threading_flags + [self.cpp_std] + extra_compile_args
        self.c_loader = CLoader(
            name,
            src,
            load_path=load_path,
            src_ext=src_ext,
            description=description,
            version=version,
            include_dirs=include_dirs,
            runtime_dirs=runtime_dirs,
            linked_libs=(("omp",) if self.threaded else ()) + linked_libs,
            macros=macros,
            source_files=source_files,
            build_script=build_script,
            requires_make=requires_make,
            out_dir=out_dir,
            cleanup_build=cleanup_build,
            extra_compile_args=extra_compile_args,
            extra_link_args=[] if extra_link_args is None else list(extra_link_args),
            recompile=recompile,
            **({} if build_kwargs is None else build_kwargs)
        )
        # else:
        #     self.c_loader = None

        # Need to insert code here to allow for new caller API to work
        self._lib = None

        self._attr = pointer_name
        # self.function_name = pointer_name
        self.debug_level = debug_level

    @classmethod
    def _check_install_lib_ffi(cls):
        """
        **LLM Docstring**

        Ensure a bundled `libffi` source directory exists, downloading the latest release when absent.

        :return: the bundled libffi target directory
        :rtype: str
        """
        targ = os.path.join(cls.libs_folder, 'libffi')
        if not os.path.exists(targ):
            from ...ExternalPrograms import GitHubReleaseManager

            manager = GitHubReleaseManager()
            latest = manager.latest_release('libffi', 'libffi')
            res = manager.release_manager.get_resource(latest[manager.resource_key], load_resource=False)
            print(res)
            shutil.copytree(res, targ)
        return targ

    @property
    def lib(self):
        """
        **LLM Docstring**

        Load and cache the compiled extension module.

        :return: the loaded Python extension
        :rtype: module
        """
        if self._lib is None:
            self._lib = self.c_loader.load()
        return self._lib
    @property
    def caller_api_version(self):
        """
        **LLM Docstring**

        Detect the extension calling API from the presence of `_FFIModule`.

        :return: `2` for capsule-based modules, otherwise `1`
        :rtype: int
        """
        if hasattr(self.lib, "_FFIModule"): # currently how we're dispatching
            return 2
        else:
            return 1
    @property
    def call_obj(self):
        """
        The object that defines how to call the potential.
        Can either be a pure python function, an FFIModule, or a PyCapsule

        :return:
        :rtype:
        """
        return FFIModule.from_module(self.lib, debug=self.debug_level)
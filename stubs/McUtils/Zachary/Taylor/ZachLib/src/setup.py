from distutils.core import setup, Extension
import shutil, os, sys
lib_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(lib_dir, 'src')
libname = 'ZachLib'

def get_macros():
    ...

def get_extension():
    ...

def setup_compile():
    ...

def compile():
    ...

def find_source():
    ...

def load():
    ...
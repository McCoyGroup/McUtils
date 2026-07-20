"""
Provides utilities for working with objects, defaults, etc. to abstract away common idoms
"""
__all__ = ['default', 'is_default', 'handle_default', 'uninitialized', 'is_uninitialized', 'handle_uninitialized', 'missing', 'is_missing', 'is_interface_like', 'is_dict_like', 'is_option_spec_like', 'destructure_option_spec', 'is_list_like', 'is_number', 'is_int', 'is_atomic', 'cached_eval', 'merge_dicts', 'str_comp', 'str_is', 'str_in', 'str_startswith', 'str_endswith', 'str_elide', 'resolve_key_collision', 'merge_dicts', 'context_wrap', 'slice_dict', 'dict_take', 'is_filepath_like', 'safe_open', 'write_file', 'read_file', 'read_json', 'write_json', 'split_path', 'drop_directory_prefix', 'filename', 'bytestream_hash', 'string_hash', 'file_hash', 'files_hash', 'directory_hash', 'compress_dir', 'compressed_dir_bytes', 'decompress_dir', 'unpack_gzip_bytes', 'FileBackedIO', 'StreamInterface', 'Logger', 'NullLogger', 'LogLevel', 'LoggingBlock', 'OptionsSet', 'OptionsMethodDispatch', 'StreamRedirect', 'OutputRedirect', 'DefaultDirectory', 'temporary_sys_path_insert', 'Schema']
from .core import *
from .FileHelpers import *
from .Loggers import *
from .Options import *
from .Redirects import *
from .Schema import *
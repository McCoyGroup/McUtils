### `FileHelpers.py`
- `is_filepath_like(file, bad_chars=None)` — Test whether a value looks like a file path (a `Path`, or a string free of
  - **class `safe_open`**
    - `__init__(file, **opts)`
  - **class `open_opts`**
- `write_file(file, data, mode='w+', **opts)` — Write data to a file (path or stream).
- `read_file(file, **opts)` — Read the full contents of a file (path or stream).
- `read_json(file, loader=None, **opts)` — Read and parse JSON from a file, separating `open` options from loader options.
- `read_orjson(file, loader=None, mode='rb', **opts)` — Read and parse JSON from a file using `orjson`.
- `write_json(file, data, writer=None, mode='w+', encoder=None, **opts)` — Serialize data to a file as JSON, separating `open` options from dumper options
- `write_orjson(file, data, writer=None, mode='w+b', **opts)` — Serialize data to a file as JSON using `orjson`.
- `split_path(path, nsteps=-1)` — Split a path into its components, either fully (`nsteps < 0`) or only the last
- `drop_directory_prefix(prefix, path)` — Return `path` with the leading portion it shares with `prefix` removed.
- `filename(path, check_dir=True)` — Return the base filename (without extension), optionally requiring that the path
- `string_hash(string, base=None, bits=None, id_generator=None)` — Hash a string (via its UTF-8 bytes).
- `bytestream_hash(filestream, base=None, bits=None, id_generator=None)` — https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
- `file_hash(filename, base=None, bits=None, id_generator=None)` — Hash the contents of a file.
- `files_hash(files, base=None, bits=None, id_generator=None)` — Hash the concatenated contents of several files into a single digest.
- `directory_hash(directory, files=None, base=None, bits=None, id_generator=None)` — Hash the contents of a directory's files.
- `compress_dir(config_dir, cache_dir=None, name=None, files=None)` — Create a gzipped tar archive of (some of) a directory's files.
- `compressed_dir_bytes(config_dir, name=None, files=None)` — Return the raw bytes of a gzipped tar archive of a directory.
- `decompress_dir(target_dir, config_gzip)` — Unpack an archive into a target directory.
- `unpack_gzip_bytes(build_dir, gzip)` — Unpack a gzipped tar archive supplied as raw bytes into a directory (via a
  - **class `FileBackedIO`**
    - `__init__(buffer, mode='w+', file=None, delete=True, **tempfile_opts)`
    - `resolve_buffer()` — Return the buffer contents, calling the generator if the buffer is a callable.
    - `name()` — The backing file's path (or `None` if not yet created).
    - `file()` — The backing file path, creating (and seeding) a temporary file on first access.
    - `write(file=None, mode=None)` — Write the buffer contents out to a file.
  - **class `StreamInterface`**
    - `__init__(stream, file_backed=False, **file_opts)`
    - `is_binary()` — Whether the stream is (or would be opened in) binary mode.
    - `get_encoding()` — **LLM Docstring**
    - `is_path_like(input)` — Heuristic test for whether a string is a path rather than inline content (no

### `Loggers.py`
  - **class `LogLevel`** (enum.Enum)
    > A simple log level object to standardize more pieces of the logger interface
  - **class `LoggingBlock`**
    > A class that extends the utility of a logger by automatically setting up a
    > named block of logs that add context and can be
    > that
    - `__init__(logger, log_level=None, block_level=0, block_level_padding=None, tag=None, opener=None, prompt=None, closer=None, printoptions=None, captured_output_tag='', capture_output=True, captured_error_tag='', capture_errors=None, **tag_vars)`
    - `tag()` — The resolved (formatted) block tag, computed lazily from a string, a
    - `stream_redirect(tag, base_stream)` — Build a `StreamRedirect` that routes writes through the logger with the given
  - **class `Logger`**
    > Defines a simple logger object to write log data to a file based on log levels.
    - `__init__(log_file=None, log_level=None, print_function=None, padding='', newline='\n', repad_messages=True, block_options=None)`
    - `to_state(serializer=None)` — Return the serializable state of the logger (dropping the print function when
    - `from_state(state, serializer=None)` — Rebuild a logger from its serialized state.
    - `block(**kwargs)` — Open a nested logging block on this logger.
    - `register(key)` — Registers the logger under the given key
    - `lookup(key, construct=False)` — Looks up a logger.
    - `preformat_keys(key_functions)` — Generates a closure that will take the supplied
    - `format_message(message, *params, preformatter=None, _repad=None, _newline=None, _padding=None, **kwargs)` — Format a message template with the given parameters, optionally running a
    - `format_metainfo(metainfo)` — Format block meta-information as a JSON string (or empty string when absent).
    - `pad_newlines(obj, padding=None, newline=None, **kwargs)` — Replace newlines in a value with the newline-plus-padding prefix so multi-line
    - `split_lines(obj)` — Split a value's string form into lines.
    - `prep_array(obj)` — Render a numpy array to lines without truncation (wide/high print limits).
    - `prep_dict(obj)` — Render a dict as `key: value` lines.
    - `log_print(message, *messrest, message_prepper=None, padding=None, newline=None, log_level=None, metainfo=None, print_function=None, print_options=None, sep=None, end=None, file=None, flush=None, preformatter=None, **kwargs)` — :param print_options: options to be passed through to print
  - **class `NullLogger`** (Logger)
    > A logger that implements the interface, but doesn't ever print.
    > Allows code to avoid a bunch of "if logger is not None" blocks
    - `__init__(*log_files, **logger_opts)`
    - `log_print(message, *params, print_options=None, padding=None, newline=None, **kwargs)` — **LLM Docstring**
    - `block(capture_output=False, **kwargs)` — Open a logging block with output capture disabled by default.

### `Options.py` — Provides functionality for managing large sets of options
  - **class `OptionsSet`**
    > Provides a helpful manager for those cases where
    > there are way too many options and we need to filter
    > them across subclasses and things
    - `__init__(*d, **ops)`
    - `update(**ops)` — Update the options from keyword arguments.
    - `keys()` — **LLM Docstring**
    - `items()` — **LLM Docstring**
    - `save(file, mode=None, attribute=None)` — Serialize the options to a file.
    - `load(file, mode=None, attribute=None)` — Load options from a file into a new `OptionsSet`.
    - `extract_kwarg_keys(obj)` — Determine the keyword-argument names of a callable from its signature (the
    - `get_props(obj)` — Determine the set of option names an object accepts, from its `__props__`,
    - `bind(obj, props=None)` — Set each option that `obj` accepts as an attribute on `obj`.
    - `filter(obj, props=None)` — Return the subset of options whose names are accepted by `obj`.
    - `exclude(obj, props=None)` — Return the subset of options whose names are *not* accepted by `obj`.
    - `split(obj, props=None)` — Split the options into the `(accepted, excluded)` subsets for `obj`.
  - **class `OptionsMethodDispatch`**
    - `__init__(methods_table, attributes_map=None, default_method=None, methods_enum=None, case_insensitive=True, allow_custom_methods=True, ignore_bad_enum_keys=False, method_key='method')`
    - `register(method_name, method, base_attributes=None)` — Register a method under a name, optionally mapping a set of base attributes to
    - `load_methods_table()` — Return the methods table, merging any generator-produced entries with the
    - `prep_method_spec(method_spec)` — Normalize a method specification into a `(method, options)` pair, accepting
    - `resolve(method_spec)` — Resolve a method specification into the actual `(method, options)` to use,

### `Redirects.py`
- `temporary_sys_path_insert(path)`
  - **class `StreamRedirect`**
    - `__init__(logger, base_stream=None, line_join=True, strip_empty=True)`
    - `write(data)` — Forward written data to the logger, skipping whitespace-only data when
    - `writelines(lines)` — Forward multiple lines to the logger, joining them with the configured joiner
    - `flush()` — Flush the underlying base stream, if any.
    - `seek(offset, whence=0)` — Seek on the underlying base stream, if any.
    - `seekable()` — Whether the underlying base stream is seekable.
    - `read(size)` — Read from the underlying base stream, if any.
    - `readline(limit=-1)` — Read a line from the underlying base stream, if any.
    - `readlines(hint=-1)` — Read all lines from the underlying base stream, if any.
  - **class `OutputRedirect`**
    - `__init__(redirect=True, stdout=None, stderr=None, capture_output=False, capture_errors=None, file_handles=False)`
    - `get_handle(handles=None, file_handles=False)` — Resolve a capture target: return the supplied handle, a fresh in-memory buffer,
    - `get_temp_stream()` — Open and enter a writable named temporary file to capture output into.
  - **class `DefaultDirectory`**
    - `__init__(output_dir=None, chdir=True, **tempdir_opts)`
    - `get_temp_dir()` — Create a `TemporaryDirectory` using the stored options.
    - `dirname()` — The path of the managed directory (or `None` before entering).

### `Schema.py` — Basic layer for Schema validation that provides a superset of JSON schema validation
  - **class `JSONSchemaTypes`** (enum.Enum)
    > Real access pattern: JSONSchemaTypes.<MemberName> (this is an enum with 6 members, e.g. JSONSchemaTypes.String == 'string'). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:
  - **class `TypeValidator`**
    - `__init__(type_obj)`
    - `resolve_typestr(type_spec)` — Resolve a type name to an actual type: a builtin alias, a JSON schema type, or a
    - `get_schema_type(t)` — Map a JSON-schema type enum member to the concrete type(s)/predicate(s) that
    - `prep_type_obj(t)` — Normalize a type object into a tuple of type(s)/predicate(s), expanding
    - `get_validators(type_spec)` — Split a type specification into a tuple of concrete types (for `isinstance`) and
    - `validate(obj, throw=False)` — Validate a value against the types and validator callables.
  - **class `ValueValidator`**
    - `__init__(enum=None, const=None, multipleOf=None, maximum=None, minimum=None, exclusiveMaximum=None, exclusiveMinimum=None, maxLength=None, minLength=None, pattern=None, maxItems=None, minItems=None, uniqueItems=None, maxProperties=None, minProperties=None, required=None, validation_function=None)`
    - `validate(value, throw=False)` — Validate a value against all active constraints.
  - **class `Schema`**
    > An object that represents a schema that can be used to test
    > if an object matches that schema or not
    - `__init__(schema, optional_schema=None)`
    - `required_keys()` — The set of property keys the schema requires (computed lazily).
    - `is_json_schema(schema)` — Test whether a schema dict is already a JSON schema (has a `$schema` key).
    - `canonicalize_schema(schema, optional_schema=None)` — Normalize any accepted schema form into a JSON schema with validator objects,
    - `validate(obj, throw=True)` — Validates that `obj` matches the provided schema
    - `to_dict(obj, throw=True, ignore_invalid=False)` — Converts `obj` into a plain `dict` representation

### `core.py` — Provides a set of singleton objects that can declare their purpose a little bit better than None can
  - **class `SingletonType`**
    > A base type for singletons
  - **class `DefaultType`** (SingletonType)
    > A type for declaring an argument should use its default value (for when `None` has meaning)
  - **class `MissingType`** (SingletonType)
    > A type for declaring a value is missing (for when `None` has meaning)
  - **class `UninitializedType`** (SingletonType)
    > A type for declaring an argument should use its default value (for when `None` has meaning)
- `is_atomic(obj, interface_types=(str, bool, numbers.Number), exlusion_types=None, implementation_props=None)` — Test whether an object is an atomic value (string, bool, or number by default).
- `is_number(obj, interface_types=(numbers.Number,), exlusion_types=None, implementation_props=None)` — Test whether an object is a number.
- `is_int(obj, interface_types=(numbers.Integral,), exlusion_types=None, implementation_props=None)` — Test whether an object is an integer.
- `is_interface_like(obj, interface_types, exlusion_types, implementation_attrs)` — General duck-typing test: an object qualifies if it isn't an excluded type and is
- `is_dict_like(obj, interface_types=(dict, types.MappingProxyType), exlusion_types=None, implementation_props=('items',))` — Test whether an object is dict-like (a mapping, or exposes `items`).
- `is_list_like(obj, interface_types=(list, tuple), exlusion_types=(str, dict, type), implementation_props=('__getitem__',))` — Test whether an object is list-like (a sequence, excluding strings/dicts/types).
- `is_default(obj, allow_None=True)` — Test whether a value is the `default` singleton (optionally treating `None` as
- `is_option_spec_like(obj, allow_enums=True)` — Test whether an object can be destructured into a `(method, options)` option
- `destructure_option_spec(spec, allow_enums=True, method_key='method')` — Split an option specification into a `(method, options)` pair, accepting bare
- `handle_default(opt, default_value, allow_None=True)` — Return `default_value` when `opt` is the `default` singleton, else `opt`.
- `is_uninitialized(obj, allow_None=True)` — Test whether a value is the `uninitialized` singleton (optionally treating `None`
- `handle_uninitialized(opt, initializer, allow_None=True, args=(), kwargs=None)` — Return the result of calling `initializer` when `opt` is uninitialized, else
- `is_missing(obj, allow_None=True)` — Test whether a value is the `missing` singleton (optionally treating `None` as
- `cached_eval(cache, key, generator, *, condition=None, args=(), kwargs=None)` — Return `cache[key]`, computing and storing it via `generator` on a miss;
- `str_comp(str_val, test, test_val, ignore_case=False)` — Compare a string against a test value with a comparison callback, optionally
- `str_is(str_val, test_val, ignore_case=False)` — Test whether a string equals a value (optionally case-insensitively).
- `str_in(str_val, test_vals, ignore_case=False)` — Test whether a string is contained in a collection (optionally
- `str_startswith(str_val, test_vals, ignore_case=False)` — Test whether a string starts with a prefix (optionally case-insensitively).
- `str_endswith(str_val, test_vals, ignore_case=False)` — Test whether a string ends with a suffix (optionally case-insensitively).
- `str_elide(long_str, width=80, placeholder='...')` — Truncate a long string to `width` characters by replacing its middle with a
- `resolve_key_collision(a, b, k, merge_iterables=True)` — Default collision handler for `merge_dicts`: recursively merge dict values, union
- `merge_dicts(a, b, collision_handler=None, merge_iterables=True)` — Merge two dicts, resolving colliding keys with a handler (defaulting to
  - **class `context_wrap`**
    - `__init__(obj)`
  - **class `slice_dict`**
    - `__init__(dict_obj)`
- `dict_take(dict_obj, spec)` — Extract entries from a mapping by an integer position, a slice of positions, a
### `CLIs.py` — Simple package for easily creating command line interfaces in a
  - **class `Command`**
    > A holder for a command that just automates type handling &
    > that sort of thing
    - `__init__(name, method)`
    - `get_help()` — Gets single method help string
    - `get_parse_dict(*spec)` — Builds a parse spec to feed into an ArgumentParser later
    - `get_parse_spec()` — Gets a parse spec that can be fed to ArgumentParser
    - `parse()` — Generates a parse spec, builds an ArgumentParser, and parses the arguments
  - **class `CommandGroup`**
    > Generic interface that defines an available set of commands
    > as class methods.
    > Basically just exists to be ingested by a CLI.
  - **class `CLI`**
    > A representation of a command line interface
    > which layers simple command dispatching on the basic
    > ArgParse interface
    - `__init__(name, description, *groups, cmd_name=None)`
    - `parse_group_command()` — Parses a group and command argument (if possible) and prunes `sys.argv`
    - `get_command()` — Consume the group and command tokens, support the default-group shorthand, and return a bound `Comm…
    - `get_group(grp)` — Resolve a registered command group and raise an informative error for missing or absent default gro…
    - `run_command()` — Resolve and execute the selected command, printing the result only when resolution produced help te…
    - `get_help()` — Gets the help string for the CLI
    - `help(print_help=True)` — Remove the help token, generate the full help text, optionally print it, and return it.
    - `run_parse(parse, unknown)` — Provides a standard entry point to running stuff using the default CLI
    - `parse_toplevel_args()` — Parses out the top level flags that the program supports
    - `run()` — Parses the arguments in `sys.argv` and dispatches to the approriate action.

### `Caches.py`
  - **class `Cache`**
    > Simple cache base class
    - `get(item, default=None)` — Retrieve `item`, returning `default` only when the cache raises `KeyError`.
  - **class `MaxSizeBackend`**
    - `keys()` — Return the keys currently stored by the bounded-cache backend.
    - `pop()` — Remove and return the entry selected for eviction by the backend policy.
  - **class `LRUDict`** (MaxSizeBackend)
    - `__init__()`
    - `keys()` — Return the ordered key view of the backend.
    - `pop()` — Evict and return the least-recently-used key/value pair.
  - **class `FIFODict`** (MaxSizeBackend)
    - `__init__()`
    - `keys()` — :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.
    - `pop()` — Remove and return the earliest inserted key/value pair.
  - **class `MaxSizeCache`** (Cache)
    > Simple lru-cache to support ravel/unravel ops
    - `__init__(max_items=128, cache_type=None)`
    - **class `Backends`** (enum.Enum)
    - `resolve_cache_type(type_name)` — Resolve a callable or registered backend specification and instantiate the backend with its options.
    - `keys()` — Expose the keys from the selected backend.
  - **class `ObjectRegistryDefaults`**
  - **class `RegistryDefaultContext`**
    - `__init__(registry, value)`
  - **class `ObjectRegistry`**
    > Provides a simple interface to global object registries
    > so that pieces of code don't need to pass things like loggers
    > or parallelizers through every step of the code
    - `__init__(default=ObjectRegistryDefaults.Raise)`
    - `temp_default(val)` — Create a context manager that temporarily replaces the registry fallback value.
    - `lookup(key)` — Return the registered object, or the configured default when missing-key lookup is non-raising.
    - `register(key, val)` — Store a weak reference to `val` under `key`.
    - `keys()` — :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.
    - `items()` — Return the live registry key/value pairs.
    - `values()` — :return: A view or list of the requested registry, cache, checkpoint, or mapping entries.

### `Checkpointing.py`
  - **class `CheckpointerKeyError`** (KeyError)
  - **class `Checkpointer`**
    > General purpose base class that allows checkpointing to be done easily and cleanly.
    > Intended to be a passable object that allows code to checkpoint easily.
    - `__init__(checkpoint_file, allowed_keys=None, omitted_keys=None)`
    - `extension_map()` — Return the extension-to-checkpointer dispatch table, honoring a class-level override when present.
    - `build_canonical(checkpoint)` — Dispatches over types of objects to make a canonical checkpointer
    - `from_file(file, **opts)` — Dispatch function to load from the appropriate file
    - `cached_eval(key, generator, *, condition=None, args=(), kwargs=None)` — Evaluate or load a keyed value through `dev.cached_eval`, using this checkpointer as the mapping ba…
    - `is_open()` — Report whether a checkpoint stream is currently open.
    - `stream()` — Return the currently open stream, or `None` outside an active context.
    - `open_checkpoint_file(chk)` — Opens the passed `checkpoint_file` (if not already open)
    - `close_checkpoint_file(stream)` — Closes the opened checkpointing stream
    - `save_parameter(key, value)` — Saves a parameter to the checkpoint file
    - `load_parameter(key)` — Loads a parameter from the checkpoint file
    - `delete_parameter(key)` — Default deletion hook; concrete checkpointers must override it to support deletion.
    - `check_parameter(key)` — Validate the key policy and test whether loading the key succeeds.
    - `update(vals)` — Write all key/value pairs from a mapping or iterable, opening the checkpoint around the operation w…
    - `get_keys(keys)` — Load a sequence of keys in order, with automatic context management.
    - `check_allowed_key(item)` — Enforce top-level allow and omit lists; tuple paths are checked by their first component.
    - `get(key, default=None)` — Load a key and return `default` when the backend raises `KeyError`.
    - `pop(key, *default)` — Load and delete a key, optionally returning a supplied default when the key is absent.
    - `keys()` — Returns the keys of currently checkpointed
  - **class `DumpCheckpointer`** (Checkpointer)
    > A subclass of `CheckpointerBase` that writes an entire dump to file at once & maintains
    > a backend cache to update it cleanly
    - `__init__(file, cache=None, open_kwargs=None, allowed_keys=None, omitted_keys=None)`
    - `load_cache()` — Create an empty dictionary when no backend cache has been loaded.
    - `dump()` — Writes the entire data structure
    - `convert()` — Converts the cache to an exportable form if needed
    - `open_checkpoint_file(chk)` — Opens the passed `checkpoint_file` (if not already open)
    - `close_checkpoint_file(stream)` — Closes the opened checkpointing stream
    - `save_parameter(key, value)` — Saves a parameter to the checkpoint file
    - `check_parameter(key)` — Loads a parameter from the checkpoint file
    - `load_parameter(key)` — Loads a parameter from the checkpoint file
    - `delete_parameter(key)` — Loads a parameter from the checkpoint file
    - `keys()` — Return top-level backend keys, opening the checkpointer temporarily if necessary.
  - **class `JSONCheckpointer`** (DumpCheckpointer)
    > A checkpointer that uses JSON as a backend
    - `__init__(file, cache=None, serializer=None, open_kwargs=None, allowed_keys=None, omitted_keys=None)`
    - `load_cache()` — Load a nonempty JSON checkpoint into a dictionary, otherwise initialize an empty cache.
    - `dump()` — Writes the entire data structure
  - **class `NumPyCheckpointer`** (DumpCheckpointer)
    > A checkpointer that uses NumPy as a backend
    - `__init__(file, cache=None, serializer=None, open_kwargs=None, allowed_keys=None, omitted_keys=None)`
    - `load_cache()` — Load a nonempty NumPy checkpoint into a dictionary, otherwise initialize an empty cache.
    - `dump()` — Writes the entire data structure
  - **class `HDF5Checkpointer`** (Checkpointer)
    > A checkpointer that uses an HDF5 file as a backend.
    > Doesn't maintain a secondary `dict`, because HDF5 is an updatable format.
    - `__init__(checkpoint_file, serializer=None, allowed_keys=None, omitted_keys=None)`
    - `open_checkpoint_file(chk)` — Opens the passed `checkpoint_file` (if not already open)
    - `close_checkpoint_file(stream)` — Opens the passed `checkpoint_file` (if not already open)
    - `save_parameter(key, value)` — Saves a parameter to the checkpoint file
    - `load_parameter(key)` — Loads a parameter from the checkpoint file
    - `keys()` — Open the stream as an HDF5 file or group as needed and return its top-level keys.
  - **class `DictCheckpointer`** (Checkpointer)
    > A checkpointer that doesn't actually do anything, but which is provided
    > so that programs can turn off checkpointing without changing their layout
    - `__init__(checkpoint_file=None, allowed_keys=None, omitted_keys=None)`
    - `open_checkpoint_file(chk)` — Opens the passed `checkpoint_file` (if not already open)
    - `close_checkpoint_file(stream)` — Opens the passed `checkpoint_file` (if not already open)
    - `save_parameter(key, value)` — Saves a parameter to the checkpoint file
    - `load_parameter(key)` — Loads a parameter from the checkpoint file
    - `delete_parameter(key)` — Loads a parameter from the checkpoint file
    - `keys()` — Return a list of in-memory checkpoint keys.
    - `get(key, default=None)` — Return a dictionary value or default without opening a stream.
    - `pop(key, *default)` — Remove and return a dictionary value using normal `dict.pop` semantics.
  - **class `NullCheckpointer`** (Checkpointer)
    > A checkpointer that saves absolutely nothing
    - `__init__(checkpoint_file=None, allowed_keys=None, omitted_keys=None)`
    - `open_checkpoint_file(chk)` — Opens the passed `checkpoint_file` (if not already open)
    - `close_checkpoint_file(stream)` — Opens the passed `checkpoint_file` (if not already open)
    - `save_parameter(key, value)` — Saves a parameter to the checkpoint file
    - `load_parameter(key)` — Loads a parameter from the checkpoint file
    - `delete_parameter(key)` — Loads a parameter from the checkpoint file
    - `keys()` — Return an empty key list because the null backend never retains data.

### `Configurations.py` — Provides functionality for managing configurations stored in files
  - **class `Config`**
    > A configuration object which basically just supports
    > a dictionary interface, but which also can automatically
    > filter itself so that it only provides the keywords supported
    > by a `from_config` method.
    - `__init__(config, serializer=None, extra_params=None)`
    - `find_config(config, name=None, extensions=None)` — Finds configuration file (if config isn't a file)
    - `get_serializer(file)` — Select a serializer instance from the configuration file extension.
    - `new(loc, init=None)` — Create the default JSON configuration file in a directory and initialize it with the supplied mappi…
    - `serialize(file, ops)` — Choose the configured or extension-derived serializer and write options to a text file.
    - `deserialize(file)` — Choose the configured or extension-derived serializer and read options from a text file.
    - `save()` — Serialize the current merged option dictionary back to the configuration file.
    - `load()` — Deserialize and return the raw configuration file contents.
    - `name()` — Return the configured `name`, falling back to the configuration filename when absent.
    - `opt_dict()` — Return loaded configuration values merged with runtime-only extra parameters.
    - `filter(keys, strict=True)` — Returns a filtered option dictionary according to keys.
    - `apply(func, strict=True)` — Applies func to stored parameters
    - `update(**kw)` — Merge keyword updates into the current option dictionary and persist the result.
    - `load_opts()` — Load the configuration once and add its containing directory as `config_location`.
    - `get_conf_attr(item)` — Read a value from the loaded configuration object using item or attribute access according to its s…
  - **class `ParameterManager`** (OptionsSet)
    - `serialize(file, mode=None)` — Write the managed options as a Python module configuration through `ModuleSerializer`.
    - `deserialize(file, mode=None, attribute=None)` — Load options from a Python module, optionally selecting an attribute.

### `Jobs.py` — A job management package to make it easier to instantiate
  - **class `Job`**
    > A job object to support simplified run scripting.
    > Provides a `job_data` checkpoint file that stores basic
    > data about job runtime and stuff, as well as a `logger` that
    > makes it easy to plug into a run time that supports logging
    - `__init__(job_dir, job_file=None, logger=None, parallelizer=None, job_parameters=None)`
    - `from_config(config_location=None, job_file=None, logger=None, parallelizer=None, job_parameters=None)` — Construct a job from configuration-compatible keyword arguments, using `config_location` as its dir…
    - `load_checkpoint(job_file)` — Loads the checkpoint we'll use to dump params
    - `load_logger(log_spec)` — Loads the appropriate logger
    - `load_parallelizer(par_spec)` — If something other than a dict is passed,
    - `path(*parts)` — :param parts:
    - `working_directory()` — Resolve a configured working directory relative to the job directory without permanently changing t…
  - **class `JobManager`** (PersistenceManager)
    > A class to manage job instances.
    > Thin layer on a `PersistenceManager`
    - `__init__(job_dir, job_type=None)`
    - `job(name, timestamp=False, **kw)` — Returns a loaded or new job with the given name and settings
    - `job_from_folder(folder, job_type=None, make_config=True, **opts)` — A special case convenience function that goes
    - `current_job(job_type=None, make_config=True, **opts)` — A special case convenience function that starts a

### `Logging.py`
  - **class `LogParser`** (FileStreamReader)
    > A parser that will take a log file and stream it as a series of blocks
    - `__init__(file, block_settings=None, binary=False, block_level_padding=None, **kwargs)`
    - `get_block_settings(block_level)` — Return syntax for a nesting level, extending the deepest known syntax with repeated padding when ne…
    - **class `LogBlockParser`**
      > A little holder class that allows block data to be parsed on demand
      - `__init__(block_data, parent, block_depth)`
      - `lines()` — Lazily parse and cache the records contained in this block.
      - `tag()` — Lazily parse and cache the block tag.
      - `block_iterator(opener, closer, preblock_handler=lambda c, w: w, postblock_handler=lambda e: e, start=0)` — Yield substrings delimited by opener and closer markers while allowing callbacks to adjust boundari…
      - `line_iterator(pattern='')` — Unfinished line-iteration stub; it computes the level prompt and then raises `NotImplementedError`.
      - `parse_prompt_blocks(chunk, prompt)` — Split a chunk into prompt-prefixed records and discard an initial empty segment.
      - `make_subblock(block)` — Wrap nested block text in a parser whose depth is one level deeper.
      - `parse_block_data()` — Separate nested blocks from prompt records, validate closers, extract the enclosing tag, and return…
      - `to_tree(tag_filter=None, depth=-1, combine_subtrees=True)` — Recursively convert a block to a tagged tree, optionally filtering nested tags and limiting depth.
    - `get_block(level=0, tag=None)` — :param level:
    - `get_line(level=0, tag=None)` — :param level:
    - `get_blocks(tag=None, level=0)` — Yield successive parsed blocks until `get_block` signals that the stream is exhausted.
    - `get_lines(tag=None, level=0)` — Yield successive prompt lines until `get_line` signals that the stream is exhausted.
    - `tag_match(tag, tag_filter)` — Test a tag against a regex string or pattern, predicate, or container-style filter.
    - `post_process_treelist(res, combine_subtrees=True)` — Collapse a singleton result and merge sibling dictionaries when their keys do not conflict.
    - `to_tree(tag_filter=None, depth=-1, combine_subtrees=True)` — Parse all top-level blocks into a `TreeWrapper`, applying tag filtering, recursion depth, and subtr…

### `ObjectBackers.py` — and make it easier to build more reliable,
  - **class `BaseObjectManager`**
    > Defines the basic parameters of an object interface
    > that can handle marshalling the core data behind
    > and object attribute to disk or vice versa
    - `__init__(obj)`
    - `get_basename()` — Build a storage basename from the object type and its `serialization_id` or runtime identity.
    - `basename()` — Lazily compute and cache the manager basename.
    - `save_attr(attr)` — Saves some attribute of the object
    - `load_attr(attr)` — Loads some attribute of the object
    - `del_attr(attr)` — Deletes some attribute of the object
  - **class `FileBackedObjectManager`** (BaseObjectManager)
    > Provides an interface to back an object with
    > a serializer
    - `__init__(obj, chk=None, loc=None, checkpoint_class=NumPyCheckpointer)`
    - `get_default_directory()` — Create or return the shared persistence location used for file-backed objects.
    - `basename()` — Get or set the explicit file tag used as the manager basename.
    - `basename(v)` — Get or set the explicit file tag used as the manager basename.
    - `get_basename()` — Build the default file tag from the managed object type and stable or runtime identity.
    - `save_attr(attr)` — Checkpoint an object attribute and return a marker describing the file-backed attribute.
    - `load_attr(attr)` — Load an attribute value from the backing checkpointer.
  - **class `FileBackedAttribute`**
    > A helper class to make it very clear that
    > an attribute is backed by a file on disk
    - `__init__(manager, attr)`

### `Persistence.py` — Provides utilities for managing object persistence.
  - **class `PersistenceLocation`**
    > An object that tracks a location to persist data
    > and whether or not that data should be cleaned up on
    > exit
    - `__init__(loc, name=None, delete=None)`
  - **class `PersistenceManager`**
    > Defines a manager that can load configuration data from a directory
    > or, maybe in the future, a SQL database or similar.
    > Requires class that supports `from_config` to load and `to_config` to save.
    - `__init__(cls, persistence_loc=None)`
    - `obj_loc(key)` — Construct the directory path for a persistent object key.
    - `load_config(key, make_new=False, init=None)` — Loads the config for the persistent structure named `key`
    - `new_config(key, init=None)` — Creates a new space and config for the persistent structure named `key`
    - `contains(key)` — Checks if `key` is a supported persistent structure
    - `load(key, make_new=False, strict=True, init=None)` — Loads the persistent structure named `key`
    - `save(obj)` — Saves requisite config data for a structure
  - **class `ResourceManager`**
    > A very simple framework for writing resources to a given directory
    > Designed to be extended and to support metadata
    - `__init__(name=None, location=None, write_metadata=False, temporary=None)`
    - `resolve_shared_directory()` — Return the user-local shared resource directory `~/.local`.
    - `get_default_base_location(temporary=None)` — Choose a new temporary directory or the shared user directory.
    - `get_base_location(temporary=True)` — Lazily resolve and cache the class base directory from an environment variable or default location.
    - `get_resource_path(*path)` — Join the base location, resource namespace, and optional subpath components.
    - `list_resources()` — Ensure the resource directory exists and map non-blacklisted entry names to their paths.
    - `save_resource(loc, val)` — Write a resource in binary, text, or JSON mode according to class flags.
    - `load_resource(loc)` — Read and decode a resource in binary, text, or JSON mode according to class flags.
    - `get_metadata_filename(name)` — Derive the sidecar metadata filename by appending `.meta.json`.
    - `get_resource_metadata(loc)` — Default metadata hook, currently returning an empty dictionary.
    - `get_resource_filename(name)` — Default filename hook, currently returning the resource name unchanged.
    - `get_resource(name, resource_function=None, load_resource=True)` — Return an existing resource, or generate and persist it with the configured factory before loading…

### `Serializers.py` — Provides scaffolding for creating serializers that dump data to a reloadable format.
  - **class `PseudoPickler`**
    > A simple plugin to work _like_ pickle, in that it should
    > hopefully support serializing arbitrary python objects, but which
    > doesn't attempt to put stuff down to a single `bytearray`, instead
    > supporting objects with `to_state` and `from_state` methods by converting
    > them to more primitive serializble types like arrays, strings, numbers,
    > etc.
    > Falls back to naive pickling when necessary.
    - `__init__(allow_pickle=False, protocol=1, b64encode=False)`
    - `to_state(obj, cache=None)` — Tries to extract state from `obj`, first through its `to_state`
    - `serialize(obj, cache=None)` — Serializes an object first by checking for a `to_state`
    - `deserialize(spec)` — Deserializes from an object spec, dispatching
  - **class `ConvertedData`**
    > Wrapper class for holding serialized data so we can be sure it's clean
    - `__init__(data, serializer)`
  - **class `BaseSerializer`**
    > Serializer base class to define the interface
    - `register(name, serializer=None)` — Register a serializer class under a name, either immediately or through decorator syntax.
    - `construct(serializer_type, **kwargs)` — Return an existing serializer or instantiate one resolved from a registry name or class.
    - `convert(data)` — Converts data into a serializable format
    - `deconvert(data)` — Converts data from a serialized format into a python format
    - `serialize(file, data, **kwargs)` — Writes the data
    - `dumps(data, **kwargs)` — Write data to a string
    - `deserialize(file, **kwargs)` — Loads data from a file
    - `loads(data, **kwargs)` — Write data to a string
  - **class `PicklingSerializer`** (BaseSerializer)
    > A serializer that makes dumping data to JSON simpler
    - `__init__(allow_pickle=True, pseudopickler=None)`
    - `convert(data)` — Pseudo-pickle arbitrary input and wrap the resulting payload as converted data.
    - `deconvert(data)` — Restore a pseudo-pickled payload to Python objects.
    - `serialize(file, data, **kwargs)` — Convert input when needed and write its binary payload to the file object.
    - `dumps(data, **kwargs)` — Return the converted binary pseudo-pickle payload directly.
    - `loads(data, key=None, **kwargs)` — Deserialize an in-memory payload and optionally select a nested key.
    - `deserialize(file, key=None, **kwargs)` — Read bytes from a file or path and delegate to `loads`.
  - **class `JSONSerializer`** (BaseSerializer)
    > A serializer that makes dumping data to JSON simpler
    - **class `BaseEncoder`** (json.JSONEncoder)
      - `__init__(*args, pseudopickler=None, allow_pickle=True, **kwargs)`
      - `default(obj)` — Convert NumPy arrays and scalars to JSON primitives, otherwise use the base encoder or pseudo-pickl…
    - `__init__(encoder=None, allow_pickle=True, pseudopickler=None)`
    - `convert(data)` — Encode data to a JSON string and mark it as converted.
    - `deconvert(data)` — Return decoded JSON data unchanged before optional pseudo-pickle restoration.
    - `serialize(file, data, **kwargs)` — JSON-encode input when needed and write the resulting text.
    - `dumps(data, **kwargs)` — Return the JSON text representation directly.
    - `loads(file, key=None, **kwargs)` — Decode JSON text and postprocess optional key selection and pseudo-pickled values.
    - `deserialize(file, key=None, **kwargs)` — Decode JSON from a file object and postprocess optional key selection and pseudo-pickled values.
  - **class `YAMLSerializer`** (BaseSerializer)
    > A serializer that makes dumping data to YAML simpler.
    > Doesn't support arbitrary python objects since that hasn't seemed like
    > a huge need yet...
    - `__init__()`
    - `convert(data)` — Wrap YAML-compatible data without structural conversion.
    - `deconvert(data)` — :param data: data to serialize, convert, or write
    - `serialize(file, data, **kwargs)` — Dump converted or raw data through the YAML API.
    - `deserialize(file, key=None, **kwargs)` — Load YAML data, deconvert it, and optionally select a nested slash-separated key.
  - **class `NDarrayMarshaller`**
    > Support class for `HDF5Serializer` and other
    > NumPy-friendly interfaces that marshalls data
    > to/from NumPy arrays
    - `__init__(base_serializer=None, allow_pickle=True, psuedopickler=None, allow_records=False, all_dicts=False, converters=None)`
    - `get_default_converters()` — Build the ordered type/duck-type dispatch table used to coerce values into NumPy-compatible forms.
    - `converter_dispatch()` — Return the custom converter mapping or create the default ordered dispatch table.
    - **class `_pickle_cache`**
      - `__init__(parent)`
      - `add(key)` — Record an object identity and raise `RecursionError` when conversion revisits an active object.
      - `pop()` — Remove the most recently tracked object identity.
    - `convert(data, allow_pickle=None)` — Recursively loop through, test data, make sure HDF5 compatible
    - `deconvert(data)` — Reverses the conversion process
  - **class `HDF5Serializer`** (BaseSerializer)
    > Defines a serializer that can prep/dump python data to HDF5.
    > To minimize complexity, we always use NumPy & Pseudopickle as an interface layer.
    > This restricts what we can serialize, but generally in insignificant ways.
    - `__init__(allow_pickle=True, psuedopickler=None, converters=None)`
    - `convert(data)` — Converts data into format that can be serialized easily
    - `serialize(file, data, **kwargs)` — Convert data, open an HDF5 file or group, and update either the `_data` dataset or a nested diction…
    - `deconvert(data)` — Converts an HDF5 Dataset into a NumPy array or Group into a dict
    - `deserialize(file, key=None, **kwargs)` — Open an HDF5 source, optionally select a nested object, and deconvert it to Python data.
  - **class `NumPySerializer`** (BaseSerializer)
    > A serializer that implements NPZ dumps
    - `get_default_converters()` — Build the ordered dispatch table for NumPy arrays, array-like objects, scalars, mappings, and seque…
    - `get_converters()` — Return the custom converter dispatch or the default converter mapping.
    - `convert(data)` — Recursively convert data and flatten nested dictionaries into separator-delimited NPZ keys.
    - `deconvert(data, sep=None)` — Unflattens nested dictionary structures so that the original data
    - `serialize(file, data, **kwargs)` — Write a single array with `np.save` or a flattened mapping with `np.savez`.
    - `deserialize(file, key=None, **kwargs)` — Load NumPy data, reconstruct nested structures, and optionally select a slash-separated key.
  - **class `ModuleSerializer`** (BaseSerializer)
    > A somewhat hacky serializer that supports module-based serialization.
    > Writes all module parameters to a dict with a given attribute.
    > Serialization doesn't support loading arbitrary python code, but deserialization does.
    > Use at your own risk.
    - `__init__(attr=None, loader=None)`
    - `loader()` — Lazily construct or return the module loader used for deserialization.
    - `attr()` — Return the configured module attribute or the default `config` name.
    - `convert(data)` — Wrap module configuration data without structural conversion.
    - `deconvert(data)` — Return the loaded module attribute unchanged.
    - `serialize(file, data, **kwargs)` — JSON-encode data and emit a Python assignment to the configured module attribute.
    - `deserialize(file, key=None, **kwargs)` — Execute/load the module, retrieve the configured attribute, and optionally select a nested key.
- `dictify_lists(tree)` — Recursively replace lists of dictionaries and ragged nested sequences with numbered dictionary entr…
- `disambiguate_tree(tree_obj, type_map=None, aliases=None)` — Assign stable key types across a nested tree, creating aliases when the same key name appears with…
- `flatten_tree(tree_obj, top_level=True, prep_tree=True, allow_pickle=False)` — Encode a nested dictionary as traversal metadata plus flattened value arrays and shape/sentinel str…
- `merge_trees(subtrees, top_level=True)` — Merge recursively flattened subtrees into shared key tables, traversal markers, shape streams, and…
- `undictify_lists(tree)` — Recursively reconstruct numbered dictionary encodings back into Python lists.
- `unflatten_tree(serial_tree, unprep_tree=True)` — Replay traversal markers and per-key shape/value pointers to rebuild the nested tree and restore li…
- `write_flat_tree(file, tree, flatten=None, allow_pickle=False, writer=None, **writer_options)` — Flatten a tree when needed and write metadata, shape streams, and value arrays to an NPZ-style writ…
- `read_flat_tree(file, unflatten=True, reader=None, allow_pickle=False, **reader_options)` — Read the NPZ-style flat-tree representation, rebuild its metadata structure, and optionally unflatt…
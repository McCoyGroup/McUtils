### `FileStreamer.py`
  - **class `FileStreamCheckPoint`**
    > A checkpoint for a file that can be returned to when parsing
    - `__init__(parent, revert=True)`
    - `disable()` — Disable automatic restoration when the checkpoint context exits.
    - `enable()` — Enable automatic restoration when the checkpoint context exits.
    - `revert()` — Seek the parent reader back to the offset captured when this checkpoint was created.
  - **class `FileStreamReaderException`** (IOError)
  - **class `SearchStream`**
    > Represents a stream from which we can pull block of data.
    > Just provides a core interface with which we can work
    - `read(n=-1)` — Define the interface for reading up to `n` units from the current stream position.
    - `rread(n=-1)` — Read the `n` units immediately preceding the current position, leaving the stream positioned at the…
    - `readline()` — Define the interface for reading one line from the stream.
    - `seek(*args, **kwargs)` — Define the interface for repositioning the stream.
    - `tell()` — Define the interface for reporting the current stream offset.
    - `find(tag, start=None, end=None)` — Define the interface for locating the first occurrence of a tag within optional bounds.
    - `rfind(tag, start=None, end=None)` — Define the interface for locating the last occurrence of a tag within optional bounds.
    - `tag_size(tag)` — Define the interface for measuring a tag in the stream's native units.
  - **class `ByteSearchStream`** (SearchStream)
    > A stream that is implemented for searching in byte strings
    - `__init__(data, encoding='utf-8', **kw)`
    - `read(n=-1)` — Read bytes from the active buffer and decode them with the configured encoding.
    - `readline()` — Read one byte line and decode it with the configured encoding.
    - `seek(*args, **kwargs)` — Move the active byte-buffer cursor using `BytesIO.seek` semantics.
    - `tell()` — Return the active byte-buffer cursor offset.
    - `encode_tag(tag)` — Convert a text tag to bytes using the configured encoding, leaving byte tags unchanged.
    - `find(tag, start=None, end=None)` — Search the stored bytes forward for a tag, defaulting to the current cursor as the lower bound.
    - `rfind(tag, start=None, end=None)` — Search the stored bytes backward for a tag, defaulting to the current cursor as the upper bound.
    - `tag_size(tag)` — Return the encoded byte length of a search tag.
  - **class `FileSearchStream`** (SearchStream)
    > A stream that is implemented for searching in mmap-ed files
    - `__init__(file, mode='r', binary=None, encoding='utf-8', check_decoding=False, decoding_mode='strict', **kw)`
    - `handle_chunk(chunk)` — Decode byte chunks with the configured encoding and error mode, optionally converting decode failur…
    - `read(n=-1)` — Read from the memory map and decode the returned chunk.
    - `readline()` — Read one line from the memory map and decode it.
    - `seek(*args, **kwargs)` — :param args: positional arguments forwarded to the wrapped callable
    - `tell()` — **LLM Docstring**
    - `find(tag, start=None, end=None)` — Find the next encoded tag in the memory map, starting at the current cursor unless bounds are suppl…
    - `rfind(tag, start=None, end=None)` — Find the previous encoded tag in the memory map, ending at the current cursor unless bounds are sup…
    - `tag_size(tag)` — Return the byte length of a tag encoded with this stream's encoding.
  - **class `StringSearchStream`** (SearchStream)
    > A stream that is implemented for searching in strings.
    > Current implementation creates a `StringIO` buffer to support `read`/`tell`/etc.
    > This is very memory inefficient, but we're not winning performance awards for
    > any of this anyway
    - `__init__(string)`
    - `read(n=-1)` — Read characters from the active string cursor.
    - `readline()` — Read one line from the active string cursor.
    - `seek(*args, **kwargs)` — :param args: positional arguments forwarded to the wrapped callable
    - `tell()` — **LLM Docstring**
    - `find(tag, start=None, end=None)` — Find the next tag in the original string, beginning at the current cursor by default.
    - `rfind(tag, start=None, end=None)` — Find the previous tag in the original string, ending at the current cursor by default.
    - `tag_size(tag)` — Return the number of characters in a tag.
  - **class `SearchStreamReader`**
    > Represents a reader which implements finding chunks of data in a stream
    - `__init__(stream)`
    - **class `StreamSearchDirection`** (enum.Enum)
    - `find_tag(tag, skip_tag=None, seek=None, allow_terminal=False, validator=None, return_body=False, direction='forward')` — Finds a tag in a file
    - **class `TagSentinels`** (enum.Enum)
    - `get_tagged_block(tag_start, tag_end, validator=None, tag_validator=None, allow_terminal=False, expand_until_valid=None, return_tag=False, return_end_points=False, direction='forward', block_size=500)` — Pulls the string between tag_start and tag_end
    - `parse_key_block(tag_start=None, tag_end=None, mode='Single', validator=None, tag_validator=None, expand_until_valid=False, preserve_tag=False, return_end_points=False, parser=None, parse_mode='List', num=None, pass_context=False, allow_terminal=False, direction='forward', **ignore)` — Parses a block by starting at tag_start and looking for tag_end and parsing what's in between them
    - `read(n=1)` — :param n: the requested count or fixed repetition count
    - `readline()` — Read one line from the wrapped stream.
    - `seek(*args, **kwargs)` — :param args: positional arguments forwarded to the wrapped callable
    - `tell()` — Return the wrapped stream's current offset.
    - `find(tag)` — Find a tag in the wrapped stream using its native search operation.
    - `rfind(tag, search_window=None)` — Find a preceding tag, using the stream's reverse search when available or a bounded read-and-search…
    - `skip_tag(tag)` — Call the wrapped stream's `skip_tag` operation; the supplied stream implementations do not define t…
    - `rskip_tag(tag)` — Call the wrapped stream's `rskip_tag` operation; the supplied stream implementations do not define…
  - **class `FileStreamReader`** (SearchStreamReader)
    > Represents a file from which we'll stream blocks of data by finding tags and parsing what's between them
    - `__init__(file, mode='r', encoding='utf-8', **kw)`
  - **class `StringStreamReader`** (SearchStreamReader)
    > Represents a string from which we'll stream blocks of data by finding tags and parsing what's between them
    - `__init__(string)`
  - **class `ByteStreamReader`** (SearchStreamReader)
    > Represents a string from which we'll stream blocks of data by finding tags and parsing what's between them
    - `__init__(string, encoding='utf-8', **kw)`
  - **class `FileStreamerTag`**
    - `__init__(tag_alternatives=None, follow_ups=None, offset=None, direction='forward', skip_tag=True, seek=True)`
  - **class `LineByLineParser`**
    - `__init__(stream, binary=True, encoding='utf-8', max_nesting_depth=-1, ignore_comments=False)`
    - `check_tag(line, depth=0, active_tag=None, label=None, history=None)` — Classify a line as a block boundary, value, comment, skip, or other parser tag; subclasses must imp…
    - `handle_block_line(label, line, depth=0, history=None)` — Return a line unchanged before it is added to the current block; subclasses may transform it.
    - `handle_block(label, block, depth=0)` — Return an accumulated block unchanged; subclasses may convert it to another representation.
    - **class `LineReaderTags`** (enum.Enum)
      > Real access pattern: LineReaderTags.<MemberName> (this is an enum with 7 members, e.g. LineReaderTags.RESETTING_BLOCK_END == 'implict_end'). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:
    - `read_stream_line(binary=None)` — Read the next iterated line and decode it when text mode is requested.
    - `stream_iter(binary=None)` — Yield every line from the underlying stream, decoding byte lines exactly once when operating in tex…
    - `find_next_block(binary=None, ignore_comments=None, max_nesting_depth=None, aggregate_values=True, depth=0)` — Consume lines until a logical block ends, recursively parse nested blocks, optionally discard comme…
  - **class `FileLineByLineReader`** (LineByLineParser)
    > Represents a file from which we'll stream blocks of data by finding tags and parsing what's between them
    - `__init__(file, mode='r', binary=False, encoding='utf-8', ignore_comments=False, max_nesting_depth=-1, **kw)`
  - **class `StringLineByLineReader`** (LineByLineParser)
    > Represents a string from which we'll stream blocks of data by finding tags and parsing what's between them
    - `__init__(string, ignore_comments=False, max_nesting_depth=-1)`
  - **class `ByteLineByLineReader`** (LineByLineParser)
    > Represents a string from which we'll stream blocks of data by finding tags and parsing what's between them
    - `__init__(string, encoding='utf-8', ignore_comments=False, max_nesting_depth=-1, **kw)`

### `RegexPatterns.py` — Simple utilities that support constructing Regex patterns
  - **class `RegexPattern`**
    > Represents a combinator structure for building more complex regexes
    > *(truncated — see stub for full docstring)*
    - `__init__(pat, name=None, children=None, parents=None, dtype=None, repetitions=None, key=None, joiner='', join_function=None, wrapper_function=None, suffix=None, prefix=None, parser=None, handler=None, default_value=None, capturing=None, allow_inner_captures=False, escape=True)`
    - `pat()` — Return or replace the primitive pattern/wrapper used by this node; setting it invalidates all compi…
    - `pat(pat)` — Return or replace the primitive pattern/wrapper used by this node; setting it invalidates all compi…
    - `children()` — :return:
    - `child_count()` — :return:
    - `child_map()` — Returns the map to subregexes for named regex components
    - `parents()` — :return:
    - `joiner()` — :return:
    - `joiner(j)` — Return or replace the separator placed between built child patterns; setting it invalidates the pat…
    - `join_function()` — :return:
    - `join_function(j)` — Return or replace the callable that combines the joiner and built children; setting it invalidates…
    - `suffix()` — :return:
    - `suffix(e)` — Return or replace the suffix appended after the combined children; setting it invalidates the patte…
    - `prefix()` — :return:
    - `prefix(s)` — Return or replace the prefix prepended before the combined children; setting it invalidates the pat…
    - `dtype()` — Returns the StructuredType for the matched object
    - `is_repeating()` — Report whether repetition metadata is stored as a `(minimum, maximum)` tuple.
    - `capturing()` — Report whether this node captures directly, including the implicit case where a repeating node cont…
    - `capturing(cap)` — Report whether this node captures directly, including the implicit case where a repeating node cont…
    - `get_capturing_groups(allow_inners=None)` — We walk down the tree to find the children with capturing groups in them and
    - `captures()` — Subtly different from capturing n that it will tell us if we need to use the group in post-processi…
    - `capturing_groups()` — Returns the capturing children for the pattern
    - `named_groups()` — Returns the named children for the pattern
    - `combine(other, *args, **kwargs)` — Combines self and other
    - `wrap(*args, **kwargs)` — Applies wrapper function
    - `build(joiner=None, prefix=None, suffix=None, recompile=True, no_captures=False, verbose=False)` — Recursively build the regex text for this node, suppressing inner captures when an outer node captu…
    - `compiled()` — Compile and cache the regex string returned by `build`.
    - `add_parent(parent)` — Register an ancestor that must be invalidated when this node changes.
    - `remove_parent(parent)` — :param parent: the parent reader or regex node
    - `add_child(child)` — Append one child, update named/capturing-descendant flags, and invalidate this node and its ancesto…
    - `add_children(children)` — Append several children, merge their named/capturing-descendant flags, and invalidate caches.
    - `remove_child(child)` — Remove one child, recompute descendant flags from the remaining children, and invalidate caches.
    - `insert_child(index, child)` — Insert a child at a specific position and invalidate cached pattern state.
    - `invalidate_cache()` — Clear built-string, compiled-regex, and capturing-group caches, then recursively invalidate all par…
    - `match(txt, *args)` — Match the compiled pattern only at the beginning of the input.
    - `fullmatch(txt, *args)` — Require the compiled pattern to match the complete input.
    - `search(txt, *args)` — Find the first occurrence of the compiled pattern in the input.
    - `findall(txt, *args)` — Return all non-overlapping matches of the compiled pattern.
    - `finditer(txt, *args)` — Iterate over match objects for all non-overlapping matches.
    - `sub(rep, txt, *args)` — :param rep: the replacement string or callable
    - `subn(rep, txt, *args)` — Replace matches and return both the resulting text and replacement count.
    - `replace(txt, replacement, *args)` — Replace matches with a supplied replacement string or callable.
    - `remove(txt, *args)` — Delete every match by replacing it with an empty string.
- `is_grouped(p)` — Takes a string pattern and tries to check if it's already in a singular construct (usually grouped.…
- `group(p, no_capture=False)` — Wrap a pattern in a capturing group, or in a non-capturing group when `no_capture` is true.
- `non_capturing(p, *a, **kw)` — Wrap a pattern in a `(?:...)` group.
- `optional(p, no_capture=False)` — Apply `?` to an already grouped atom, otherwise first place the pattern in a non-capturing group.
- `alternatives(p, no_capture=False)` — Ensure an alternation expression is grouped, choosing capturing or non-capturing grouping from `no_…
- `shortest(p, no_capture=False)` — Convert a pattern to a lazy zero-or-more expression, or make an existing `*`/`+` quantifier lazy.
- `repeating(p, min=1, max=None, no_capture=False)` — Apply `*`, `+`, `{n}`, `{n,}`, or `{n,m}` according to the supplied bounds, then capture the entire…
- `duplicated(p, num, riffle='', no_capture=False)` — Repeat the same pattern exactly `num` times with `riffle` inserted between copies.
- `named(p, n, no_capture=False)` — Wrap a pattern in a Python named capture, or suppress the named capture when `no_capture` is true.
- `opnb_p(p, no_capture=False)` — Wrap a pattern in an optional non-capturing group.
- `wrap_repeats(self, min=None, max=None, no_capture=None)` — Store repetition bounds on a `RegexPattern` when the `Repeating` wrapper is applied.
- `wrap_name(self, n)` — Assign a capture key and, when unnamed, use that key as the node's descriptive name.
- `wrap_duplicate_type(self, n, riffle='')` — Update the node's declared dtype shape to prepend the fixed duplication count.

### `StringParser.py`
  - **class `StringParserException`** (Exception)
  - **class `StringParser`**
    > A convenience class that makes it easy to pull blocks out of strings and whatnot
    - `__init__(regex)`
    - `parse(txt, regex=None, block_handlers=None, dtypes=None, out=None)` — Finds a single match for the and applies parsers for the specified regex in txt
    - `parse_all(txt, regex=None, num_results=None, block_handlers=None, dtypes=None, out=None)` — Find all non-overlapping matches, allocate or reuse typed result storage, add a result axis for new…
    - **class `MatchIterator`**
      - **class `Match`**
        - `__init__(parent, block)`
        - `value()` — Allocate typed result storage and parse this match into it on demand.
      - `__init__(parser, match_iter, num_results, dtypes, block_handlers)`
    - `parse_iter(txt, regex=None, num_results=None, block_handlers=None, dtypes=None)` — Create a lazy iterator over matches, carrying the inferred dtypes and block handlers needed to pars…
    - `get_regex_block_handlers(regex)` — Uses the uncompiled RegexPattern to determine what blocks exist and what handlers they should use
    - `get_regex_dtypes(regex)` — Uses the uncompiled RegexPattern to determine which StructuredTypes to return
    - `handler_method(method)` — Turns a regular function into a handler method by adding in (and ignoring) the array argument
    - `load_array(data, dtype='float')` — Parse whitespace-delimited text into a NumPy array with `numpy.loadtxt`.
    - `to_array(data, array=None, append=False, dtype='float', shape=None, pre=None)` — A method to take a string or iterable of strings and quickly dump it to a NumPy array of the right…
    - `array_handler(array=None, append=False, dtype='float', shape=None, pre=None)` — Returns a handler that uses to_array

### `StructuredType.py`
  - **class `StructuredType`**
    > Represents a structured type with a defined calculus to simplify the construction of combined types when writing
    > parsers that take multi-typed data
    > *(truncated — see stub for full docstring)*
    - `__init__(base_type, shape=None, is_alternative=False, is_optional=False, default_value=None)`
    - `is_simple()` — Report whether the specification is an unqualified primitive type (or `None`) rather than an option…
    - `add_types(other)` — Constructs a new type by treating the two objects as siblings, that is if they can be merged due to…
    - `compound_types(other)` — Creates a structured type where rather than merging types they simply compound onto one another
    - `repeat(n=None, m=None)` — Returns a new version of the type, but with the appropriate shape for being repeated n-to-m times
    - `drop_axis(axis=0)` — Returns a new version of the type, but with the appropriate shape for dropping an axis
    - `extend_shape(base_shape)` — Extends the shape of the type such that base_shape precedes the existing shape
  - **class `DisappearingTypeClass`** (StructuredType)
    > A special type that is entirely ignored in the structured type algebra
    - `__init__()`
  - **class `StructuredTypeArray`**
    > Represents an array of objects defined by the StructuredType spec provided
    > mostly useful as it dispatches to NumPy where things are simple enough to do so
    > *(truncated — see stub for full docstring)*
    - `__init__(stype, num_elements=50, padding_mode='fill', padding_value=None)`
    - `is_simple()` — Just returns wheter the core datatype is simple
    - `dict_like()` — Report whether compound storage is keyed by a dictionary or `OrderedDict`.
    - `extension_axis()` — Determines which axis to extend when adding more memory to the array
    - `extension_axis(ax)` — Get or set the axis used for growth; when unset, choose the first indeterminate axis, falling back…
    - `shape()` — Get the filled shape of simple storage or the component shapes of compound storage; the setter stor…
    - `shape(s)` — Get the filled shape of simple storage or the component shapes of compound storage; the setter stor…
    - `block_size()` — Return the number of scalar values in one element along the extension axis, summing component block…
    - `append_depth()` — Get or set recursive append depth; changing it propagates the same increment to all compound subarr…
    - `append_depth(d)` — Get or set recursive append depth; changing it propagates the same increment to all compound subarr…
    - `dtype()` — Returns the core data type held by the StructuredType that represents the array
    - `stype()` — Returns the StructuredType that the array holds data for
    - `array()` — Return the filled slice of simple NumPy storage, or the complete tuple/mapping of compound subarray…
    - `axis_shape_indeterminate(axis)` — Tries to determine if an axis has had any data placed into it or otherwise been given a determined…
    - `has_indeterminate_shape()` — Tries to determine if the entire array has a determined shape
    - `filled_to()` — Get per-axis populated extents for simple storage or nested extents for compound storage; setting a…
    - `filled_to(filling)` — Get per-axis populated extents for simple storage or nested extents for compound storage; setting a…
    - `set_filling(amt, axis=0)` — Set one populated extent directly, propagating the update through compound children.
    - `increment_filling(inc=1, axis=0)` — Increase one populated extent, propagating the increment through compound children.
    - `empty_array(shape=None, num_elements=None)` — Creates empty arrays with (potentially) default elements
    - `extend_array(axis=None)` — Grow storage by concatenating an equally shaped empty block along the extension axis, recursively g…
    - `set_part(key, value)` — Recursively sets parts of an array if not simple, otherwise just delegates to NumPy
    - `get_part(item, use_full_array=True)` — If simple, delegates to NumPy, otherwise tries to recursively get parts...?
    - `add_axis(which=0, num_elements=None, change_shape=True)` — Adds an axis to the array, generally used for expanding from singular or 1D data to higher dimensio…
    - `can_cast(val)` — Determines whether val can probably be cast to the right return type and shape without further proc…
    - `append(val, axis=0)` — Puts val in the first empty slot in the array
    - `extend(val, single=True, prepend=False, axis=None)` — Adds the sequence val to the array
    - `fill(array)` — Sets the result array to be the passed array
    - `cast_to_array(txt)` — Casts a string of things with a given data type to an array of that type and does some optional
  - **class `StructuredTypeArrayException`** (Exception)

### `TeXParser.py`
  - **class `TeXParser`** (Parsers.FileStreamReader)
    - `is_valid_tex_block(block)` — Accept a TeX call block when unescaped opening braces are exactly one fewer than closing braces, ma…
    - `is_valid_stream_start(tag_str)` — Accept a candidate command tag when it has a non-empty body and balanced square brackets.
    - `parse_tex_call(allowed_calls=None, return_end_points=False)` — Locate an allowed TeX command, read its balanced braced argument, then consume and concatenate any…
    - `parse_tex_environment(allowed_environments=None, return_end_points=False)` — Extract a complete TeX environment, restricted to selected names when requested, validating nested…
  - **class `BibItemParser`** (Parsers.FileStreamReader)
    - `is_valid_tex_block(block)` — Accept a BibTeX field value when escaped braces are ignored and the remaining braces are balanced.
    - `is_valid_key_block(block)` — Accept text consisting of optional whitespace, a word-like field name, optional whitespace, and `=`.
    - `parse_header(return_end_points=False)` — Parse the `@type{citation_key,` prefix of one BibTeX entry and return the entry type and citation k…
    - `parse_bib_line(allowed_fields=None, return_end_points=False)` — Parse one `field = value` assignment, searching backward to find the field name when unrestricted a…
  - **class `BibTeXParser`** (Parsers.FileStreamReader)
    - `is_valid_tex_block(block)` — Accept a BibTeX entry block when the consumed opening brace leaves one more closing brace than open…
    - `is_valid_stream_start(tag_str)` — Compile the entry-start pattern once and full-match candidate strings such as `@article{`.
    - `parse_bib_item(allowed_items=None, return_end_points=False)` — Extract one complete balanced BibTeX entry, optionally restricting the accepted entry types and ret…
    - `parse_bib_body(text, allowed_fields=None, parse_lines=True)` — Parse an entry string into its type, citation key, header endpoints, and a mapping from field names…

### `XYZParser.py`
  - **class `XYZParser`** (FileLineByLineReader)
    - `__init__(*args, **kwds)`
    - `check_tag(line, depth=0, active_tag=None, label=None, history=None)`
    - `handle_block(label, block_data, join=True, depth=0, number_pattern=None, label_pattern=None, simple_format=False)`
    - `parse(max_blocks=None)`
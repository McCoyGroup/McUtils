### `Conveniences.py`
- `format_tensor_element_table(inds, vals, headers=('Indices', 'Value'), format='{:8.3f}', column_join='|', index_format='{:>5.0f}', **etc)` — Combine transposed index arrays with one or more value columns and format them under spanning heade…
- `format_symmetric_tensor_elements(tensor, symmetries=None, cutoff=1e-06, headers=('Indices', 'Value'), allowed_indices=None, filter=None, format='{:12.3f}', **etc)` — Select entries above a cutoff, retain one ordered representative per declared symmetry, apply optio…
- `format_mode_labels(labels, freqs=None, high_to_low=True, mode_index_format='{:.0f}', frequency_format='{:.0f}', headers=None, column_join=' | ', none_tag='mixed', **etc)` — Render one-based mode numbers with normalized label text and optional frequencies, optionally rever…
- `format_zmatrix(zm, preserve_embedding=True, preserve_indices=True, list_form=True)` — Format Z-matrix index rows with width chosen from the largest index and optionally remove embedding…
- `format_state_vector_frequency_table(state_list, freq_data, state_header='State', freq_header='Freq.', freq_fmt='{:.3f}', sep=' | ', join=' ')` — Join state-vector columns with one or more frequency columns under spanning headers.
- `format_radix_value(duration, target_format, variable_map, format_variables=None)` — Successively divide a duration by named unit sizes and interpolate quotient components plus the fin…
- `format_elapsed_time(duration, target_format='{hours:d}:{minutes:02d}:{seconds:02d}', format_variables=None)` — Convert a numeric or `timedelta` duration to seconds and format it through the configured year/day/…

### `FileMatcher.py`
  - **class `StringMatcher`**
    > Defines a simple filter that applies to a file and determines whether or not it matches the pattern
    - `__init__(match_patterns, negative_match=False)`
    - `matches(f)` — Evaluate the configured matcher against the input and apply optional negation.
  - **class `MatchList`** (StringMatcher)
    > Defines a set of matches that must be matched directly (uses `set` to make this basically a constant time check)
    - `__init__(*matches, negative_match=False)`
    - `test_match(f)` — Test constant-time membership in the stored literal match set.
  - **class `FileMatcher`** (StringMatcher)
    > Defines a filter that uses StringMatcher to specifically match files
    - `__init__(match_patterns, negative_match=False, use_basename=False)`
    - `matches(f)` — Evaluate the configured matcher against the input and apply optional negation.

### `TableFormatters.py` — Just a simple text table formatter with support for headers, separators, any kind of python formatt…
  - **class `TableFormatter`**
    - `__init__(column_formats, *, headers=None, header_spans=None, header_format=None, column_join=None, row_join=None, header_column_join=None, header_row_join=None, separator=None, separator_lines=1, content_join=None, column_alignments=None, header_alignments=None, row_padding=None)`
    - `prep_input_arrays(headers, data, header_spans)` — Normalize headers, spans, and rows to rectangular lists with a shared maximum column count.
    - `custom_formatter(f)` — Convert format strings, iterable-format specifications, or callables into objects exposing a `.form…
    - `resolve_formatters(ncols, col_formats)` — Repeat the supplied formatter sequence cyclically and truncate it to the requested column count.
    - `prep_formatters(formats)` — Normalize one or more format specifications through `custom_formatter`.
    - `format_tablular_data_columns(data, formats, row_padding=None, strict=False)` — Format row-major data into column-major strings, optionally padding the first column of each row.
    - `align_left(col, width)` — Pad each string in a column using left alignment to the requested width.
    - `align_right(col, width)` — Pad each string in a column using right alignment to the requested width.
    - `align_center(col, width)` — Pad each string in a column using center alignment to the requested width.
    - `align_dot(col, width, dot='.')` — Align strings by their final decimal marker, pad missing fractional widths, and right-align the res…
    - `resolve_aligner(alignment)`
    - `align_column(header_data, cols_data, header_alignment, column_alignment, join_widths, header_widths)` — Jointly size a grouped header and its body columns while accounting for inter-column join widths.
    - `format(headers_or_table, *table_data, header_format=None, header_spans=None, column_formats=None, column_alignments=None, header_alignments=None, column_join=None, row_join=None, header_column_join=None, header_row_join=None, separator=None, separator_lines=None, content_join=None, row_padding=None, strict=False)` — Assemble formatted headers, spanning groups, aligned body columns, separators, and joins into one t…
    - `extract_tree_headers(tree, key_normalizer=None, depth=0, default_key=None, terminal_data_function=None)` — Recursively derive hierarchical header rows, span metadata, and a tabular leaf array from a nested…
    - `from_tree(tree_data, header_spans=None, key_normalizer=None, depth=0, default_key=None, column_formats=None, header_normalization_function=None, header_function=None, terminal_data_function=None, **opts)` — Construct a formatter and leaf-data array from nested tree data, with optional header transformatio…
    - `format_tree(tree_data, data_normalization_function=None, **opts)` — Extract and optionally normalize tree data, then return its formatted table text.

### `TeXWriter.py`
  - **class `TeXWriter`**
    - `format_tex(context=None)` — Abstract formatting hook that subclasses must implement to produce TeX source.
    - `dispatch_format(b, context)` — Convert supported Python, NumPy, and `TeXWriter` values into TeX-ready text using type-directed dis…
    - `as_expr()` — Wrap this writer as a symbolic `TeXExpr` so arithmetic and comparison composition can be used.
  - **class `TeXContextManager`**
    - `resolve(name='default')` — Return the weakly cached named context manager, creating it when no live manager exists.
    - `__init__()`
    - `subcontext(cls)` — Instantiate a context class bound to this manager.
    - `set_context(ctx)` — Push a context onto the active-context stack.
    - `leave_context()` — Pop the most recently entered context.
    - `context()` — Return the currently active context, or `None` when the stack is empty.
    - `math_mode()` — Report whether the current context is a `MathContext`.
  - **class `TeXContext`**
    - `__init__(manager)`
  - **class `MathContext`** (TeXContext)
  - **class `TeXBlock`** (TeXWriter)
    > Real access pattern: TeXBlock.<AttrName> (6 class attributes, e.g. TeXBlock.tag == None). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:
    - `__init__(body=None, *, tag=None, modifier=None, modifier_type=None, separator=None, context=None, label=None)`
    - `prep_body(context=None)` — Format each body element, append a normalized `\label{...}` when requested, and return the body fra…
    - `construct_modified_tag(tag, mod, mod_type='[]')` — Build matching `\begin` and `\end` strings, inserting one or more delimited modifiers after the ope…
    - `construct_header_footer()` — Construct this block’s environment opener and closer from its configured tag and modifier.
    - `format_body(body_params)` — Wrap formatted body fragments in the environment tags, when a tag is configured, and join them with…
    - `format_tex(context=None)` — Format a block, entering its requested context while preparing the body and then emitting the envir…
  - **class `TeXRow`** (TeXBlock)
  - **class `TeXArray`** (TeXBlock)
    > Real access pattern: TeXArray.<AttrName> (9 class attributes, e.g. TeXArray.tag == 'tabular'). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:
    - `__init__(headers_or_body, body=None, *, alignment='auto', number_format='{:8.3f}', content_join=None, column_join=None, row_join=None, separator=None, header_spans=None, header_alignments=None, resizeable=False, **opts)`
    - `construct_alignment_spec(body)` — Infer one TeX alignment code per column, using centered columns for nonnumeric content and right al…
    - `construct_header_footer()` — Build the `tabular` or `tabularx` delimiters, inferred alignment specification, and horizontal-rule…
    - `format_numpy_array(array)` — Render a numeric array with `numpy.savetxt`, choosing field width from the largest magnitude and co…
    - `format_mixed_array(array, context=None)` — Render heterogeneous rows after TeX-dispatching each cell and left-padding cells to common per-colu…
    - `prep_body(context=None, headers=None, body=None)` — Normalize optional headers, multicolumn spans, and column formatters, then delegate table layout to…
  - **class `TeXTable`** (TeXBlock)
    - `__init__(headers_or_body, body=None, width=1, caption=None, resizeable=False, number_format=None, header_spans=None, **etc)`
    - `prep_body(context=None, body=None)` — Wrap the table content in a centered minipage and append optional caption and label commands.
  - **class `TeXFunction`** (TeXWriter)
    - `__init__(*args, function_name=None)`
    - `format_tex(context=None)` — Emit a TeX command followed by each dispatched argument enclosed in braces.
  - **class `TeXMulticolumn`** (TeXFunction)
    - `__init__(width, fmt, body)`
  - **class `TeXBold`** (TeXFunction)
  - **class `TeXBracketed`** (TeXWriter)
    - `__init__(body, brackets=None)`
    - `format_tex(context=None)` — Dispatch the wrapped body and surround it with the configured TeX delimiters.
  - **class `TeXParenthesized`** (TeXBracketed)
  - **class `TeXEquation`** (TeXBlock)
  - **class `TeXNode`** (Abstract.Expr)
    - `to_ast()` — Reject AST conversion because TeX-only symbolic nodes are formatting constructs, not executable exp…
  - **class `TeXSuperscript`** (TeXNode)
    - `__init__(obj, index)`
  - **class `TeXApply`** (TeXNode)
    - `__init__(function, argument)`
  - **class `TeXSymbol`** (Abstract.Name)
  - **class `TeXExpr`** (TeXWriter)
    - `name(s)` — Normalize multi-character names to TeX control sequences and wrap them as a symbolic TeX expression.
    - `symbol(s)` — Normalize multi-character names to TeX control sequences and wrap them as a symbolic TeX expression.
    - `__init__(body)`
    - `Equals(other)` — Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating t…
    - `LessThan(other)` — Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating t…
    - `LessEquals(other)` — Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating t…
    - `GreaterThan(other)` — Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating t…
    - `GreaterEquals(other)` — Build and return a new `TeXExpr` containing the corresponding symbolic operation without mutating t…
    - `convert_name(name, converter)` — Convert a symbolic name node into its TeX string representation using the recursive converter.
    - `convert_const(const, converter)` — Convert a symbolic const node into its TeX string representation using the recursive converter.
    - `convert_call(call, converter)` — Convert a symbolic call node into its TeX string representation using the recursive converter.
    - `convert_superscript(op, converter)` — Convert a symbolic superscript node into its TeX string representation using the recursive converte…
    - `convert_bitxor(op, converter)` — Convert a symbolic bitxor node into its TeX string representation using the recursive converter.
    - `convert_power(op, converter)` — Convert a symbolic power node into its TeX string representation using the recursive converter.
    - `convert_subscript(op, converter)` — Convert a symbolic subscript node into its TeX string representation using the recursive converter.
    - `convert_add(op, converter)` — Convert a symbolic add node into its TeX string representation using the recursive converter.
    - `convert_sub(op, converter)` — Convert a symbolic sub node into its TeX string representation using the recursive converter.
    - `convert_mul(op, converter)` — Convert a symbolic mul node into its TeX string representation using the recursive converter.
    - `convert_bitor(op, converter)` — Convert a symbolic bitor node into its TeX string representation using the recursive converter.
    - `convert_div(op, converter)` — Convert a symbolic div node into its TeX string representation using the recursive converter.
    - `convert_eq(op, converter)` — Convert a symbolic eq node into its TeX string representation using the recursive converter.
    - `convert_raw(obj, converter)` — Convert a symbolic raw node into its TeX string representation using the recursive converter.
    - `converter_dispatch()` — Return the mapping from symbolic node tags to TeX conversion functions, including a raw fallback.
    - `format_tex(context=None)` — Transmogrify the symbolic expression through TeX converters and add dollar delimiters only outside…
  - **class `TeX`**
    > Namespace for TeX-related utilities, someday might help with document prep from templates
    - `Matrix(mat, **kwargs)` — Construct a TeX array from the matrix and wrap it in scalable parentheses.
  - **class `TeXImportGraph`**
    - `__init__(tex_root, root_dir=None, head_parser=None, import_heads=None, strip_comments=True, aliases=None, ignored_files=None, **parser_options)`
    - `import_parser(head, tag)` — Extract the argument following an import-like command, normalize it to a `.tex` filename, and retur…
    - `head_resolver(tag)` — Extract a TeX command head by removing the leading backslash and truncating before optional or requ…
    - `load_module_parser(tag)` — Resolve a module command to `sections/<module>/main.tex` and record the module directory as the new…
    - `load_block_parser(head, root, tag)` — Resolve a `load*` command under its resource root and inject a label header for non-figure/table/eq…
    - `resolve_parser(head)` — Select the path parser for an import-like TeX command head.
    - `strip_tex_comments(body)` — Remove full-line and unescaped trailing percent comments from TeX source.
    - `find_imports(root=None, import_heads=None, root_dir=None)` — Parse one TeX file for configured import commands, optionally through a comment-stripped temporary…
    - `populate_graph(import_heads=None, root_dir=None)` — Breadth/depth traverse reachable TeX imports, skip missing files, and memoize the resulting adjacen…
  - **class `TeXTranspiler`**
    - `__init__(tex_root, root_dir=None, figure_renaming_function=None, bib_renaming_function=None, strip_comments=True, figures_path=None, figure_merge_function=None, bib_path=None, bib_merge_function=None, bib_cleanup_function=None, citation_renaming_function=None, aliases=None, styles_path=None, parser_options=None)`
    - `figure_counter(name_root='Figure', start_at=1)` — Create a stateful renamer that assigns sequential names while preserving each figure extension.
    - `add_bibs(bib_list)` — Concatenate bibliography files into a persistent temporary file and mark it for later deletion.
    - `pruned_bib(bib_file_or_filter, cites=None, *, filter=None, **parser_options)` — Filter a BibTeX file in place to entries referenced by the supplied citation map, or return a confi…
    - `get_injection_body(root_dir, node_data, body)` — Resolve and return the requested derived value from the object’s current configuration.
    - `apply_body_edit(cur_text, edits, normalization_function=None)` — Apply endpoint-based replacements in source order while accounting for text already consumed from t…
    - `flatten_import_graph(graph, root, cache=None, root_dir=None, strip_comments=False)` — Recursively inline imported TeX files, memoizing results and inserting `None` sentinels to break cy…
    - `remap_block(flat_tex, call_head, file_parser, replacement_path=None, renaming_function=None)` — Locate resource commands, extract filenames, optionally rename/repath them, and rewrite the command…
    - `remap_figures(flat_tex, figures_path=None)` — Rewrite the corresponding TeX resource or reference commands and return the updated source together…
    - `remap_bibliography(flat_tex, bib_path=None)` — Rewrite the corresponding TeX resource or reference commands and return the updated source together…
    - `remap_style_files(flat_tex, styles_path=None)` — Rewrite the corresponding TeX resource or reference commands and return the updated source together…
    - `get_call_list(tex_stream, tags)` — Resolve and return the requested derived value from the object’s current configuration.
    - `create_label_block_map(tex_stream, call_tags, block_parser)` — Scan the TeX source for the requested command family and organize parsed blocks by type and source…
    - `create_label_map(tex_stream)` — Scan the TeX source for the requested command family and organize parsed blocks by type and source…
    - `create_ref_map(tex_stream)` — Scan the TeX source for the requested command family and organize parsed blocks by type and source…
    - `create_cite_map(tex_stream)` — Scan the TeX source for the requested command family and organize parsed blocks by type and source…
    - `remap_citation_set(tex_stream, ref_handler, cite_map=None)` — Rewrite the corresponding TeX resource or reference commands and return the updated source together…
    - `remap_citations(flat_tex, si_tex=None, citation_renaming_function=None)` — Rewrite the corresponding TeX resource or reference commands and return the updated source together…
    - `ref_remapping_label(head, label, si_index_map)` — Convert references to supplementary labels into explicit display text while leaving main-document r…
    - `figure_table_remapping(si_labels, label_function=None)` — Build a closure that rewrites references using stable supplementary figure/table/equation indices.
    - `remap_refs(tex_stream, ref_handler, ref_map=None)` — Rewrite the corresponding TeX resource or reference commands and return the updated source together…
    - `find_si_documents(flat_tex)` — Find external supplementary-document commands and map document names to their source endpoint range…
    - `remap_si(flat_tex)` — Rewrite the corresponding TeX resource or reference commands and return the updated source together…
    - `create_flat_tex(include_aux=True)` — Flatten imports and optionally remap styles, figures, bibliography, supplementary documents, and ci…
    - `transpile(target_dir, file_name='main.tex', include_si=True, include_aux=True, allow_missing_styles=False)` — Flatten the document, copy remapped auxiliary resources and supplementary files, and write the fina…

### `TemplateWriter.py`
  - **class `TemplateWriter`**
    > A general class that can take a directory layout and apply template parameters to it
    > Very unsophisticated but workable. For a more sophisticated take that walks through
    > object trees, see `TemplateEngine`.
    - `__init__(template_dir, replacements=None, file_filter=None, **opts)`
    - `replacements()` — Lazily compile replacement keys into backtick-delimited string substitution pairs.
    - `apply_replacements(string)` — Applies the defined replacements to the
    - `write_file(template_file, out_dir, apply_template=True, template_dir=None)` — writes a single _file_ to _dir_ and fills the template from the parameters passed when intializing…
    - `iterate_write(out_dir, apply_template=True, src_dir=None, template_dir=None)` — Iterates through the files in the template_dir and writes them out to dir
  - **class `OptionalTemplate`**
    - `__init__(template, **opts)`
    - **class `DefaultFormatter`** (Formatter)
      - `get_value(key, args, kwds)` — Resolve and return the requested derived value from the object’s current configuration.
    - `apply_template(template, opts, formatter=None, strip_missing_blocks=None, strip_missing=True)` — Format optional placeholders with a sentinel for missing keys, then remove missing values or entire…
    - `apply(**opts)` — Merge instance defaults with call-time options and apply them to the stored optional template.

### `TemplateEngine/ObjectWalker.py` — Provides a class that will walk through a set of objects & their children, as loaded into memory,
  - **class `ObjectTree`** (dict)
    > Simple tree that stores the structure of the documentation
  - **class `ObjectSpec`** (dict)
  - **class `MethodDispatch`** (collections.OrderedDict)
    > Provides simple utility to dispatch methods based on types
    - `__init__(*args, default=None, **kwargs)`
    - **class `DispatchTests`**
      - `__init__(*tests)`
      - `test(k, obj)` — Does the actual dispatch testing
    - `method_dispatch(obj, *args, **kwargs)` — A general-ish purpose type or duck-type method dispatcher.
  - **class `ObjectHandler`**
    - `__init__(obj, *, spec=None, tree=None, name=None, parent=None, walker=None, extra_fields=None, **kwargs)`
    - `resolve_key(key, default=None)` — Look up a field in the object specification first and then in the extra field mapping.
    - `name()` — Returns the name (not full identifier) of the object
    - `get_name()` — Returns the name the object will have in its documentation page
    - `get_identifier(o)` — Build a dotted identifier from an explicit identifier, module name, and qualified object name.
    - `identifier()` — Lazily compute and cache the dotted identifier for the handled object.
    - `parent()` — Returns the parent object for docs purposes
    - `resolve_parent(check_tree=True)` — By default, just the module in which it is contained.
    - `resolve_relative_obj(spec)` — Resolve a relative or attribute-based object specification against the handled object and its modul…
    - `children()` — Returns the child objects for docs purposes
    - `resolve_children(check_tree=True)` — First tries to use any info supplied by the docs tree
    - `tree_spec()` — Provides info that gets added to the `written` dict and which allows
    - `handle()` — Define the abstract operation performed after an object and its descendants have been traversed.
    - `stop_traversal()` — Report whether traversal should stop before recording or visiting the handled object.
  - **class `ObjectWalker`**
    > A class that walks a module/object structure, calling handlers
    > appropriately at each step
    > *(truncated — see stub for full docstring)*
    - `__init__(handlers=None, tree=None, **extra_fields)`
    - `get_handler(obj, *, tree=None, walker=None, cls=None, **kwargs)` — Construct an explicitly requested handler class or dispatch the object through the configured handl…
    - `resolve_object(o)` — Resolves to an arbitrary object by name
    - `resolve_spec(spec, **kwargs)` — Resolves an object spec.
    - `visit(o, parent=None, depth=0, max_depth=-1, **kwargs)` — Visits a single object in the tree

### `TemplateEngine/TemplateEngine.py`
  - **class `TemplateOps`**
    - `loop(caller, *args, joiner='', formatter=None, **kwargs)` — Call a template operation over synchronized positional and keyword iterables and optionally join th…
    - `loop_template(template, *args, joiner='', formatter=None, **kwargs)` — Format a string template over synchronized iterables using `loop`.
    - `join(*args, joiner=' ', formatter=None)` — Join a sequence of strings, accepting either separate values or one non-string iterable.
    - `load(template, formatter=None)` — Load a named template through the active formatter.
    - `include(template, formatter=None)` — Load and immediately render another template using the current format parameters.
    - `apply(template, *args, formatter=None, **kwargs)` — Render a template with explicit arguments through the active formatter.
    - `nonempty(data, formatter=None)` — Test whether a value is non-`None` and has positive length.
    - `wrap(fn)` — Adapt a callable so it accepts and ignores the formatter keyword injected into directives.
    - `cleandoc(txt, formatter=None)` — Normalize indentation and surrounding whitespace in documentation text.
    - `wrap_str(obj, formatter=None)` — Convert an object to an escaped string literal, using triple quotes for multiline text.
    - `optional(key, default='', formatter=None)` — Retrieve an optional formatting parameter with a fallback value.
  - **class `FormatDirective`** (enum.Enum)
    > Base class for directives -- shouldn't be an enum really...
    - `__init__(name, callback=None)`
    - `extend(*others)` — Create a new directive enumeration containing members from this class and additional enumerations.
  - **class `TemplateFormatDirective`** (FormatDirective)
  - **class `TemplateFormatterError`** (ValueError)
  - **class `TemplateASTEvaluator`**
    - `__init__(formatter, directives, format_parameters)`
    - `handle_comprehension(g, expr, callback)` — Evaluate one comprehension generator while temporarily binding its target variable.
    - `evaluate_node(node)` — Recursively interpret the supported subset of Python AST nodes used by template expressions.
  - **class `TemplateFormatter`** (string.Formatter)
    > Provides a formatter for fields that allows for
    > the inclusion of standard Bootstrap HTML elements
    > alongside the classic formatting
    - **class `frozendict`** (dict)
    - `__init__(templates=None)`
    - `format_parameters()` — Return the parameter mapping for the innermost active formatting operation.
    - `templates()` — **LLM Docstring**
    - `special_callbacks()` — Map special format-field markers to evaluation, directive, comment, raw, and assignment handlers.
    - `callback_map()` — Combine special markers with every registered directive marker.
    - `apply_eval_tree(_, spec)` — Parse and evaluate a cleaned Python expression or statement block against the active parameters.
    - `apply_directive_tree(_, spec)` — Evaluate a directive expression after wrapping it in parentheses.
    - `apply_assignment(_, spec, eval=False)` — Assign the literal right-hand text from an inline assignment into the active parameter mapping.
    - `apply_raw(key, spec)` — :param key: the lookup, assignment, or formatting key
    - `apply_comment(key, spec)` — :param key: the lookup, assignment, or formatting key
    - `apply_directive(key, spec)` — Convert a directive marker and argument text into an evaluable directive call.
    - `format_field(value, format_spec)` — Route special string-valued fields through callback handlers and otherwise use standard formatting.
    - `load_template(template)` — Resolve a registered template and read file-backed content with caching.
    - `vformat(format_string, args, kwargs)` — Render a template within a temporary parameter scope populated with special callback markers.
  - **class `OrderedSet`** (dict)
    - `__init__(*iterable)`
    - `union(other)` — Return a new ordered set containing this set followed by unseen keys from another set.
    - `add(k)` — Add a key while preserving insertion order and uniqueness.
    - `update(ks)` — Add every key from an iterable.
  - **class `Locator`** (typing.Protocol)
    - `locate(identifier)` — Define the protocol operation that resolves a resource identifier.
    - `paths(**opts)` — Define the protocol operation that enumerates available resource identifiers.
  - **class `ResourcePathLocator`** (Locator)
    - `__init__(path)`
    - `locate(identifier)` — Resolve an existing absolute or relative identifier, searching configured roots in order.
    - `resource_path(d, f)` — Join a search root with a resource-relative path.
    - `paths(max_depth=7, **_)` — Walk search roots and collect resource-relative file paths up to a maximum depth.
    - `directories()` — Return the concrete root directories searched by this locator.
  - **class `SubresourcePathLocator`** (ResourcePathLocator)
    - `__init__(roots, extension)`
    - `resource_path(d, f)` — Join a root, fixed subresource directory, and resource-relative path.
  - **class `ResourceLocator`** (Locator)
    - `__init__(locators)`
    - `locate(identifier)` — Return the first resource path resolved by the configured locators.
    - `paths(filter_pattern=None, **_)` — Combine resource paths from all locators and optionally filter them by regex or glob.
    - `directories()` — Return unique search directories from all component locators in encounter order.
  - **class `TemplateEngine`**
    > Provides an engine for generating content using a
    > `TemplateFormatter` and `ResourceLocator`
    - `__init__(locator, template_pattern='*.*', ignore_missing=False, formatter_class=None, ignore_paths=())`
    - `format_map(template, parameters)` — Resolve a template identifier when registered and render it with a parameter mapping.
    - `format(template, **parameters)` — Render a template using keyword parameters.
    - **class `outStream`**
      - `__init__(file, mode='w+', **kw)`
      - `write(s)` — Open the output context, write one string, and return the original destination.
    - `write_string(target, txt)` — Write rendered text to a target through `outStream`.
    - `apply(template, target, **template_params)` — Render a template and either return the string or write it unless the target is ignored.
  - **class `TemplateHandler`** (ObjectHandler)
    - `__init__(obj, *, out=None, engine=None, root=None, squash_repeat_packages=True, is_package_root=False, **extra_fields)`
    - `template_params(**kwargs)` — Merge handler extra fields with parameters computed for the current object.
    - `get_template_params(**kwargs)` — Returns the parameters that should be inserted into the template
    - `package_path()` — Return the package name and source URL tuple for the handled object.
    - `get_package_and_url(include_url_base=True)` — Returns package name and corresponding URL for the object
    - `target_identifier()` — Return the normalized dotted identifier used for the output target.
    - `squash_reps(ident)` — Collapse the leading repeated package components in a dotted identifier.
    - `get_target_extension(identifier=None)` — Split an object identifier into normalized path components for output and resource lookup.
    - `get_output_file(out)` — Returns package name and corresponding URL for the object
    - `handle(template=None, target=None, write=True)` — Formats the documentation Markdown from the supplied template
    - `check_should_write()` — Determines whether the object really actually should be
  - **class `TemplateResourceExtractor`** (ResourceLocator)
    - `path_extension(handler)` — Provides the default examples path for the object
    - `get_resource(handler, keys=None, attrs=None)` — Locate a resource using configured handler fields, object attributes, or the default derived path.
    - `load(handler)` — Loads examples for the stored object if provided
  - **class `ModuleTemplateHandler`** (TemplateHandler)
  - **class `ClassTemplateHandler`** (TemplateHandler)
  - **class `FunctionTemplateHandler`** (TemplateHandler)
  - **class `MethodTemplateHandler`** (TemplateHandler)
  - **class `ObjectTemplateHandler`** (TemplateHandler)
  - **class `IndexTemplateHandler`** (TemplateHandler)
  - **class `TemplateWalker`** (ObjectWalker)
    - `__init__(engine, out=None, description=None, **extra_fields)`
    - `default_handlers()` — Build the ordered mapping from modules, classes, functions, and fallback objects to handler classes.
    - `get_handler(obj, *, out=None, engine=None, tree=None, **kwargs)` — Construct a handler while injecting this walker’s output directory and template engine.
    - `visit_root(o, **kwargs)` — Visit a root object through the standard traversal implementation.
    - `write(objects, max_depth=-1, index='index.md')` — Walks through the objects supplied and applies the appropriate templates
  - **class `TemplateResourceList`** (Locator)
    > Implements the `ResourceLocator` interface, but is backed by a `dict` of
    > explicit resources rather than a set of paths.
    - `__init__(resource_dict)`
    - `paths(**_)` — Return the identifiers available in the explicit resource mapping.
    - `locate(identifier)` — Retrieve the resource associated with an identifier, returning `None` when absent.
  - **class `TemplateInterfaceList`** (TemplateResourceList)
    > A set of functions to be used to construct interfaces
    - `__init__(resource_dict)`
  - **class `TemplateInterfaceFormatter`**
    > Provides an interface that mimics a `TemplateFormatter`
    > but does nothing more than route to a set of template functions
    - `__init__(templates)`
    - `format_parameters()` — Return the innermost active interface parameter mapping.
    - `templates()` — :return: The stored mapping of interface template callables.
    - `special_callbacks()` — Return the currently empty special-callback mapping for interface templates.
    - `load_template(template)` — Retrieve a callable template by identifier.
    - `vformat(template, args, kwargs)` — Invoke a callable template inside a temporary formatting-parameter scope.
  - **class `TemplateInterfaceEngine`** (TemplateEngine)
    > A variant on a template engine designed for more interactive use.
    > In many ways, _not_ a template engine, but too useful to ignore while I
    > find a more uniform abstraction.
    > Generates _interfaces_ from a set of interface template functions
    > rather than strings from template files.
    - `__init__(templates, ignore_missing=False, formatter_class=None, ignore_paths=())`
    - `format_map(template, parameters)` — Resolve and invoke a callable template with the supplied parameter mapping.
    - `apply(template, target, **template_params)` — Return an interface result directly or map it to a non-ignored target key.
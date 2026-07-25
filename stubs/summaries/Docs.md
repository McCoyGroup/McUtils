### `DocWalker.py` — Provides a class that will walk through a set of objects & their children, as loaded into memory, a…
  - **class `DocSpec`** (ObjectSpec)
    > A specification for an object to document.
    > Supports the fields given by `spec_fields`.
  - **class `ExamplesExtractor`** (TemplateResourceExtractor)
  - **class `TestsExtractor`** (TemplateResourceExtractor)
    - `path_extension(handler)` — Provides the default examples path for the object
    - `load(handler)` — Loads a test resource and wraps nonempty source in an `ExamplesParser`.
  - **class `TestExamplesFormatter`**
    - `__init__(parser)`
    - `from_file(tests_file)` — Creates an examples formatter from a test file.
    - `get_template_parameters()` — Formats an examples file
  - **class `DocTemplateOps`** (MarkdownOps)
  - **class `InteractiveTemplateEngine`** (TemplateInterfaceEngine)
    - `__init__(templates=None, ignore_missing=False, formatter_class=None, ignore_paths=())`
    - `clean_params(params)` — Removes fields whose values are `None` or empty strings.
    - `prep_pars(writer, pars)` — Converts named documentation sections into JHTML heading/content pairs.
    - `format_parameters_table(parameters)` — Renders parsed parameter metadata as a vertical JHTML flex container.
    - `format_props_table(writer, props)` — Renders class property names and runtime type names as a vertical flex container.
    - `format_related_links(writer, related)` — Builds interactive links that resolve and display related objects on demand.
    - `index_browser(index_files=None, details=None, related=None, description=None, examples=None, _self=None, **kw)` — Builds the interactive root index and initializes the shared display pane on first use.
    - `module_browser(members=None, name=None, id=None, details=None, related=None, description=None, examples=None, tests=None, lineno=None, _self=None, **kw)` — Builds an interactive module view with lazily loaded member documentation.
    - `class_browser(id=None, name=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, methods=None, examples=None, tests=None, details=None, _self=None, **_)` — Builds an interactive class view containing properties, parameters, methods, and optional sections.
    - `method_browser(id=None, name=None, decorator=None, signature=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, examples=None, tests=None, details=None, **_)` — Builds a collapsible interactive method view with syntax-styled signature and parsed documentation.
    - `object_browser(id=None, name=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, methods=None, examples=None, tests=None, details=None, _self=None, **_)` — Builds an interactive fallback view for a general documented object.
    - `function_browser(id=None, name=None, decorator=None, signature=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, examples=None, tests=None, details=None, **_)` — Builds an interactive function view with signature, parameter metadata, and optional sections.
  - **class `DocTemplateHandler`** (TemplateHandler)
    - `__init__(obj, *, out=None, engine=None, root=None, examples_loader=None, tests_loader=None, include_line_numbers=True, walker=None, **extra_fields)`
    - `get_lineno()` — Finds the one-based source line for the handled object when line numbers are enabled.
    - `parse_doc(doc)` — :param doc:
    - `load_examples()` — Loads examples through the configured examples extractor.
    - `load_tests()` — Loads and formats tests, falling back to matching tests inherited from the parent handler.
  - **class `DocObjectTemplateHandler`** (DocTemplateHandler)
    - `get_package_and_url(include_url_base=True)` — Normalizes package source URLs so package `__init__.py` paths point to the package module path.
    - `load_examples()` — Loads examples through the configured examples extractor.
    - `load_tests()` — Loads and formats tests, falling back to matching tests inherited from the parent handler.
  - **class `ModuleWriter`** (DocTemplateHandler)
    > A writer targeted to a module object. Just needs to write the Module metadata.
    > *(truncated — see stub for full docstring)*
    - `__init__(obj, is_package_root=None, **kwargs)`
    - `get_template_params()` — Provides module specific parameters
    - `get_members(mod)` — Returns the module names explicitly exported through `__all__`.
  - **class `ClassWriter`** (DocObjectTemplateHandler)
    > A writer targeted to a class
    > *(truncated — see stub for full docstring)*
    - `load_methods(function_writer=None)` — Loads the methods supported by the class
    - `format_prop(k, o)` — Formats a property name and the concrete type name of its value.
    - `get_template_params(function_writer=None)` — :param function_writer:
  - **class `FunctionWriter`** (DocObjectTemplateHandler)
    > Writer to dump functions to file
    > *(truncated — see stub for full docstring)*
    - `get_signature()` — Obtains the inspectable call signature of the handled function.
    - `get_template_params(**kwargs)` — Collects function metadata, parsed docstring fields, examples, tests, and source location for rende…
  - **class `MethodWriter`** (FunctionWriter)
    > Writes class methods to file
    > (distinct from functions since not expected to exist solo)
    - `get_template_params(**kwargs)` — Collects method template parameters after unwrapping class, static, and property descriptors.
    - `get_signature()` — Returns the handled method signature, falling back to `(self)` for non-inspectable properties.
    - `identifier()` — Resolves the method identifier, constructing property identifiers from their parent class.
  - **class `ObjectWriter`** (DocObjectTemplateHandler)
    > Writes general objects to file.
    > Basically a fallback to support singletons and things
    > of that nature.
    > *(truncated — see stub for full docstring)*
    - `identifier()` — Builds a fallback identifier for a general object and drops the enclosing class component.
    - `check_should_write()` — Determines whether the object really actually should be
    - `get_template_params()` — Collects fallback object metadata from its docstring, type, examples, and source line.
  - **class `IndexWriter`** (DocTemplateHandler)
    > Writes an index file with all of the
    > written documentation files.
    > Needs some work to provide more useful info by default.
    > *(truncated — see stub for full docstring)*
    - `__init__(*args, description=None, **kwargs)`
    - `get_identifier(o)` — Returns the fixed identifier used for documentation indexes.
    - `get_file_paths()` — Normalizes written file paths relative to the configured documentation root.
    - `get_index_files()` — Converts string paths into `[stem, path]` index entries.
    - `get_template_params()` — Parses the index description and assembles index entries and examples for rendering.
  - **class `DocWalker`** (TemplateWalker)
    > A class that walks a module structure, generating `.md` files for every class inside it as well as for global functions,
    > and a Markdown index file.
    > *(truncated — see stub for full docstring)*
    - `__init__(out=None, engine=None, verbose=True, template_locator=None, examples_directory=None, tests_directory=None, **extra_fields)`
    - `get_engine(locator)` — Non-engine locators are wrapped in a Markdown `TemplateEngine` using `*.md` templates.
    - `get_examples_loader(examples_directory)` — Normalizes an examples directory into an `ExamplesExtractor`.
    - `get_tests_loader(tests_directory)` — Normalizes a tests directory into a `TestsExtractor`.
    - `get_handler(*args, examples_loader=None, tests_loader=None, **kwargs)` — Creates a handler while injecting the walker's default examples and tests loaders.
    - `visit_root(o, tests_directory=None, examples_directory=None, verbose=None, **kwargs)` — Visits one root specification while temporarily applying root-specific test and example directories.
- `jdoc(obj, max_depth=1, engine=None, verbose=False, **etc)` — provides documentation in a Jupyter-friendly environment

### `DocsBuilder.py`
  - **class `DocBuilder`**
    > A documentation builder class that uses a `DocWalker`
    > to build documentation, but which also has support for more
    > involved use cases, like setting up a `_config.yml` or other
    > documentation template things.
    > *(truncated — see stub for full docstring)*
    - `__init__(packages=None, config=None, target=None, root=None, config_file=None, templates_directory=None, examples_directory=None, tests_directory=None, readme=None)`
    - `get_template_locator(template_directory, use_repo_templates=False)` — Builds the resource search path used to locate documentation templates.
    - `load_config()` — Loads the config file to be used and fills in template parameters
    - `create_layout()` — Creates the documentation layout that will be expanded upon by
    - `load_walker()` — Loads the `DocWalker` used to write docs.
    - `build()` — Writes documentation layout to `self.target`

### `Docstrings.py`
  - **class `DocstringDialectHandler`** (abc.ABC)
    > A pluggable docstring convention: parses raw text into the canonical
    > ``DocstringData`` fields, and renders those fields back into text using
    > the same convention.
    > *(truncated — see stub for full docstring)*
    - `sniff(raw)` — Return True if `raw` looks like it was written in this dialect.
    - `extract(raw, node)` — Parse `raw` (+ signature info from `node`) into the canonical dict:
    - `render(data)` — Render a (possibly edited) ``DocstringData`` back into body text.
  - **class `GoogleDialectHandler`** (DocstringDialectHandler)
    > Google-style: ``Args:`` / ``Returns:`` / ``Examples:`` sections.
    - `sniff(raw)`
    - `extract(raw, node)`
    - `render(data)`
  - **class `SphinxDialectHandler`** (DocstringDialectHandler)
    > reST/Sphinx-style: ``:param name:`` / ``:type name:`` / ``:return:`` /
    > ``:rtype:`` field lists, e.g.::
    > *(truncated — see stub for full docstring)*
    - `sniff(raw)`
    - `extract(raw, node)`
    - `render(data)`
  - **class `PlainDialectHandler`** (DocstringDialectHandler)
    > Fallback for free-text docstrings with no recognized section markup.
    > Preserves a summary/details split and any doctest examples, but does not
    > impose ``Args:``/``:param:`` structure the original text didn't have.
    - `sniff(raw)`
    - `extract(raw, node)`
    - `render(data)`
- `detect_dialect(raw, default=None)` — Pick the dialect handler that best matches `raw`.
- `resolve_dialect(dialect, default=dev.default)`
- `data_extractor(raw, node, dialect=None)` — Break a raw docstring + its function node into structured fields.
- `default_exclude(qualname, package_name=None)` — True if any dotted component of `qualname` -- i.e.
  - **class `DocstringData`**
    > Structured record of one function/method's docstring and metadata.
    > *(truncated — see stub for full docstring)*
    - `to_json()` — Return a plain, JSON-serializable dict of this record.
    - `from_json(d)` — Reconstruct a record from a dict produced by :meth:`to_json`.
  - **class `DocstringParser`**
    > Parse a Python source file into a list of :class:`DocstringData`.
    > *(truncated — see stub for full docstring)*
    - `__init__(dialect=None, filter=None, exclude=default_exclude)`
    - `wanted(qualname, package_name=None)` — True if `qualname` should actually be parsed, given this
    - `parse_source(src, only_missing=False, package_name=None)` — Parse `src` text and return one :class:`DocstringData` per function.
    - `parse_file(path, only_missing=False, package_name=None)` — Read `path` and delegate to :meth:`parse_source`.
  - **class `DocstringWriter`**
    > Write (possibly edited) :class:`DocstringData` records back into source.
    > *(truncated — see stub for full docstring)*
    - `__init__(header=DEFAULT_HEADER, add_header=True, dialect=None)`
    - `write_source(src, data_list)` — Return a new source string with the given records' docstrings applied.
    - `write_file(path, data_list, target=dev.default, backup=None)` — Read `path`, apply `data_list`, and write the result back to `path`.
    - `verify_code_identity(original_src, new_src)` — Confirm only docstrings differ between two versions of a file.
  - **class `DocstringQAField`**
    - `register(name, method=None)`
    - `__init__(description=None, score=None)`
    - `short_name()`
  - **class `MissingDescription`** (DocstringQAField)
  - **class `MissingShortDescription`** (MissingDescription)
  - **class `MissingParameter`** (DocstringQAField)
  - **class `MissingReturnValue`** (DocstringQAField)
  - **class `MissingReturnType`** (DocstringQAField)
  - **class `StaleParameter`** (DocstringQAField)
  - **class `StaleParameterType`** (DocstringQAField)
  - **class `MissingParameterDescription`** (MissingDescription)
  - **class `MissingParameterType`** (DocstringQAField)
  - **class `BadDescription`** (DocstringQAField)
  - **class `ShortDescriptionTooLong`** (BadDescription)
  - **class `HasExamples`** (DocstringQAField)
  - **class `HasRelated`** (DocstringQAField)
  - **class `HasLinks`** (DocstringQAField)
  - **class `DocstringDataAnalyzer`**
    - `__init__(data, analyses=None)`
    - `default_analyses()`
    - `get_analyses()`
    - `analyze_docstring_quality()` — Heuristically assess the quality of a parsed docstring.
  - **class `DocstringsHandler`** (PackageHandler)
    > `PackageHandler` that runs `DocstringParser` + `DocstringDataAnalyzer`
    > over every function/method in a package's source during `parse()`, then
    > -- at `write()` time, once every package has been processed -- writes a
    > single `docstring_quality.json` at the root of `out_dir` tracking the
    > score and issue breakdown for every docstring in the whole run.
    > *(truncated — see stub for full docstring)*
    - `__init__(dispatcher, dialect=None, analyses=None, filter=None, exclude=default_exclude)`
    - `parse(package_name, pkg_src_path)` — Score every docstring under `pkg_src_path`; safe against any one
    - `write(components, compact=True)` — Aggregate every package's `parse()` result into a single

### `ExamplesParser.py`
  - **class `ExamplesParser`**
    > Provides a parser for unit tests to turn them into examples
    - `__init__(unit_tests)`
    - `find_setup(tree_iter)` — Consumes leading module-level setup nodes until the first class definition.
    - `parse_tests(tree_iter)` — Parses out the
    - `walk_tree()` — Separates module setup, class setup, and `test_` methods and refreshes all parser caches.
    - `format_node(node)` — Returns the source text for an AST node with its original leading indentation.
    - `from_file(tests_file)` — Creates a parser from a test source file.
    - `class_spec()` — Returns the parsed test class and its non-test setup nodes.
    - `setup()` — Returns module-level setup nodes preceding the test class.
    - `functions()` — Returns the ordered mapping of example names to `test_` function nodes.
    - `functions_map()` — Returns the reverse mapping from referenced names to examples that use them.
    - `load_function_map()` — Builds a reverse index of names referenced by each parsed test function.
    - `get_examples_functions(node)` — Collects names referenced by a function or AST node body.
    - `filter_by_name(name)` — Returns a shallow parser copy restricted to examples that reference a given name.

### `HTMLDocs.py` — Provides `static_doc`, a sibling to `McUtils.Docs.jdoc` that walks an object
  - **class `JHTMLDocumentationEngine`** (TemplateInterfaceEngine)
    > Renders the same fields `InteractiveTemplateEngine` renders into
    > ipywidget-backed JHTML elements, but using only the plain (non-widget)
    > side of the same `JHTML` element interfaces -- `JHTML.Div`,
    > `JHTML.Details`/`JHTML.Summary`, `JHTML.Heading` & friends, `JHTML.Code`,
    > `JHTML.Markdown`, `JHTML.List`/`JHTML.ListItem` -- so the whole tree
    > serializes to plain text via `.tostring()` with no kernel involved.
    > *(truncated — see stub for full docstring)*
    - `__init__(templates=None, ignore_missing=False, formatter_class=None, ignore_paths=())`
    - `md(text)` — Converts nonempty Markdown text to a JHTML Markdown element.
    - `clean_params(params)` — Removes fields whose values are `None` or empty strings.
    - `params_table(parameters)` — Renders parsed parameter metadata as a documentation list.
    - `extra_sections(**fields)` — Renders nonempty named fields as native `<details>` sections.
    - `code_block(decorator, name, signature)` — Renders a compact Python function signature block.
    - `index_browser(index_files=None, details=None, related=None, description=None, examples=None, _self=None, **kw)` — Renders an index page from its description, child index entries, and optional sections
    - `module_browser(members=None, name=None, id=None, details=None, related=None, description=None, examples=None, tests=None, lineno=None, _self=None, **kw)` — Renders a module section with expandable output for each documented member
    - `class_browser(id=None, name=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, methods=None, examples=None, tests=None, details=None, _self=None, **_)` — Renders a class section containing description, properties, parameters, and handled methods
    - `method_browser(id=None, name=None, decorator=None, signature=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, examples=None, tests=None, details=None, **_)` — Renders a method as a collapsible details element with signature and documentation
    - `object_browser(id=None, name=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, methods=None, examples=None, tests=None, details=None, _self=None, **_)` — Renders a generic object section with its runtime type and optional documentation sections
    - `function_browser(id=None, name=None, decorator=None, signature=None, related=None, out_file=None, lineno=None, parameters=None, props=None, description=None, examples=None, tests=None, details=None, **_)` — Renders a function section containing its signature, description, parameters, and optional sections
- `static_doc(obj, max_depth=1, title=None, out_file=None, include_finx_js=True, verbose=False, return_string=False)` — Walks `obj` with the exact same `DocWalker` machinery `jdoc` uses

### `MarkdownTemplates.py`
  - **class `MarkdownOps`**
    - `format_item(item, item_level=0)` — Formats a value as an indented Markdown list item.
    - `format_link(alt, link)` — :param alt: the visible link text
    - `format_obj_link(spec, root=None)` — Formats a link to a documented object using its canonical name and path.
    - `format_inline_code(arg)` — :param arg:
    - `format_code_block(arg)` — :param arg:
    - `format_quote_block(arg)` — :param arg:
    - `format_grid(link_grid, boxed=False)` — Renders rows of Markdown content inside the module's Bootstrap-style HTML grid templates.
    - `split(links, ncols=3, pad='')` — Splits a sequence into fixed-width rows and pads the final row.
    - `format_collapse_section(header, content, name=None, open=True, include_opener=True)` — Formats content as a Bootstrap-compatible collapsible section.
    - `format_obj_link_grid(mems, ncols=3, root=None, boxed=True)` — Builds a boxed grid of canonical links for object identifiers.
    - `canonical_name(identifier, formatter=None)` — Returns the final dotted component of an object identifier.
    - `canonical_link(identifier, root=None, formatter=None)` — Converts a dotted object identifier into a relative Markdown filename.
    - `html(tag, content, markdown=True, formatter=None, **styles)` — Wraps content in a `JHTML.HTML` element and substitutes it after serialization.
    - `bootstrap(tag, content, markdown=True, formatter=None, **styles)` — Wraps content in a Bootstrap JHTML component and substitutes it after serialization.
    - `alert(content, variant='warning', markdown=True, formatter=None, **styles)` — Formats content with the Bootstrap `Alert` component.
  - **class `MarkdownFormatDirective`** (FormatDirective)
  - **class `MarkdownTemplateFormatter`** (TemplateFormatter)

### `Stubs.py` — Self-contained toolkit that turns a Python package into two LLM-friendly
- `default_exclude(qualname, package_name=None)` — Default `exclude` predicate shared by `StubSummaryBuilder`,
  - **class `StubSummaryBuilder`**
    > Parameters
    > ----------
    > root_src_dir : str or None
    >     Path to the root module's source directory (the folder
    >     containing its __init__.py). If None, the root module must be
    >     importable and its location is resolved from that import.
    > out_dir : str
    >     Output directory. Stub trees are written to
    >     `<out_dir>/<root_module_name>/<pkg_name>/...`, summaries to
    >     `<out_dir>/summaries/<pkg_name>.md`, and the graph index to
    >     `<out_dir>/summaries/index.md`.
    > max_doc_len : int
    >     Cap on class docstrings in summaries: first paragraph or this
    >     many characters, whichever comes first.
    > min_words : int
    >     For one-line descriptions: skip docstring lines with this many
    >     words or fewer (filters out short placeholder lines), using the
    >     first line that exceeds it.
    > write_sidecar_file : bool…
    > *(truncated — see stub for full docstring)*
    - `__init__(out_dir='stubs', max_doc_len=800, min_words=5, write_sidecar_file=False, verbose=False, dispatcher=None, filter=None, exclude=default_exclude)`
    - `wanted(qualname, package_name=None)` — True if `qualname` should appear in the API summary, given this
    - `root_module_name()`
    - `dynamic_mode()`
    - `dependency_graph()`
    - `sidecar()`
    - `collapse_scalar_assign_runs(body, min_group=6, context=None)`
    - `is_collapsed_registry(node)`
    - `externalize_large_literal(node, module_key)`
    - `is_simple_assign(node, max_len=120)`
    - `is_all_operation(node)` — True for any statement that assigns to, augments, or mutates
    - `resolve_dynamic_all(package_name, rel_path=None)` — If we're in dynamic_mode (the root module was really
    - `record_module_dependencies(source, package_name, rel_path=None)` — Parse the ORIGINAL (pre-stub) source of one module and record,
    - `write_dependency_graph()` — Write dependency_graph.json at the root of out_dir.
    - `stub_function(node)`
    - `stub_class(node)`
    - `stub_module(source, module_key, dynamic_all=None)`
    - `stub_package(src_dir, out_dir, package_name=None, keep_full=None)`
    - `write_sidecar_files()`
    - `first_line(docstring, max_len=100)`
    - `class_doc_summary(full_doc)`
    - `render_params(args, skip_first=False)`
    - `summarize_class(node, indent='  ', package_name=None, qualname_prefix=None)`
    - `summarize_module(path, rel_path, package_name=None)`
    - `build_package_summary(src_dir, out_file, package_name=None)`
    - `write_llm_readme()` — Write LLM.md at the root of out_dir: an operating manual for
    - `write_index(report)` — Write summaries/index.md from a flat {package_name: info} report
  - **class `PackageHandler`**
    > Base class for one pluggable, per-package documentation artifact.
    > *(truncated — see stub for full docstring)*
    - `__init__(dispatcher)`
    - `parse(package_name, pkg_src_path)` — Do the per-package work; return this package's components.
    - `write(components)` — Do the cross-package work, given every package's `parse()` result.
  - **class `StubSummaryHandler`** (PackageHandler)
    > Generates per-module stubs + a per-package API summary during
    > `parse()`. At `write()` time -- once every package has been parsed --
    > writes the artifacts that depend on the full set having been built:
    > dependency_graph.json, the sidecar data file (if enabled),
    > summaries/index.md, and LLM.md.
    - `__init__(dispatcher, builder=None, filter=None, exclude=default_exclude)`
    - `parse(package_name, pkg_src_path)`
    - `write(components)`
  - **class `ExampleHandler`** (PackageHandler)
    > Extracts runnable examples from each package's test file (see
    > `locate_test_file`) during `parse()`, writing each one under
    > `<out_dir>/examples/<package_name>/` immediately (there's no reason to
    > defer per-example writes -- they don't depend on any other package).
    > At `write()` time, writes the single aggregated usage_graph.json built
    > up across every package's examples.
    - `__init__(dispatcher, filter=None, exclude=default_exclude)`
    - `wanted(qualname, package_name=None)` — True if `qualname` (a ``"{TestClass}.{test_method}"`` name)
    - `locate_test_file(package_name, tests_directory)` — a flat directory containing one `<PackageName>Tests.py` file per
    - `build_usage_graph_for_package(package_name, parser)` — Combine ExamplesParser.functions_map (bare name -> example
    - `extract_examples(package_name, tests_directory=None)` — For one top-level package: locate its test file (see
    - `write_usage_graph()` — Write usage_graph.json at the root of out_dir: {fully
    - `parse(package_name, pkg_src_path)`
    - `write(components)`
  - **class `DocumentationPackageDispatcher`**
    > Owns package/module resolution -- discovering a root module's
    > top-level packages, and the per-run state that comes with that
    > (sidecar data, dependency/usage graphs, the accumulated report) -- and
    > drives a set of `PackageHandler`s over it. Each handler is responsible
    > for one independent documentation artifact; by default that's stubs
    > +summaries (`StubSummaryHandler`) and extracted examples
    > (`ExampleHandler`), but any `PackageHandler` subclass can be added or
    > swapped in via `handlers`.
    > *(truncated — see stub for full docstring)*
    - `__init__(root_src_dir=None, out_dir='stubs', max_doc_len=800, min_words=5, write_sidecar_file=False, verbose=False, allow_static_mode=True, tests_directory=None, handlers=None)`
    - `root_module_name()`
    - `resolved_root_dir()`
    - `packages()`
    - `sidecar()`
    - `report()`
    - `dynamic_mode()`
    - `dependency_graph()`
    - `usage_graph()`
    - `discover_top_level_packages(root_module_name, try_dynamic=True, src_dir=None)`
    - **class `ModuleData`**
      - `__init__(parent, module_name, module_dir, packages, dynamic_mode)`
    - `generate(package_name, root_module_name=None, update_current=False)` — Resolve `package_name`'s source path and run every handler's
    - `generate_all(root_module_name)` — Discover every top-level package under `root_module_name`,
    - `finalize()` — Call every handler's `.write()` with the full accumulated
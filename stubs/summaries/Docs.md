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
    - `__init__(root_src_dir=None, out_dir='stubs', max_doc_len=800, min_words=5, write_sidecar_file=False, verbose=False, allow_static_mode=True, tests_directory=None)`
    - `root_module_name()`
    - `resolved_root_dir()`
    - `packages()`
    - `sidecar()`
    - `report()`
    - `dynamic_mode()`
    - `dependency_graph()`
    - `usage_graph()`
    - `collapse_scalar_assign_runs(body, min_group=6, context=None)`
    - `is_collapsed_registry(node)`
    - `externalize_large_literal(node, module_key)`
    - `is_simple_assign(node, max_len=120)`
    - `is_all_operation(node)` — True for any statement that assigns to, augments, or mutates
    - `resolve_dynamic_all(package_name, rel_path=None)` — If we're in dynamic_mode (the root module was really
    - `record_module_dependencies(source, package_name, rel_path=None)` — Parse the ORIGINAL (pre-stub) source of one module and record,
    - `write_dependency_graph()` — Write dependency_graph.json at the root of out_dir.
    - `locate_test_file(package_name, tests_directory)` — a flat directory containing one `<PackageName>Tests.py` file per
    - `build_usage_graph_for_package(package_name, parser)` — Combine ExamplesParser.functions_map (bare name -> example
    - `extract_examples(package_name, tests_directory=None)` — For one top-level package: locate its test file (see
    - `write_usage_graph()` — Write usage_graph.json at the root of out_dir: {fully
    - `stub_function(node)`
    - `stub_class(node)`
    - `stub_module(source, module_key, dynamic_all=None)`
    - `stub_package(src_dir, out_dir, package_name=None, keep_full=None)`
    - `write_sidecar_files()`
    - `first_line(docstring, max_len=100)`
    - `class_doc_summary(full_doc)`
    - `render_params(args, skip_first=False)`
    - `summarize_class(node, indent='  ')`
    - `summarize_module(path, rel_path)`
    - `build_package_summary(src_dir, out_file)`
    - `discover_top_level_packages(root_module_name, try_dynamic=True, src_dir=None)`
    - **class `ModuleData`**
      - `__init__(parent, module_name, module_dir, packages, dynamic_mode)`
    - `generate(package_name, root_module_name=None, update_current=False)`
    - `generate_all(root_module_name)`
    - `write_llm_readme()` — Write LLM.md at the root of out_dir: an operating manual for
    - `finalize()`
    - `write_index()`
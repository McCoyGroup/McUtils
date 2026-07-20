import ast, collections, inspect
__all__ = ['ExamplesParser']

class ExamplesParser:
    """
    Provides a parser for unit tests to turn them into examples
    """

    def __init__(self, unit_tests):
        """
        **LLM Docstring**

        Parses unit-test source into an AST and initializes lazy caches.

        The constructor does not classify tests immediately; `walk_tree` populates the cached class, setup, function, and function-map fields on demand.

        :param unit_tests: the Python source containing setup code and test methods
        :type unit_tests: str
        """
        ...

    def find_setup(self, tree_iter):
        """
        **LLM Docstring**

        Consumes leading module-level setup nodes until the first class definition.

        :param tree_iter: an iterator over top-level AST nodes
        :type tree_iter: Iterator[ast.AST]
        :return: the first class node, or `None`, together with the preceding setup nodes
        :rtype: tuple[ast.ClassDef | None, list[ast.AST]]
        """
        ...

    def parse_tests(self, tree_iter):
        """
        Parses out the
        :param tree_iter:
        :type tree_iter:
        :return:
        :rtype:
        """
        ...

    def walk_tree(self):
        """
        **LLM Docstring**

        Separates module setup, class setup, and `test_` methods and refreshes all parser caches.

        This implementation assumes the first class node exists and passes its body to `parse_tests`.
        :return: the module/class setup pair and ordered mapping of example names to test nodes
        :rtype: tuple[tuple[list[ast.AST], list[ast.AST]], collections.OrderedDict[str, ast.FunctionDef]]
        """
        ...

    def format_node(self, node):
        """
        **LLM Docstring**

        Returns the source text for an AST node with its original leading indentation.

        :param node: the node to format
        :type node: ast.AST
        :return: the cached source fragment
        :rtype: str
        """
        ...

    @classmethod
    def from_file(cls, tests_file):
        """
        **LLM Docstring**

        Creates a parser from a test source file.

        :param tests_file: the file to read
        :type tests_file: str | os.PathLike
        :return: a parser for the file contents
        :rtype: ExamplesParser
        """
        ...

    @property
    def class_spec(self):
        """
        **LLM Docstring**

        Returns the parsed test class and its non-test setup nodes.

        Parsing is triggered lazily if necessary.
        :return: the class node and class-setup list
        :rtype: tuple[ast.ClassDef, list[ast.AST]]
        """
        ...

    @property
    def setup(self):
        """
        **LLM Docstring**

        Returns module-level setup nodes preceding the test class.

        Parsing is triggered lazily if necessary.
        :return: the setup-node list
        :rtype: list[ast.AST]
        """
        ...

    @property
    def functions(self):
        """
        **LLM Docstring**

        Returns the ordered mapping of example names to `test_` function nodes.

        The `test_` prefix is removed from each key.
        :return: the parsed test-function mapping
        :rtype: collections.OrderedDict[str, ast.FunctionDef]
        """
        ...

    @property
    def functions_map(self):
        """
        **LLM Docstring**

        Returns the reverse mapping from referenced names to examples that use them.

        Parsing and map construction are triggered lazily if necessary.
        :return: the referenced-name mapping
        :rtype: dict[str, list[str]]
        """
        ...

    def load_function_map(self):
        """
        **LLM Docstring**

        Builds a reverse index of names referenced by each parsed test function.
        :return: a mapping from referenced names to example keys
        :rtype: dict[str, list[str]]
        """
        ...
    IGNORE_UNHANDLED_STATEMENTS = False

    def _handle_stmt(self, stmt, all_fns):
        """
        **LLM Docstring**

        Collects recognizable referenced names from one AST node.

        The traversal deliberately handles only common node shapes. Several expression forms are ignored for speed, and unrecognized forms raise unless `IGNORE_UNHANDLED_STATEMENTS` is enabled.

        :param stmt: the statement or expression to inspect
        :type stmt: ast.AST | None

        :param all_fns: the accumulator updated in place
        :type all_fns: set[str]
        """
        ...

    def get_examples_functions(self, node):
        """
        **LLM Docstring**

        Collects names referenced by a function or AST node body.

        :param node: the node whose body should be inspected
        :type node: ast.AST
        :return: the referenced-name set
        :rtype: set[str]
        """
        ...

    def filter_by_name(self, name):
        """
        **LLM Docstring**

        Returns a shallow parser copy restricted to examples that reference a given name.

        :param name: the referenced function or object name
        :type name: str
        :return: a restricted parser, or `None` when no examples match
        :rtype: ExamplesParser | None
        """
        ...
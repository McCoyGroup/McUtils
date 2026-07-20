import pprint, collections, enum
from .. import Devutils as dev
from .. import Numputils as nput
__all__ = ['TreeWrapper', 'tree_traversal', 'tree_iter', 'graph_iter', 'TreeSentinels']

class TreeTraversalOrder(enum.Enum):
    BreadthFirst = 'bfs'
    DepthFirst = 'dfs'

class TreeCallOrder(enum.Enum):
    PreVisit = 'pre'
    PostVisit = 'post'
    PostChildren = 'final'

class TreeSentinels(enum.Enum):
    Stop = 'stop'
    Skip = 'skip'

def _get_tree_children(tree):
    """
    **LLM Docstring**

    Enumerate the immediate entries of a mapping or sequence as `(position, key)` pairs.

    :param tree: The nested container or adjacency structure to traverse.
    :type tree: object

    :return: A list of indexed child descriptors.
    :rtype: list
    """
    ...

def _get_tree_item(tree, item):
    """
    **LLM Docstring**

    Resolve a child descriptor produced by `_get_tree_children` against its parent container.

    :param tree: The nested container or adjacency structure to traverse.
    :type tree: object

    :param item: Index, path, or item to retrieve.
    :type item: object

    :return: The selected child object.
    :rtype: object
    """
    ...

def tree_traversal(tree, callback, root=None, get_item=None, get_children=None, visited: set=None, check_visited=None, traversal_ordering='bfs', call_order='post'):
    """
    **LLM Docstring**

    Traverse a tree or graph-like object and invoke a callback before visiting, after marking, or after queuing each node.

    :param tree: The nested container or adjacency structure to traverse.
    :type tree: object

    :param callback: Function called with traversal context for each visited node.
    :type callback: object

    :param root: Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.
    :type root: object

    :param get_item: Callback resolving a child descriptor into a child node.
    :type get_item: object

    :param get_children: Callback returning child descriptors for a node.
    :type get_children: object

    :param visited: Mutable or per-path set of nodes already seen.
    :type visited: set

    :param check_visited: Whether to suppress already-visited nodes.
    :type check_visited: object

    :param traversal_ordering: Traversal order, `"bfs"` or `"dfs"`.
    :type traversal_ordering: object

    :param call_order: Point at which the callback is invoked relative to child expansion.
    :type call_order: object

    :return: The first non-`None` callback result, or `None` after exhaustion.
    :rtype: object
    """
    ...

def tree_iter(tree, root=None, get_item=None, get_children=None, visited: set=None, check_visited=None, traversal_ordering='bfs', yield_paths=False, per_path_visited=False, enable_disconnectivity=False):
    """
    **LLM Docstring**

    Yield nodes or root-to-node paths from a configurable breadth-first or depth-first traversal.

    :param tree: The nested container or adjacency structure to traverse.
    :type tree: object

    :param root: Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.
    :type root: object

    :param get_item: Callback resolving a child descriptor into a child node.
    :type get_item: object

    :param get_children: Callback returning child descriptors for a node.
    :type get_children: object

    :param visited: Mutable or per-path set of nodes already seen.
    :type visited: set

    :param check_visited: Whether to suppress already-visited nodes.
    :type check_visited: object

    :param traversal_ordering: Traversal order, `"bfs"` or `"dfs"`.
    :type traversal_ordering: object

    :param yield_paths: Whether to yield path records instead of individual traversal payloads.
    :type yield_paths: object

    :param per_path_visited: Whether each queued path receives its own visited-node set instead of mutating one global set.
    :type per_path_visited: object

    :param enable_disconnectivity: Whether terminal paths should search earlier path nodes for skipped branches.
    :type enable_disconnectivity: object

    :return: An interactive generator yielding nodes or paths.
    :rtype: collections.abc.Iterator
    """
    ...

def _get_graph_children_generator(graph):
    """
    **LLM Docstring**

    Create a child lookup closure bound to an adjacency mapping.

    :param graph: Graph object, adjacency matrix, or adjacency mapping used by the operation.
    :type graph: object

    :return: A callable returning `graph[node]`.
    :rtype: object
    """
    ...

def _get_graph_item_generator(graph):
    """
    **LLM Docstring**

    Create the identity child resolver used for adjacency-list graphs.

    :param graph: Graph object, adjacency matrix, or adjacency mapping used by the operation.
    :type graph: object

    :return: A callable that returns each child identifier unchanged.
    :rtype: object
    """
    ...

def graph_iter(graph, root=None, get_item=None, get_children=None, visited: set=None, traversal_ordering='bfs', yield_paths=False, enable_disconnectivity=False):
    """
    **LLM Docstring**

    Adapt an adjacency mapping to `tree_iter`, enabling cycle-safe graph traversal and optional path enumeration.

    :param graph: Graph object, adjacency matrix, or adjacency mapping used by the operation.
    :type graph: object

    :param root: Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.
    :type root: object

    :param get_item: Callback resolving a child descriptor into a child node.
    :type get_item: object

    :param get_children: Callback returning child descriptors for a node.
    :type get_children: object

    :param visited: Mutable or per-path set of nodes already seen.
    :type visited: set

    :param traversal_ordering: Traversal order, `"bfs"` or `"dfs"`.
    :type traversal_ordering: object

    :param yield_paths: Whether to yield path records instead of individual traversal payloads.
    :type yield_paths: object

    :param enable_disconnectivity: Whether terminal paths should search earlier path nodes for skipped branches.
    :type enable_disconnectivity: object

    :return: A configured traversal generator.
    :rtype: collections.abc.Iterator
    """
    ...

class TreeWrapper:

    def __init__(self, tree):
        """
        **LLM Docstring**

        Wrap a nested mapping or sequence with traversal and path-indexing conveniences.

        :param tree: The nested container or adjacency structure to traverse.
        :type tree: object

        :return: No value is returned.
        :rtype: None
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Format the wrapped tree using `pprint.pformat`.

        :return: A concise string representation.
        :rtype: str
        """
        ...

    def __len__(self):
        """
        **LLM Docstring**

        Return the number of top-level entries in the wrapped tree.

        :return: The number of contained elements.
        :rtype: object
        """
        ...

    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over the wrapped container.

        :return: An iterator over contained elements.
        :rtype: collections.abc.Iterator
        """
        ...

    def condense_subtrees(self):
        """
        **LLM Docstring**

        Merge a top-level sequence of mapping subtrees into one mapping when every element is dictionary-like.

        :return: `self` when condensation is not possible, otherwise a new wrapper around the merged mapping.
        :rtype: object
        """
        ...

    def keys(self):
        """
        **LLM Docstring**

        Return mapping keys when the wrapped tree is mapping-like; otherwise return `None`.

        :return: A mapping key view, or `None`.
        :rtype: object
        """
        ...

    def values(self):
        """
        **LLM Docstring**

        Return mapping values or the sequence itself for non-mapping trees.

        :return: A mapping value view or the wrapped sequence.
        :rtype: object
        """
        ...

    def find_subtree(self, key):
        """
        **LLM Docstring**

        Find the first direct subtree associated with one of the requested keys.

        :param key: Index, path, or mapping key selecting an item.
        :type key: object

        :return: The first matching direct subtree, or `None`.
        :rtype: object
        """
        ...

    @classmethod
    def get_tree_item(cls, tree, item):
        """
        **LLM Docstring**

        Follow a path through nested mappings and sequences, translating integer positions into mapping-key order where needed.

        :param tree: The nested container or adjacency structure to traverse.
        :type tree: object

        :param item: Index, path, or item to retrieve.
        :type item: object

        :return: The nested object reached by the path.
        :rtype: object
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Resolve a nested path through the wrapped tree.

        :param item: Index, path, or item to retrieve.
        :type item: object

        :return: The nested object selected by `item`.
        :rtype: object
        """
        ...

    def bfs(self, callback, **opts):
        """
        **LLM Docstring**

        Run `tree_traversal` in breadth-first order.

        :param callback: Function called with traversal context for each visited node.
        :type callback: object

        :param opts: Additional options forwarded to the delegated operation.
        :type opts: object

        :return: The first non-`None` callback result, or `None`.
        :rtype: object
        """
        ...

    def dfs(self, callback, **opts):
        """
        **LLM Docstring**

        Run `tree_traversal` in depth-first order.

        :param callback: Function called with traversal context for each visited node.
        :type callback: object

        :param opts: Additional options forwarded to the delegated operation.
        :type opts: object

        :return: The first non-`None` callback result, or `None`.
        :rtype: object
        """
        ...
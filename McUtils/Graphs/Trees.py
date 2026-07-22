
import pprint, collections, enum

from .. import Devutils as dev
from .. import Numputils as nput

__all__ = ["TreeWrapper", "tree_traversal", "tree_iter", "graph_iter", "TreeSentinels"]

class TreeTraversalOrder(enum.Enum):
    BreadthFirst = 'bfs'
    DepthFirst = 'dfs'

class TreeCallOrder(enum.Enum):
    PreVisit = "pre"
    PostVisit = "post"
    PostChildren = "final"

class TreeSentinels(enum.Enum):
    Stop = "stop"
    Skip = "skip"

def _get_tree_children(tree):
    """
    **LLM Docstring**

    Enumerate the immediate entries of a mapping or sequence as `(position, key)` pairs.

    :param tree: The nested container or adjacency structure to traverse.
    :type tree: object

    :return: A list of indexed child descriptors.
    :rtype: list
    """
    if hasattr(tree, 'keys'):
        return list(enumerate(tree.keys()))
    else:
        return list(enumerate(tree))
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
    return tree[item[1]]
def tree_traversal(tree, callback,
                   root=None,
                   get_item=None,
                   get_children=None,
                   visited:set=None,
                   check_visited=None,
                   traversal_ordering='bfs',
                   call_order='post'
                   ):
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
    if get_children is None and get_item is None:
        get_children, get_item = _get_tree_children, _get_tree_item
    elif get_children is not None and get_item is None:
        raise ValueError("`get_children` must be implemented if `get_item` is provided")
    elif get_children is None and get_item is not None:
        raise ValueError("`get_item` must be implemented if `get_children` is provided")

    if root is dev.default:
        root = get_children(tree)[0]
    if root in visited:
        return

    if check_visited is None:
        check_visited = visited is not None
    if check_visited and visited is None:
        visited = set()

    queue = collections.deque([[None, root]])
    if isinstance(traversal_ordering, str):
        traversal_ordering = TreeTraversalOrder(traversal_ordering)
    if isinstance(call_order, str):
        call_order = TreeCallOrder(call_order)
    if traversal_ordering is traversal_ordering.BreadthFirst:
        pop = queue.popleft
        extend = queue.extend
    else:
        pop = queue.popleft
        extend = queue.extendleft

    while queue:
        parent, head = pop()

        if call_order == TreeCallOrder.PreVisit:
            res = callback(parent, head, visited)
            if res is not None:
                return res

        if check_visited:
            visited.add(head)

        if call_order == TreeCallOrder.PostVisit:
            res = callback(parent, head, visited)
            if res is not None:
                return res

        if check_visited:
            extend(
                [head, get_item(head, h)]
                for h in get_children(head)
                if h not in visited
            )
        else:
            extend(
                [head, get_item(head, h)]
                for h in get_children(head)
            )

        if call_order == TreeCallOrder.PostChildren:
            res = callback(parent, head, visited)
            if res is not None:
                return res

def tree_iter(tree,
              root=None,
              get_item=None,
              get_children=None,
              visited: set = None,
              check_visited=None,
              traversal_ordering='bfs',
              yield_paths=False,
              use_child_paths=None,
              per_path_visited=False,
              enable_disconnectivity=False
              ):
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
    if get_children is None and get_item is None:
        if use_child_paths is None: use_child_paths = True
        get_children, get_item = _get_tree_children, _get_tree_item
    elif get_children is not None and get_item is None:
        raise ValueError("`get_item` must be implemented if `get_children` is provided")
    elif get_children is None and get_item is not None:
        raise ValueError("`get_children` must be implemented if `get_item` is provided")
    else:
        if use_child_paths is None: use_child_paths = False

    if root is dev.default:
        root = get_children(tree)[0]

    if check_visited is None:
        check_visited = visited is not None
    if check_visited and visited is None:
        visited = set()

    if visited is not None and root in visited:
        return

    queue = collections.deque([[None, root, [], visited]])
    if isinstance(traversal_ordering, str):
        traversal_ordering = TreeTraversalOrder(traversal_ordering)
    if traversal_ordering is traversal_ordering.BreadthFirst:
        pop = queue.popleft
        extend = queue.extend
    else:
        #TODO: control how I want the children to be added...FIFO or LIFO
        pop = queue.popleft
        extend = lambda children:queue.extendleft(reversed(list(children)))

    yield_terminal = dev.str_is(yield_paths, 'terminal')

    while queue:
        parent, head, path, visited = pop()
        if yield_paths:
            if yield_terminal:
                res = None
            else:
                res = yield (path, False)
        else:
            res = yield path
        if res is TreeSentinels.Skip:
            continue
        elif res is TreeSentinels.Stop:
            break

        if check_visited:
            if per_path_visited or enable_disconnectivity:
                visited = visited | {head}
            else:
                visited.add(head)

        subtree = tree if head is None else head
        children = list(get_children(subtree))
        if check_visited:
            children = [
                h for h in children
                if h not in visited
            ]
        if yield_paths or enable_disconnectivity:
            if not use_child_paths:
                path = path + [head]
        if len(children) > 0:
            if use_child_paths:
                extend([head, get_item(subtree, h), path + [h], visited] for h in children)
            else:
                extend([head, get_item(subtree, h), path, visited] for h in children)
        elif yield_paths or enable_disconnectivity:
            if enable_disconnectivity:
                # walk down the path from the start to find the first possible branch
                # we skipped
                for p in path:
                    children = list(get_children(p))
                    if check_visited:
                        children = [
                            h for h in children
                            if h not in visited
                        ]
                    children = [
                        h for h in children
                        if h not in path
                    ]
                    if len(children) > 0:
                        if use_child_paths:
                            extend([p, get_item(p, h), path + [h], visited] for h in children)
                        else:
                            extend([p, get_item(p, h), path, visited] for h in children)
                        break
                else:
                    yield (path, True)
            else:
                yield (path, True)

def _get_graph_children_generator(graph):
    """
    **LLM Docstring**

    Create a child lookup closure bound to an adjacency mapping.

    :param graph: Graph object, adjacency matrix, or adjacency mapping used by the operation.
    :type graph: object

    :return: A callable returning `graph[node]`.
    :rtype: object
    """
    def _get_graph_children(head):
        """
        **LLM Docstring**

        Return the neighbors stored for a graph node.

        :param head: The current node whose neighbors or child value are requested.
        :type head: object

        :return: The adjacency entries for `head`.
        :rtype: object
        """
        return graph[head]
    return _get_graph_children
def _get_graph_item_generator(graph):
    """
    **LLM Docstring**

    Create the identity child resolver used for adjacency-list graphs.

    :param graph: Graph object, adjacency matrix, or adjacency mapping used by the operation.
    :type graph: object

    :return: A callable that returns each child identifier unchanged.
    :rtype: object
    """
    def _get_graph_item(head, item):
        """
        **LLM Docstring**

        Return a neighboring node unchanged because graph adjacency entries are already node identifiers.

        :param head: The current node whose neighbors or child value are requested.
        :type head: object

        :param item: Index, path, or item to retrieve.
        :type item: object

        :return: The supplied child identifier.
        :rtype: object
        """
        return item
    return _get_graph_item
def graph_iter(graph,
               root=None,
               get_item=None,
               get_children=None,
               visited: set = None,
               traversal_ordering='bfs',
               yield_paths=False,
               enable_disconnectivity=False
               ):
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
    graph = {
        k:list(v)
        for k, v in graph.items()
    }
    if get_children is None and get_item is None:
        get_children, get_item = _get_graph_children_generator(graph), _get_graph_item_generator(graph)
    return tree_iter(
        graph,
        root=root,
        get_item=get_item,
        get_children=get_children,
        visited=visited,
        check_visited=True,
        per_path_visited=True,
        traversal_ordering=traversal_ordering,
        yield_paths=yield_paths,
        enable_disconnectivity=enable_disconnectivity
    )

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
        self.tree = tree

    def __repr__(self):
        """
        **LLM Docstring**

        Format the wrapped tree using `pprint.pformat`.

        :return: A concise string representation.
        :rtype: str
        """
        fmt_tree = pprint.pformat(self.tree)
        cls = type(self)
        return f"{cls.__name__}({fmt_tree})"
    def __len__(self):
        """
        **LLM Docstring**

        Return the number of top-level entries in the wrapped tree.

        :return: The number of contained elements.
        :rtype: object
        """
        return len(self.tree)
    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over the wrapped container.

        :return: An iterator over contained elements.
        :rtype: collections.abc.Iterator
        """
        return iter(self.tree)
    def condense_subtrees(self):
        """
        **LLM Docstring**

        Merge a top-level sequence of mapping subtrees into one mapping when every element is dictionary-like.

        :return: `self` when condensation is not possible, otherwise a new wrapper around the merged mapping.
        :rtype: object
        """
        if hasattr(self.tree, 'keys') or not all(
            hasattr(t, 'keys') for t in self.tree
        ):
            return self
        else:
            new_tree = self.tree[0]
            for t in self.tree[1:]:
                new_tree = dev.merge_dicts(new_tree, t)
            return type(self)(new_tree)
    def keys(self):
        """
        **LLM Docstring**

        Return mapping keys when the wrapped tree is mapping-like; otherwise return `None`.

        :return: A mapping key view, or `None`.
        :rtype: object
        """
        if hasattr(self.tree, 'keys'):
            return self.tree.keys()
        else:
            return None
    def values(self):
        """
        **LLM Docstring**

        Return mapping values or the sequence itself for non-mapping trees.

        :return: A mapping value view or the wrapped sequence.
        :rtype: object
        """
        if hasattr(self.tree, 'values'):
            return self.tree.values()
        else:
            return self.tree
    def find_subtree(self, key):
        """
        **LLM Docstring**

        Find the first direct subtree associated with one of the requested keys.

        :param key: Index, path, or mapping key selecting an item.
        :type key: object

        :return: The first matching direct subtree, or `None`.
        :rtype: object
        """
        if hasattr(self.tree, 'keys'):
            return self.__getitem__(key)
        else:
            if nput.is_atomic(key):
                key = [key]
            for k in key:
                for n,v in enumerate(self.tree):
                    if dev.is_dict_like(v) and k in v:
                        return v[k]
                    # elif v == k:
                    #     return v
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
        t = tree
        if nput.is_atomic(item):
            item = [item]
        base_exception = None
        for k in item:
            if not isinstance(k, str) and hasattr(t, 'keys'):
                woof = []
                for n,v in enumerate(t.keys()):
                    woof.append(v)
                    if n >= k:
                        break
                else:
                    base_exception = IndexError("index {} not valid for subtree with keys {}".format(
                        k, t.keys()
                    ))
                    break
                k = woof[-1]
            try:
                t = t[k]
            except (IndexError, KeyError, TypeError) as e:
                base_exception = e
                break


        if base_exception is not None:
            raise IndexError(f"{item} not found in tree") from base_exception

        return t
    def __getitem__(self, item):
        """
        **LLM Docstring**

        Resolve a nested path through the wrapped tree.

        :param item: Index, path, or item to retrieve.
        :type item: object

        :return: The nested object selected by `item`.
        :rtype: object
        """
        return self.get_tree_item(self.tree, item)
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
        #TODO: support most sophsticated children/item indexing
        return tree_traversal(self.tree, callback, traversal_ordering='bfs', **opts)
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
        return tree_traversal(self.tree, callback, traversal_ordering='dfs', **opts)
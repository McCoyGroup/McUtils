
import itertools, collections
import scipy.sparse as sparse, numpy as np
from .. import Numputils as nput
from .. import Iterators as itut
from . import Trees as tree

__all__ = [
    "EdgeGraph",
    "MoleculeEdgeGraph"
]

class EdgeGraph:
    __slots__ = ["labels", "edges", "graph", "map"]
    def __init__(self, labels, edges, graph=None, edge_map=None):
        self.labels = labels
        self.edges = np.asanyarray(edges)
        if graph is None:
            graph = self.adj_mat(len(labels), self.edges)
        self.graph = graph
        if edge_map is None:
            edge_map = self.build_edge_map(self.edges)
        self.map = edge_map
        self._rings = None

    @classmethod
    def adj_mat(cls, num_nodes, edges):
        adj = np.zeros((num_nodes, num_nodes), dtype=bool)
        rows,cols = edges.T
        adj[rows, cols] = 1
        adj[cols, rows] = 1

        return sparse.csr_matrix(adj)

    def get_distances(self, indices=None):
        return sparse.csgraph.shortest_path(
            self.graph,
            directed=False,
            unweighted=True,
            indices=indices
        )

    @classmethod
    def build_edge_map(cls, edge_list):
        map = {}
        for e1,e2 in edge_list:
            if e1 not in map: map[e1] = set()
            map[e1].add(e2)
            if e2 not in map: map[e2] = set()
            map[e2].add(e1)
        return map

    @classmethod
    def _remap(cls, labels, pos, rows, cols):
        if len(rows) == 0:
            edge_list = np.array([], dtype=int).reshape(-1, 2)
        else:
            new_mapping = np.zeros(len(labels), dtype=int)
            new_mapping[pos,] = np.arange(len(pos))
            new_row = new_mapping[rows,]
            new_col = new_mapping[cols,]
            edge_list = np.array([new_row, new_col]).T

        return [labels[p] for p in pos], edge_list
    @classmethod
    def _take(cls, pos, labels, adj_mat:sparse.compressed):
        rows, cols, _ = sparse.find(adj_mat)
        utri = cols >= rows
        rows = rows[utri]
        cols = cols[utri]
        row_cont, _, _ = nput.contained(rows, pos)
        col_cont, _, _ = nput.contained(cols, pos)
        cont = np.logical_and(row_cont, col_cont)

        labels, edge_list = cls._remap(labels, pos, rows[cont], cols[cont])
        return cls(labels, edge_list)

    def take(self, pos):
        return self._take(pos, self.labels, self.graph)

    def split(self, backbone_pos):
        new_adj = self.graph.copy()
        for n in backbone_pos:
            for i,j in self.map[n]:
                new_adj[i,j] = 0
        ncomp, labels = sparse.csgraph.connected_components(new_adj, directed=False, return_labels=True)
        groups, _ = nput.group_by(np.arange(len(labels)), labels)
        return [
            self._take(pos, self.labels, new_adj)
            for _, pos in groups
        ]

    @classmethod
    def _subgraph_match(cls,
                        root1, labels1, edge_map1,
                        root2, labels2, edge_map2,
                        visited=None
                        ):
        if labels1[root1] != labels2[root2]:
            return False
        if len(edge_map1.get(root1, [])) != len(edge_map2.get(root2, [])):
            return False

        if visited is None:
            visited = (set(), set())
        visit1, visit2 = visited

        # queue1 = collections.deque([root1])
        tests1 = set(edge_map1.get(root1, [])) - visit1
        tests2 = set(edge_map2.get(root2, [])) - visit2
        for r1 in tests1:
            visit1.add(r1)
            for r2 in tests2:
                visit2.add(r2)
                # check if all the subgraphs match via DFS
                # we could do this without recursion, but it'd be
                # more annoying
                if cls._subgraph_match(
                    r1, labels1, edge_map1,
                    r2, labels2, edge_map2,
                    visited=(visit1, visit2)
                ):
                    tests2.remove(r2)
                    break
                else:
                    visit2.remove(r2)

        return len(tests2) == 0

    @classmethod
    def graph_match(cls, graph1:'EdgeGraph', graph2:'EdgeGraph'):
        # we do some quick prunes
        atoms1 = graph1.labels
        atoms2 = graph2.labels
        if (
                len(atoms1) != len(atoms2)
                or atoms1[0] != atoms2[0]
                or len(graph1.edges) != len(graph2.edges)
                or list(sorted(atoms1)) != list(sorted(atoms2))
                or list(sorted(len(v) for v in graph1.map.values())) != list(sorted(len(v) for v in graph2.map.values()))
        ):
            return False

        return cls._subgraph_match(
            0, graph1.labels, graph1.map,
            0, graph2.labels, graph2.map
        )

    def __eq__(self, other):
        return self.graph_match(self, other)

    @classmethod
    def build_neighborhood_graph(cls, node, labels, edge_map, ignored=None, num=1):
        edges = []
        visited = set()
        if ignored is None: ignored = []
        ignored = set(ignored)
        queue = [node]
        for i in range(num):
            new_queue = []
            for node in queue:
                visited.add(node)
                new_nodes = set(edge_map[node]) - visited - ignored
                edges.extend((node, e) for e in new_nodes)
                new_queue.extend(new_nodes)
            queue = new_queue

        edges = np.array(edges, dtype=int)
        if len(edges) == 0:
            edges = np.reshape(edges, (-1, 2))
        labels, edges = cls._remap(labels, list(visited), edges[:, 0], edges[:, 1])
        return cls(labels, edges)

    def neighbor_graph(self, root, ignored=None, num=1):
        return self.build_neighborhood_graph(root, self.labels, self.map, ignored=ignored, num=num)

    @property
    def rings(self):
        if self._rings is None:
            self._rings = self.get_rings()
        return self._rings
    def get_rings(self):
        # clunky, but it works
        test_rings = []
        for n,l in enumerate(self.labels):
            if len(self.map[n]) < 2: continue
            visited = set()
            test_rings.append(
                tree.tree_traversal(
                    self.map,
                    lambda parent, child, visited: (
                        visited
                            if len(visited & self.map[child]) > 1 else
                        None
                    ),
                    root=n,
                    get_children=lambda h: [c for c in self.map[h] if len(self.map[c]) > 1],
                    get_item=lambda _, h: h,
                    visited=visited,
                    call_order='post',
                    traversal_ordering='bfs'
                )
            )

        filt_rings = [t for t in test_rings if t is not None]

        rings = []
        keys = set()
        for i,r1 in enumerate(filt_rings):
            for r2 in filt_rings[i:]:
                int_ring = r1 & r2
                key = tuple(sorted(int_ring))
                if key in keys: continue
                keys.add(key)
                r = self.check_ring(int_ring)
                if r: rings.append(r)
        return rings


    def check_ring(self, ring_atoms):
        if len(ring_atoms) < 3: return False
        ring_atoms = set(ring_atoms)
        if any(len(self.map[r] & ring_atoms) == 1 for r in ring_atoms): return False
        visited = set()
        root = next(iter(ring_atoms))
        ring = []
        return tree.tree_traversal(
                    self.map,
                    lambda parent, child, visited: (
                        ring + [child]
                            if (parent != root and root in self.map[child]) else
                        ring.append(child)
                    ),
                    root=root,
                    get_children=lambda h: self.map[h] & ring_atoms,
                    get_item=lambda _, h: h,
                    visited=visited,
                    call_order='post',
                    traversal_ordering='dfs'
                )

    def get_fragments(self):
        from scipy.sparse import csgraph
        _, labels = csgraph.connected_components(self.graph, directed=False, return_labels=True)
        _, groups = nput.group_by(np.arange(len(labels)), labels)[0]
        return groups

    @classmethod
    def get_maximum_overlap_permutation(cls, graph_1:'EdgeGraph', graph_2:'EdgeGraph'):
        syms_1 = graph_1.labels
        syms_2 = graph_2.labels

        if any(s_1 != s_2 for s_1, s_2 in zip(syms_1, syms_2)):
            if len(itut.dict_diff(itut.counts(syms_1), itut.counts(syms_2))) > 0:
                raise ValueError(f"graph labels must agree: {syms_1} != {syms_2}")
            ordering_1 = list(sorted(range(len(syms_1)), key=syms_1.__getitem__))
            ordering_2 = list(sorted(range(len(syms_2)), key=syms_2.__getitem__))
            perm_0 = np.array(ordering_2)[np.argsort(ordering_1)]
            graph_2 = graph_2.take(perm_0)
        else:
            perm_0 = None

        bond_set_1 = {tuple(sorted(e)) for e in graph_1.edges}
        bond_set_2 = {tuple(sorted(e)) for e in graph_2.edges}

        # initial bond difference
        test_bonds = np.unique(np.array(
            list(bond_set_1 - bond_set_2)
            + list(bond_set_2 - bond_set_1)
        ))

        # permutable groups
        sym_splits, _ = nput.group_by(np.arange(len(syms_1)), np.array([ord(s) for s in syms_1]))
        perm_blocks = []
        perm_atoms = []
        for _, atom_inds in zip(*sym_splits):
            atom_inds = nput.intersection(atom_inds, test_bonds)[0]  # only permute things in the original core
            if len(atom_inds) > 0:
                perm_atoms.append(atom_inds)
                perm_blocks.append(itertools.permutations(atom_inds))

        nsym = len(syms_1)
        core_size = len(test_bonds)
        perm = np.arange(nsym)
        for full_perm in itertools.product(*perm_blocks):
            reindexing = np.arange(nsym)
            for atom_inds, new_idx in zip(perm_atoms, full_perm):
                reindexing[atom_inds,] = new_idx
            new_bond_set_1 = {
                (reindexing[i], reindexing[j])
                for (i, j) in bond_set_1
            }
            new_core = np.unique(np.array(
                list(new_bond_set_1 - bond_set_2)
                + list(bond_set_2 - new_bond_set_1)
            ))
            if len(new_core) < core_size:
                perm = reindexing

        if perm_0 is not None:
            return perm_0[perm]
        else:
            return perm

    def get_reindexing(self, other_graph):
        return self.get_maximum_overlap_permutation(other_graph, self)
    def align_labels(self, other_graph):
        perm = self.get_reindexing(other_graph)
        return self.take(perm)



class MoleculeEdgeGraph(EdgeGraph):

    def get_rings(self):
        # use rdkit's cycles...not assured to be the smallest set ;_;
        from ..ExternalPrograms.RDKit import RDMolecule
        return RDMolecule.from_coords(
            ["C"]*len(self.labels),
            coords=np.zeros((len(self.labels), 3)),
            bonds=[[int(i), int(j), 1] for i,j in self.edges]
        ).rings

    @classmethod
    def _match_motif(cls, label, neighbors, motif_root, *motif_branches):
        branch_members = set()
        for b in motif_branches:
            branch_members.update(b)
        if label not in branch_members:
            return False
        if label != motif_root:
            for b in motif_branches:
                ...
                # if l
    @classmethod
    def _idenfity_motifs(cls, label, neighbors, index=None, graph=None):
        ...
    @classmethod
    def _make_label(cls, label, neighbors, index=None, graph=None):
        if len(neighbors) == 0: return label
        if isinstance(neighbors[0], str):
            if label == "H":
                if len(neighbors) > 1:
                    return label + cls._format_atom_counts(neighbors)
                else:
                    return neighbors[0] + label
            elif label == "C":
                non_c_neighbors = [l for l in neighbors if l != "C"]
                if len(non_c_neighbors) > 0:
                    neighbors = non_c_neighbors
                elif len(neighbors) > 0:
                    return "C"+str(len(neighbors)+1)
                return label + cls._format_atom_counts(neighbors)
            else:
                non_c_neighbors = [l for l in neighbors if l != "C"]
                if len(non_c_neighbors) > 0:
                    neighbors = non_c_neighbors
                return label + cls._format_atom_counts(neighbors)
        else:
            raise ValueError("can't make atom type for neighbor depth > 2")

    def _collect_neighbor_list(self, root, depth=1, visited=None):
        if visited is None: visited = {root}
        nl = []
        ni = []
        for m in self.map.get(root, []):
            if m in visited: continue
            visited.add(m)
            if depth > 1:
                sublist, subinds = self._collect_neighbor_list(m, depth=depth-1, visited=visited)
                nl.append((self.labels[m], sublist))
                ni.append((m, subinds))
            else:
                nl.append(self.labels[m])
                ni.append(m)
        return tuple(nl), tuple(ni)


    chemical_order = ['C', 'O', 'N', 'H', 'F', 'Cl', 'Br', 'I']
    @classmethod
    def _sort_atom_types(cls, counts, chemical_order=None):
        if chemical_order is None:
            if not isinstance(cls.chemical_order, dict):
                cls.chemical_order = {
                    k:n for n,k in enumerate(cls.chemical_order)
                }
            chemical_order = cls.chemical_order
        elif not hasattr(chemical_order, 'get'):
            chemical_order = {
                k: n for n, k in enumerate(chemical_order)
            }

        if hasattr(counts, "items"):
            return sorted(
                counts.items(),
                key=lambda kv: chemical_order.get(kv[0], len(chemical_order))
            )
        else:
            return sorted(
                counts,
                key=lambda kv: chemical_order.get(kv, len(chemical_order))
            )

    @classmethod
    def _format_atom_counts(cls, neighbors):
        if isinstance(neighbors, dict):
            nbs = neighbors
        else:
            nbs = itut.counts(neighbors)
        return "".join(l+("" if k == 1 else str(k)) for l,k in cls._sort_atom_types(nbs))
    @classmethod
    def _format_ring_counts(cls, neighbors):
        return "[" + cls._format_atom_counts(neighbors) + "]"

    @classmethod
    def _atomlist_match(cls, list_1, list_2):
        count1 = itut.counts(list_1)
        count2 = itut.counts(list_2)
        for g,c in count2.items():
            if g == "_":
                continue
            else:
                c2 = count1.get(g, -1)
                if c2 > c:
                    count1[g] -= c
                    continue
                elif c2 > 0:
                    c -= c2
                    del count1[g]
        return count2.get('_', -1) < sum(count1.values())

    @classmethod
    def _bonding_pattern_matcher(cls, neighbor_lists):
        group_counts = itut.counts(neighbor_lists)
        primary_counts = itut.counts(nl[0] for nl in neighbor_lists)
        def match(test_counts, primary_counts=primary_counts, groups_counts=group_counts):
            if hasattr(test_counts, 'items'): test_counts = test_counts.items()
            unmatched = []
            primary_counts = primary_counts.copy()
            groups_counts = groups_counts.copy()
            # we handle wild cards by keeping track of the excess/unmatched patterns
            for group, count in test_counts:
                if isinstance(group, str):
                    if group == "_":
                        unmatched.append([group, count])
                        continue
                    cur_count = primary_counts.get(group, -1)
                    if cur_count < count:
                        return False
                    elif cur_count > count:
                        primary_counts[group] -= count
                    else:
                        del primary_counts[group]
                else:
                    root, rem = group
                    if root == "_" or any("_" in pat for pat in rem):
                        unmatched.append([group, count])
                        continue
                    cur_count = group_counts.get(group, -1)
                    if cur_count < count:
                        return False
                    elif cur_count > count:
                        groups_counts[group] -= count
                    else:
                        del groups_counts[group]
            # now with what we have left over, we need to match each
            # remaining "wildcard" pattern, in principle we need to do this
            # by taking ever possible combination of rems...but we'll be lazy and
            # do it greedily assuming only a few wild cards
            total_strs = sum(primary_counts.values())
            new_umatched = []
            for group, count in unmatched:
                if isinstance(group, str): #"_"
                    if total_strs >= count:
                        total_strs -= count
                    else:
                        return False
                elif group[0] == '_': # we have to match these last
                    new_umatched.append([group, count])
                else:
                    for g,c in groups_counts.items():
                        if g[0] == group[0]:
                            if cls._atomlist_match(group[1], g[1]):
                                if count >= c:
                                    count -= c
                                    del groups_counts[g]
                                else:
                                    groups_counts[g] -= count
                                    break
                    else:
                        if count > 0:
                            return False

            for group, count in new_umatched:
                for g, c in groups_counts.items():
                    if cls._atomlist_match(group[1], g[1]):
                        if count >= c:
                            count -= c
                            del groups_counts[g]
                        else:
                            groups_counts[g] -= count
                            break
                else:
                    if count > 0:
                        return False

            return True

        return match

    ring_type_dispatch = {
            ((("C", 1),)*6): 'benzene',
            (("C", 1),)*5 +(("N", 0),): 'pyridine',
            (("C", 1), ("C", 1), ("N", 0), ("C", 1), ("C", 1), ("N", 0)): 'pyrazine',
            (("C", 1),)*4 +(("N", 0),): 'pyridine',
            # (("C", ("_",))*4, ("N",)): 'furan',
            # (("C", 5),): self._check_cycloprop_ring,
            # (("C", 5), ("N", 1)): self._check_pyridine,
            # (("C", 4), ("N", 1)): self._check_furan,
            # (("C", 4), ("N", 2)): self._check_pyrazine,
            # (("C", 3), ("N", 2)): self._check_pyrazole,
        }
    def categorize_ring(self, ring):
        ring_atoms = [self.labels[n] for n in ring]
        ring_neighbors = None
        for count_list, name in self.ring_type_dispatch.items():
            nat = len(ring_atoms)
            if len(count_list) < nat: continue
            elem_list = [c[0] for c in count_list]
            for i in range(0, nat):
                perm = [(i+j) % nat for j in range(nat)]
                rats = [ring_atoms[j] for j in perm]
                if rats == elem_list:
                    if ring_neighbors is None:
                        ring_neighbors = [
                            self._collect_neighbor_list(r, visited=set(ring))[0]
                            for r in ring
                        ]
                    # a possible choice, need to see if it matches now
                    rns = [len(ring_neighbors[j]) for j in perm]
                    if all(
                        c==t
                        for (_,c),t in zip(count_list, rns)
                    ):
                        return name, tuple(ring[p] for p in perm)
                    break
            # just to make sure
            # if (
            #         len(count_list) == len(ring_counts)
            #         and all(ring_counts.get(a, -1) == v for a,v in count_list)
            # ):
            #     match = matcher(ring)
            #     if match: return match
        return self._format_ring_counts(ring_atoms), ring

    functional_groups = {
        #TODO: replace this with RDKit identifiers
        ("C", ((("H", ()), 3),)): "methyl",
        ("C", ((("H", ()), 2),)): "ethyl",
        ("C", ((("O", ()), 1), (("O", ("H",)), 1))): "carboxylic acid",
        ("C", ((("O", ()), 2),)): "carboxylate",
        ("C", ((("O", ()), 1),)): "carboxyl",
        ("N", ((("H", ()), 3),)): "amine",
        ("N", ((("H", ()), 2),)): "amide",
        ("N", ((("O", ()), 2),)): "nitro",
        ("N", ((("O", ()), 1),)): "nitrosyl",
        ("O", (("C", 2),)): "ether",
        ("C", ((("O", ()), 1), (("O", ("C",)), 1),)): "ester",
        ("C", (("C", 2), (("O", ()), 1))): "ketone",
        ("O", ((("O", ("H",)), 1),)): "peroxide",
        ("C", ((("C", ("H", "H", "H")), 3),)): "tert-butyl"
    }
    def match_functional_group(self, root, neighbor_lists, cache=None):
        key = (root, neighbor_lists)
        if cache is not None and key in cache:
            return cache[key]
        # group_counts = itut.counts(neighbor_lists)
        # primary_counts = itut.counts(nl[0] for nl in neighbor_lists)
        matcher = self._bonding_pattern_matcher(neighbor_lists)
        for (fg_root, counts), name in self.functional_groups.items():
            if fg_root == root:
                if matcher(counts):
                # if all(
                #         (
                #             primary_counts.get(group, -1) == count
                #                 if isinstance(group, str) else
                #             group_counts.get(group, -1) == count
                #         )
                #         for group, count in counts
                # ):
                    if cache is not None:
                        cache[key] = (name, counts)
                    return (name, counts)
        else:
            if cache is not None:
                cache[key] = None
    def find_functional_groups(self):
        possible_fgs = {fg_root for (fg_root, counts), name in self.functional_groups.items()}
        fgs = []
        for n,l in enumerate(self.labels):
            if l in possible_fgs:
                neighbor_list, neighbor_inds = self._collect_neighbor_list(n, depth=2)
                match = self.match_functional_group(l, neighbor_list)
                if match:
                    name, counts = match
                    map = dict(counts)
                    inds = [n]
                    for nl,ni in zip(neighbor_list, neighbor_inds):
                        if map.get(nl, -1) > 0:
                            map[nl] -= 1
                            inds.extend(itut.flatten(ni))
                        elif map.get(nl[0], -1) > 0:
                            map[nl[0]] -= 1
                            inds.append(ni[0])
                    fgs.append([name, inds])
        return fgs


    atom_identifier = collections.namedtuple(
        "atom_identifier",
        ["ring", "group", "motif", "atom"]
    )
    def _get_identifier(self, n, label_constructor, rings, groups):
        ring = None
        group = None
        atom = self.labels[n]
        if rings is not None:
            for name,r in rings:
                if n in r:
                    ring = name
                    break
        if groups is not None:
            for name,g in groups:
                if n in g:
                    group = name
                    break
        lab = label_constructor(
            atom,
            self._collect_neighbor_list(n, depth=1)[0],
            index=n,
            graph=self
        )

        return self.atom_identifier(ring, group, lab, atom)

    def get_label_types(self,
                        label_constructor=None,
                        use_ring_identifiers=True,
                        use_functional_group_identifiers=True
                        ):
        if label_constructor is None:
            label_constructor = self._make_label

        if use_ring_identifiers:
            ring_identifiers = [
                self.categorize_ring(r)
                for r in self.rings
            ]
        else:
            ring_identifiers = None

        if use_functional_group_identifiers:
            functional_groups = self.find_functional_groups()
        else:
            functional_groups = None

        return [
            self._get_identifier(n, label_constructor, ring_identifiers, functional_groups)
            for n, _ in enumerate(self.labels)
        ]



import itertools
import numpy as np
from .YoungTableaux import YoungTableauxGenerator
from .Permutations import IntegerPartitioner
from .Sequences import stable_factorial_ratio
from .. import Numputils as nput

__all__ = [
    "CharacterTable",
    "symmetric_group_class_sizes",
    "symmetric_group_character_table",
    "dihedral_group_character_table"
]

def check_boundary_strip_sst(vals, sst):
    diffs = []

    # check for 2x2 blocks
    for i,row in enumerate(sst[:-1]):
        if len(diffs) < i+1:
            diffs.append(np.diff(row))
        dd = diffs[i]
        eq_pos = np.where(dd == 0)
        if len(eq_pos) == 0: continue
        for p in eq_pos[0]:
            if len(diffs) < i + 2:
                diffs.append(np.diff(sst[i+1]))
            d2 = diffs[i+1]
            if (
                    len(d2) > p
                    and d2[p] == 0
                    and sst[i][p] == sst[i+1][p]
                    and sst[i][p+1] == sst[i+1][p+1]
            ):
                return False

    # check for connected-ness
    for v in vals:
        pos = []
        for i,r in enumerate(sst):
            j = np.where(r == v)
            if len(j) > 0 and len(j[0]) > 0:
                pos.extend([i,jj] for jj in j[0])
        if len(pos) > 1:
            pos = np.array(pos)
            dm = nput.distance_matrix(pos)
            np.fill_diagonal(dm, 2)
            min_vals = np.min(dm, axis=1)
            if np.max(min_vals) > 1:
                return False

    return True

def _group_size(n, p):
    p, c = np.unique(p, return_counts=True)
    num_terms = np.arange(n+1)[2:]
    denom_terms = sum(
        ([pp]*cc + list(range(cc+1))[2:] for pp, cc in zip(p, c)),
        []
    )
    return stable_factorial_ratio(num_terms, denom_terms)

def symmetric_group_class_sizes(n, partitions=None):
    if partitions is None:
        partitions = reversed(list(itertools.chain(*IntegerPartitioner.partitions(n))))
    return np.array([_group_size(n, p) for p in partitions])

def symmetric_group_character_table(n, tableaux=None, partitions=None, return_partitions=False, return_weights=False):
    if tableaux is None:
        tableaux, _ = YoungTableauxGenerator(n).get_standard_tableaux(return_partitions=True)
        if partitions is None:
            partitions = list(reversed(_))
    characters = []
    if partitions is None:
        partitions = list(reversed(list(itertools.chain(*IntegerPartitioner.partitions(n)))))

    for p in partitions:
        vals = list(range(1, len(p)+1))
        types = np.concatenate([[i + 1] * k for i, k in enumerate(p)])
        subcharacters = []
        for sst_set in tableaux:
            term = 0
            seen = set()
            for sst in zip(*sst_set):
                sst = [types[b,] for b in sst]
                key = tuple(np.concatenate(sst))
                if key in seen: continue
                seen.add(key)
                from McUtils.Formatters import TableFormatter
                cbs = check_boundary_strip_sst(vals, sst)
                # print(cbs)
                # print(TableFormatter("").format(sst))
                if cbs:
                    heights = {}
                    for row in sst:
                        for k in np.unique(row):
                            heights[k] = 1 + heights.get(k, -1)
                    term += (-1)**(sum(heights.values()))
            subcharacters.append(term)
        characters.append(subcharacters)

    ct = np.array(characters).T
    if return_partitions or return_weights:
        res = (ct,)
        if return_partitions:
            res = res + (partitions,)
        if return_weights:
            res = res + (symmetric_group_class_sizes(n, partitions),)
        return res
    else:
        return ct

def cyclic_group_character_table(n):
    table = np.zeros((n, n), dtype=complex)
    table[0] = 1
    inds = np.arange(1, n)[:, np.newaxis] * np.arange(n)[np.newaxis, :]
    table[1:] = np.exp(2j*np.pi*inds/n)
    return table

def dihedral_group_character_table(n, return_conjugacy_classes=False):
    # if n < 3:
    #     raise ValueError("no dihedral group under 3 elements")

    if n == 3:
        return symmetric_group_character_table(3)

    k = (2*n + 9 + 3*(-1)**n) // 4
    table = np.zeros((k, k), dtype=float if n % 2 == 1 else float)
    table[0] = 1

    if n % 2 == 0:
        table[1:4, 0] = 1
        table[4:, 0] = 2
        classes = [
            (0, k) for k in range(1, (n//2)+1)
        ] + [
            (1, 0)
        ] + [
            (1, 1)
        ]

        for j,(a,b) in enumerate(classes):
            if a > 0:
                if b == 0:
                    table[1:4, 1+j] = [-1, 1, -1]
                else:
                    table[1:4, 1+j] = [-1, (-1)**b, (-1)**(b+1)]
            else:
                if b == 1:
                    table[1:4, 1+j] = [1, -1, -1]
                else:
                    table[1:4, 1+j] = [1, (-1)**b, (-1)**(b)]
                table[4:, 1+j] = 2*np.cos(2*np.pi*b*np.arange(1, k-3)/n)
    else:
        table[1:2, 0] = 1
        table[2:, 0] = 2
        classes = [
            (0, k) for k in range(1, (n-1)//2 +1)
        ] + [
            (1, 0)
        ]

        for j,(a,b) in enumerate(classes):
            if a > 0:
                table[1:2, 1 + j] = [-1]
            else:
                table[1:2, 1 + j] = [1]
                table[2:, 1 + j] = 2*np.cos(2*np.pi*b*np.arange(1, k-1)/n)

    if np.sum(np.abs(table - np.round(table))) < 1e-6:
        table = np.round(table).astype(int)

    if return_conjugacy_classes:
        return table, classes
    else:
        return table

def dh_group_character_table(n):
    if n % 2 == 1:
        table = np.zeros((n+3, n+3), dtype=float)
        table[0] = 1
        table[1] = 1
        k = (n + 1) // 2
        table[1, k] = -1
        table[1, -1] = -1
        m = (n - 1) // 2
        inds = np.arange(1, m+1)[:, np.newaxis] * np.arange(m+1)[np.newaxis, :]
        j = (n+3)//2
        table[2:j, :m+1] = 2*np.cos(2*np.pi*inds/n)
        table[2:j, m+2:-1] = table[2:j, :m+1]
        table[j:] = table[:j] @ np.diag(np.concatenate([np.ones(j), -np.ones(j)]))
    else:
        table = np.zeros((n+6, n+6), dtype=float)
        table[:2] = 1
        k = n // 2
        table[1, k+1:k+3] = -1
        table[1, -2:] = -1

        table[2, :k+1] = (-1)**np.arange(k+1)
        table[2, k+2] = -1
        table[2, -1] = -1
        table[2, k+1] = 1
        table[2, -2] = 1
        table[2, k+3:2*k+4] = table[2, :k+1]

        table[3] = table[2]
        table[3, k+2] = 1
        table[3, -1] = 1
        table[3, k+1] = -1
        table[3, -2] = -1

        inds = np.arange(1, k)[:, np.newaxis] * np.arange(k+1)[np.newaxis, :]
        table[4:4+k-1, :k+1] = 2*np.cos(2*np.pi*inds/n)
        table[4:4+k-1, k+3:2*k+4] = table[4:4+k-1, :k+1]

        table[4+k-1:] = table[:4+k-1] @ np.diag(np.concatenate([np.ones(k+3), -np.ones(k+3)]))

    if np.sum(np.abs(table - np.round(table))) < 1e-6:
        table = np.round(table).astype(int)

    return table

def dd_group_character_table(n):
    if n % 2 == 1:
        return dh_group_character_table(n)
    else:
        return dihedral_group_character_table(8)

def improper_rotation_group_character_table(n):
    if n % 2 == 1:
        raise ValueError("improper rotation groups must be even")
    if n % 4 == 0:
        table = np.zeros((n, n), dtype=complex)
        table[0] = 1
        table[1] = (-1)**np.arange(n)
        inds = np.arange(1, n//2)[:, np.newaxis] * np.arange(n)[np.newaxis, :]
        table[2::2] = np.exp(inds*2j*np.pi/n)
        table[3::2] = np.exp(-inds*2j*np.pi/n)
    else:
        table = np.zeros((n, n), dtype=complex)
        table[0] = 1
        inds = np.arange(1, (n-2)//4 + 1)[:, np.newaxis] * np.arange(n)[np.newaxis, :]
        m = n//2
        table[1:m:2] = np.exp(inds*4j*np.pi/n)
        table[2:m:2] = np.exp(-inds*4j*np.pi/n)
        table[m:] = table[:m] @ np.diag(np.concatenate([np.ones(m), -np.ones(m)]))
    return table

def ch_group_character_table(n):
    # rewrite in terms of diag
    table = np.zeros((2*n, 2*n), dtype=complex)
    table[0] = 1
    inds = np.arange(1, n)[:, np.newaxis] * np.arange(2*n)[np.newaxis, :]
    table[1:n] = np.exp(inds*2j*np.pi/n)
    table[n:] = table[:n] @ np.diag(np.concatenate([np.ones(n), -np.ones(n)]))
    return table


point_group_map = {
    'Cv':dihedral_group_character_table,
    'S':improper_rotation_group_character_table,
    'Dh':dh_group_character_table,
    "Dd":dd_group_character_table,
    "Ch":ch_group_character_table,
    "C":cyclic_group_character_table
}

def point_group_character_table(key, n, **etc):
    return point_group_map[key](n, **etc)

def I_point_group():
    return np.array([
        [1, 1, 1, 1, 1],
        [3, 2 * np.cos(np.pi / 5), 2 * np.cos((3 * np.pi) / 5), 0, -1],
        [3, 2 * np.cos((3 * np.pi) / 5), 2 * np.cos(np.pi / 5), 0, -1],
        [4, -1, -1, 1, 0],
        [5, 0, 0, -1, 1]
    ])

def Ih_point_group():
    return np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [3, 2 * np.cos(np.pi / 5), 2 * np.cos((3 * np.pi) / 5), 0, -1, 3, 2 * np.cos((3 * np.pi) / 5),
         2 * np.cos(np.pi / 5), 0, -1],
        [3, 2 * np.cos((3 * np.pi) / 5), 2 * np.cos(np.pi / 5), 0, -1, 3, 2 * np.cos(np.pi / 5),
         2 * np.cos((3 * np.pi) / 5), 0, -1],
        [4, -1, -1, 1, 0, 4, -1, -1, 1, 0],
        [5, 0, 0, -1, 1, 5, 0, 0, -1, 1],
        [1, 1, 1, 1, 1, -1, -1, -1, -1, -1],
        [3, 2 * np.cos(np.pi / 5), 2 * np.cos((3 * np.pi) / 5), 0, -1, -3, -2 * np.cos((3 * np.pi) / 5),
         -2 * np.cos(np.pi / 5), 0, 1],
        [3, 2 * np.cos((3 * np.pi) / 5), 2 * np.cos(np.pi / 5), 0, -1, -3, -2 * np.cos(np.pi / 5),
         -2 * np.cos((3 * np.pi) / 5), 0, 1],
        [4, -1, -1, 1, 0, -4, 1, 1, -1, 0],
        [5, 0, 0, -1, 1, -5, 0, 0, 1, -1]
    ])

def O_point_group():
    return np.array([
        [1, 1, 1, 1, 1],
        [1, -1, 1, 1, -1],
        [2, 0, 2, -1, 0],
        [3, 1, -1, 0, -1],
        [3, -1, -1, 0, 1]
    ])

def Oh_point_group():
    return np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, -1, -1, 1, 1, -1, 1, 1, -1],
        [2, -1, 0, 0, 2, 2, 0, -1, 2, 0],
        [3, 0, -1, 1, -1, 3, 1, 0, -1, -1],
        [3, 0, 1, -1, -1, 3, -1, 0, -1, 1],
        [1, 1, 1, 1, 1, -1, -1, -1, -1, -1],
        [1, 1, -1, -1, 1, -1, 1, -1, -1, 1],
        [2, -1, 0, 0, 2, -2, 0, 1, -2, 0],
        [3, 0, -1, 1, -1, -3, -1, 0, 1, 1],
        [3, 0, 1, -1, -1, -3, 1, 0, 1, -1]
    ])

def T_point_group():
    return np.array([
        [1, 1, 1, 1],
        [1, np.exp((2j * np.pi) / 3), np.exp(-((2j * np.pi) / 3)), 1],
        [1, np.exp(-((2j * np.pi) / 3)), np.exp((2j * np.pi) / 3), 1],
        [3, 0, 0, -1]
    ])

def Td_point_group():
    return np.array([
        [1, 1, 1, 1, 1],
        [1, 1, 1, -1, -1],
        [2, -1, 2, 0, 0],
        [3, 0, -1, 1, -1],
        [3, 0, -1, -1, 1]
    ])

def Th_point_group():
    return np.array([
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, np.exp((2j * np.pi) / 3), np.exp(-((2j * np.pi) / 3)), 1, 1, np.exp((2j * np.pi) / 3),
         np.exp(-((2j * np.pi) / 3)), 1],
        [1, np.exp(-((2j * np.pi) / 3)), np.exp((2j * np.pi) / 3), 1, 1, np.exp(-((2j * np.pi) / 3)),
         np.exp((2j * np.pi) / 3), 1],
        [3, 0, 0, -1, 3, 0, 0, -1],
        [1, 1, 1, 1, -1, -1, -1, -1],
        [1, np.exp((2j * np.pi) / 3), np.exp(-((2j * np.pi) / 3)), 1, -1, -np.exp((2j * np.pi) / 3),
         -np.exp(-((2j * np.pi) / 3)), -1],
        [1, np.exp(-((2j * np.pi) / 3)), np.exp((2j * np.pi) / 3), 1, -1, -np.exp(-((2j * np.pi) / 3)),
         -np.exp((2j * np.pi) / 3), -1],
        [3, 0, 0, -1, -3, 0, 0, 1]
    ])


fixed_size_point_group_map = {
    'I': I_point_group,
    "Ih": Ih_point_group,
    "O": O_point_group,
    "Oh": Oh_point_group,
    "T": T_point_group,
    "Td": Td_point_group,
    "Th": Th_point_group
}


def fixed_size_point_group_character_table(key, **etc):
    return fixed_size_point_group_map[key](**etc)

class CharacterTable:
    def __init__(self, characters, group_name=None, classes=None, irrep_names=None):
        self.table = np.asanyarray(characters)
        if np.issubdtype(self.table.dtype, np.dtype(complex)):
            col_weights = np.real(nput.vec_dots(self.table.T, np.conj(self.table.T)))
        else:
            col_weights = nput.vec_dots(self.table.T, self.table.T)
        self.group_order = col_weights[0]
        self.class_sizes = col_weights[0] // col_weights
        self.group_name = group_name
        self.classes = classes
        self.irrep_names = irrep_names

    @classmethod
    def symmetric_group(cls, n):
        chars, parts = symmetric_group_character_table(n, return_partitions=True)
        return cls(
            chars,
            group_name=f"S_{n}",
            classes=[
                "".join(f"{x}[{c}]" for x, c in zip(*np.unique(p, return_counts=True)))
                for p in parts
            ]
        )

    @classmethod
    def cyclic_group(cls, n):
        return cls(
            cyclic_group_character_table(n),
            group_name=f"C_{n}",
            classes=[str(i) for i in range(n)]
        )

    @classmethod
    def dihedral_group(cls, n):
        return cls(
            dihedral_group_character_table(n),
            group_name=f"D_{n}",
            # classes=[str(i) for i in range(n)]
        )

    @classmethod
    def improper_rotation_group(cls, n):
        return cls(
            improper_rotation_group_character_table(n),
            group_name=f"s_{n}",
            # classes=[str(i) for i in range(n)]
        )

    @classmethod
    def point_group(cls, key, n):
        return cls(
            point_group_character_table(key, n),
            group_name=f"{key}_{n}",
            # classes=[str(i) for i in range(n)]
        )

    @classmethod
    def fixed_size_point_group(cls, key):
        return cls(
            fixed_size_point_group_character_table(key),
            group_name=key
            # classes=[str(i) for i in range(n)]
        )

    @classmethod
    def format_character_table(self, table, group_name=None, classes=None, irrep_names=None):
        from ..Formatters import TableFormatter

        table = np.asanyarray(table)
        dtype = table.dtype
        col_types = ["{:.0f}" if np.issubdtype(dtype, np.dtype(int)) else "{:.3f}"] * len(table[0])

        table = table.tolist()
        if group_name is not None:
            if irrep_names is None:
                irrep_names = [""] * len(table)
            if classes is None:
                classes = [""] * len(table[0])

        if irrep_names is not None:
            table = [
                [i] + t
                for i,t in zip(irrep_names, table)
            ]


        return TableFormatter(
            ([""] if irrep_names is not None else []) + col_types,
            headers=([group_name] + classes) if group_name is not None else classes,
            column_join=[" | "] + [" "]*len(table[0]) if irrep_names is not None else None
        ).format(table)

    def format(self, classes=None, irrep_names=None, group_name=None):
        if classes is None:
            classes = self.classes
        if irrep_names is None:
            irrep_names = self.irrep_names
        if group_name is None:
            group_name = self.group_name
        return self.format_character_table(
            self.table,
            group_name=group_name,
            classes=classes,
            irrep_names=irrep_names
        )

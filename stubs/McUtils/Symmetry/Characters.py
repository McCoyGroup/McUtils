import itertools
import numpy as np
from .. import Combinatorics as comb
from .. import Numputils as nput
__all__ = ['CharacterTable', 'symmetric_group_class_sizes', 'symmetric_group_character_table', 'point_group_data']

def check_boundary_strip_sst(vals, sst):
    """
    **LLM Docstring**

    Test whether a labeled skew tableau forms valid connected boundary strips without any `2 x 2` block.

    :param vals: Strip labels whose connectedness is checked.
    :type vals: object
    :param sst: Candidate skew standard tableau represented as rows.
    :type sst: object
    :return: A Boolean indicating whether all strips satisfy the boundary-strip conditions.
    :rtype: bool
    """
    ...

def _group_size(n, p):
    """
    **LLM Docstring**

    Compute the size of a symmetric-group conjugacy class from its cycle partition using a stable factorial ratio.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :param p: Partition or cycle-type data.
    :type p: object
    :return: The conjugacy-class size.
    :rtype: int
    """
    ...

def symmetric_group_class_sizes(n, partitions=None):
    """
    **LLM Docstring**

    Compute conjugacy-class sizes for every supplied partition of `S_n`.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :param partitions: Integer partitions that define conjugacy classes. Defaults to `None`.
    :type partitions: object
    :return: An array of class sizes in partition order.
    :rtype: np.ndarray
    """
    ...

def symmetric_group_character_table(n, tableaux=None, partitions=None, return_partitions=False, return_weights=False):
    """
    **LLM Docstring**

    Construct the symmetric-group character table with the Murnaghan–Nakayama rule over standard Young tableaux.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :param tableaux: Standard Young tableaux used for the Murnaghan–Nakayama construction. Defaults to `None`.
    :type tableaux: object
    :param partitions: Integer partitions that define conjugacy classes. Defaults to `None`.
    :type partitions: object
    :param return_partitions: Value used as `return_partitions` by the implementation. Defaults to `False`.
    :type return_partitions: object
    :param return_weights: Value used as `return_weights` by the implementation. Defaults to `False`.
    :type return_weights: object
    :return: The character table, optionally followed by partitions and class weights.
    :rtype: np.ndarray | tuple
    """
    ...

def cyclic_group_character_table(n):
    """
    **LLM Docstring**

    Construct the hard-coded or analytic character table for the `cyclic_group` group family.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: The square character table with irreducible representations along rows.
    :rtype: np.ndarray
    """
    ...

def cyclic_permutations(n):
    """
    **LLM Docstring**

    Generate permutation representatives for the requested cyclic action.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: An integer array whose rows are permutations.
    :rtype: np.ndarray
    """
    ...

def cyclic_group_classes(n):
    """
    **LLM Docstring**

    Generate permutation representatives and conjugacy-class index groups for the requested point-group family.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: A pair containing all permutation representatives and lists or arrays of class indices.
    :rtype: tuple[np.ndarray, list[np.ndarray]]
    """
    ...

def cyclic_group_operation_representation(n, elements=None, check_mod=True):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
    :type elements: object
    :param check_mod: Value used as `check_mod` by the implementation. Defaults to `True`.
    :type check_mod: object
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def cyclic_group_irrep_names(n):
    """
    **LLM Docstring**

    Generate irreducible-representation labels in the same order as the corresponding character table.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: The ordered representation names.
    :rtype: list[str]
    """
    ...

def dihedral_group_character_table(n):
    """
    **LLM Docstring**

    Construct the hard-coded or analytic character table for the `dihedral_group` group family.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: The square character table with irreducible representations along rows.
    :rtype: np.ndarray
    """
    ...

def dihedral_group_classes(n):
    """
    **LLM Docstring**

    Generate permutation representatives and conjugacy-class index groups for the requested point-group family.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: A pair containing all permutation representatives and lists or arrays of class indices.
    :rtype: tuple[np.ndarray, list[np.ndarray]]
    """
    ...

def dihedral_group_operation_representation(n, elements=None):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
    :type elements: object
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def cv_group_irrep_names(n):
    """
    **LLM Docstring**

    Generate irreducible-representation labels in the same order as the corresponding character table.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: The ordered representation names.
    :rtype: list[str]
    """
    ...

def d_group_matrices(n, elements=None):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
    :type elements: object
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def dh_group_character_table(n):
    """
    **LLM Docstring**

    Construct the hard-coded or analytic character table for the `dh_group` group family.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: The square character table with irreducible representations along rows.
    :rtype: np.ndarray
    """
    ...

def dh_group_classes(n):
    """
    **LLM Docstring**

    Generate permutation representatives and conjugacy-class index groups for the requested point-group family.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: A pair containing all permutation representatives and lists or arrays of class indices.
    :rtype: tuple[np.ndarray, list[np.ndarray]]
    """
    ...

def dh_group_matrices(n, elements=None):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
    :type elements: object
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def dh_group_names(n):
    """
    **LLM Docstring**

    Generate irreducible-representation labels in the same order as the corresponding character table.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: The ordered representation names.
    :rtype: list[str]
    """
    ...

def dd_group_character_table(n):
    """
    **LLM Docstring**

    Construct the hard-coded or analytic character table for the `dd_group` group family.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: The square character table with irreducible representations along rows.
    :rtype: np.ndarray
    """
    ...

def dd_group_classes(n):
    """
    **LLM Docstring**

    Generate permutation representatives and conjugacy-class index groups for the requested point-group family.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: A pair containing all permutation representatives and lists or arrays of class indices.
    :rtype: tuple[np.ndarray, list[np.ndarray]]
    """
    ...

def dd_group_matrices(n, elements=None):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
    :type elements: object
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def dd_group_names(n):
    """
    **LLM Docstring**

    Generate irreducible-representation labels in the same order as the corresponding character table.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: The ordered representation names.
    :rtype: list[str]
    """
    ...

def _permutation_product(perms_lists):
    """
    **LLM Docstring**

    Yield direct-product permutations by shifting disjoint permutation blocks and concatenating one choice from each block.

    :param perms_lists: Collections of permutations acting on disjoint index blocks.
    :type perms_lists: object
    :return: An iterator over combined permutations.
    :rtype: typing.Iterator[np.ndarray]
    """
    ...

def cycle_decomposition_permutation_product(n):
    """
    **LLM Docstring**

    Construct a permutation representation from cyclic factors derived from the prime factorization of `n`.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: The combined permutation array.
    :rtype: np.ndarray
    """
    ...

def improper_rotation_group_character_table(n):
    """
    **LLM Docstring**

    Construct the hard-coded or analytic character table for the `improper_rotation_group` group family.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: The square character table with irreducible representations along rows.
    :rtype: np.ndarray
    """
    ...

def improper_rotation_group_classes(n):
    """
    **LLM Docstring**

    Generate permutation representatives and conjugacy-class index groups for the requested point-group family.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: A pair containing all permutation representatives and lists or arrays of class indices.
    :rtype: tuple[np.ndarray, list[np.ndarray]]
    """
    ...

def improper_rotation_group_operation_representation(n, elements=None):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
    :type elements: object
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def improper_rotation_group_names(n):
    """
    **LLM Docstring**

    Generate irreducible-representation labels in the same order as the corresponding character table.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: The ordered representation names.
    :rtype: list[str]
    """
    ...

def ch_group_character_table(n):
    """
    **LLM Docstring**

    Construct the hard-coded or analytic character table for the `ch_group` group family.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: The square character table with irreducible representations along rows.
    :rtype: np.ndarray
    """
    ...

def ch_group_classes(n):
    """
    **LLM Docstring**

    Generate permutation representatives and conjugacy-class index groups for the requested point-group family.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: A pair containing all permutation representatives and lists or arrays of class indices.
    :rtype: tuple[np.ndarray, list[np.ndarray]]
    """
    ...

def ch_group_matrices(n, elements=None):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
    :type elements: object
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def ch_group_names(n):
    """
    **LLM Docstring**

    Generate irreducible-representation labels in the same order as the corresponding character table.

    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :return: The ordered representation names.
    :rtype: list[str]
    """
    ...

def parametrized_point_group_character_table(key, n, **etc):
    """
    **LLM Docstring**

    Construct the hard-coded or analytic character table for the `parametrized_point_group` group family.

    :param key: Point-group family key or fixed group name.
    :type key: object
    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :param etc: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
    :type etc: dict
    :return: The square character table with irreducible representations along rows.
    :rtype: np.ndarray
    """
    ...

def parametrized_point_group_classes(key, n, **etc):
    """
    **LLM Docstring**

    Generate permutation representatives and conjugacy-class index groups for the requested point-group family.

    :param key: Point-group family key or fixed group name.
    :type key: object
    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :param etc: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
    :type etc: dict
    :return: A pair containing all permutation representatives and lists or arrays of class indices.
    :rtype: tuple[np.ndarray, list[np.ndarray]]
    """
    ...

def parametrized_point_group_matrices(key, n, **etc):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param key: Point-group family key or fixed group name.
    :type key: object
    :param n: Group order or problem size used to construct the requested representation.
    :type n: object
    :param etc: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
    :type etc: dict
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def I_point_group():
    """
    **LLM Docstring**

    Construct the hard-coded or analytic character table for the `I` group family.

    :return: The square character table with irreducible representations along rows.
    :rtype: np.ndarray
    """
    ...

def I_group_classes():
    """
    **LLM Docstring**

    Generate permutation representatives and conjugacy-class index groups for the requested point-group family.

    :return: A pair containing all permutation representatives and lists or arrays of class indices.
    :rtype: tuple[np.ndarray, list[np.ndarray]]
    """
    ...

def I_group_matrices(elements=None):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
    :type elements: object
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def I_group_names():
    """
    **LLM Docstring**

    Generate irreducible-representation labels in the same order as the corresponding character table.

    :return: The ordered representation names.
    :rtype: list[str]
    """
    ...

def Ih_point_group():
    """
    **LLM Docstring**

    Construct the hard-coded or analytic character table for the `Ih` group family.

    :return: The square character table with irreducible representations along rows.
    :rtype: np.ndarray
    """
    ...

def Ih_group_classes():
    """
    **LLM Docstring**

    Generate permutation representatives and conjugacy-class index groups for the requested point-group family.

    :return: A pair containing all permutation representatives and lists or arrays of class indices.
    :rtype: tuple[np.ndarray, list[np.ndarray]]
    """
    ...

def Ih_group_matrices(elements=None):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
    :type elements: object
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def Ih_group_names():
    """
    **LLM Docstring**

    Generate irreducible-representation labels in the same order as the corresponding character table.

    :return: The ordered representation names.
    :rtype: list[str]
    """
    ...

def O_point_group():
    """
    **LLM Docstring**

    Construct the hard-coded or analytic character table for the `O` group family.

    :return: The square character table with irreducible representations along rows.
    :rtype: np.ndarray
    """
    ...

def O_group_classes():
    """
    **LLM Docstring**

    Generate permutation representatives and conjugacy-class index groups for the requested point-group family.

    :return: A pair containing all permutation representatives and lists or arrays of class indices.
    :rtype: tuple[np.ndarray, list[np.ndarray]]
    """
    ...

def O_group_matrices(elements=None):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
    :type elements: object
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def O_group_names():
    """
    **LLM Docstring**

    Generate irreducible-representation labels in the same order as the corresponding character table.

    :return: The ordered representation names.
    :rtype: list[str]
    """
    ...

def Oh_point_group():
    """
    **LLM Docstring**

    Construct the hard-coded or analytic character table for the `Oh` group family.

    :return: The square character table with irreducible representations along rows.
    :rtype: np.ndarray
    """
    ...

def Oh_group_classes():
    """
    **LLM Docstring**

    Generate permutation representatives and conjugacy-class index groups for the requested point-group family.

    :return: A pair containing all permutation representatives and lists or arrays of class indices.
    :rtype: tuple[np.ndarray, list[np.ndarray]]
    """
    ...

def Oh_group_matrices(elements=None):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
    :type elements: object
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def Oh_group_names():
    """
    **LLM Docstring**

    Generate irreducible-representation labels in the same order as the corresponding character table.

    :return: The ordered representation names.
    :rtype: list[str]
    """
    ...

def T_point_group():
    """
    **LLM Docstring**

    Construct the hard-coded or analytic character table for the `T` group family.

    :return: The square character table with irreducible representations along rows.
    :rtype: np.ndarray
    """
    ...

def T_group_classes():
    """
    **LLM Docstring**

    Generate permutation representatives and conjugacy-class index groups for the requested point-group family.

    :return: A pair containing all permutation representatives and lists or arrays of class indices.
    :rtype: tuple[np.ndarray, list[np.ndarray]]
    """
    ...

def T_group_matrices(elements=None):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
    :type elements: object
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def T_group_names():
    """
    **LLM Docstring**

    Generate irreducible-representation labels in the same order as the corresponding character table.

    :return: The ordered representation names.
    :rtype: list[str]
    """
    ...

def Td_point_group():
    """
    **LLM Docstring**

    Construct the hard-coded or analytic character table for the `Td` group family.

    :return: The square character table with irreducible representations along rows.
    :rtype: np.ndarray
    """
    ...

def Td_group_classes():
    """
    **LLM Docstring**

    Generate permutation representatives and conjugacy-class index groups for the requested point-group family.

    :return: A pair containing all permutation representatives and lists or arrays of class indices.
    :rtype: tuple[np.ndarray, list[np.ndarray]]
    """
    ...

def Td_group_matrices(elements=None):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
    :type elements: object
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def Td_group_names():
    """
    **LLM Docstring**

    Generate irreducible-representation labels in the same order as the corresponding character table.

    :return: The ordered representation names.
    :rtype: list[str]
    """
    ...

def Th_point_group():
    """
    **LLM Docstring**

    Construct the hard-coded or analytic character table for the `Th` group family.

    :return: The square character table with irreducible representations along rows.
    :rtype: np.ndarray
    """
    ...

def Th_group_classes():
    """
    **LLM Docstring**

    Generate permutation representatives and conjugacy-class index groups for the requested point-group family.

    :return: A pair containing all permutation representatives and lists or arrays of class indices.
    :rtype: tuple[np.ndarray, list[np.ndarray]]
    """
    ...

def Th_group_matrices(elements=None):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param elements: Selected group elements or element indices; `None` requests the full set. Defaults to `None`.
    :type elements: object
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def Th_group_names():
    """
    **LLM Docstring**

    Generate irreducible-representation labels in the same order as the corresponding character table.

    :return: The ordered representation names.
    :rtype: list[str]
    """
    ...

def fixed_size_point_group_character_table(key, **etc):
    """
    **LLM Docstring**

    Construct the hard-coded or analytic character table for the `fixed_size_point_group` group family.

    :param key: Point-group family key or fixed group name.
    :type key: object
    :param etc: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
    :type etc: dict
    :return: The square character table with irreducible representations along rows.
    :rtype: np.ndarray
    """
    ...

def fixed_size_point_group_classes(key, **etc):
    """
    **LLM Docstring**

    Generate permutation representatives and conjugacy-class index groups for the requested point-group family.

    :param key: Point-group family key or fixed group name.
    :type key: object
    :param etc: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
    :type etc: dict
    :return: A pair containing all permutation representatives and lists or arrays of class indices.
    :rtype: tuple[np.ndarray, list[np.ndarray]]
    """
    ...

def fixed_size_point_group_matrices(key, **etc):
    """
    **LLM Docstring**

    Build the three-dimensional Cartesian matrix representation for selected group elements.

    :param key: Point-group family key or fixed group name.
    :type key: object
    :param etc: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
    :type etc: dict
    :return: An array of shape `(n_elements, 3, 3)`.
    :rtype: np.ndarray
    """
    ...

def point_group_data(key, n=None, prop=None, **etc):
    """
    **LLM Docstring**

    Look up fixed-size or parametrized point-group generators and optionally evaluate one requested property.

    :param key: Point-group family key or fixed group name.
    :type key: object
    :param n: Group order or problem size used to construct the requested representation. Defaults to `None`.
    :type n: object
    :param prop: Value used as `prop` by the implementation. Defaults to `None`.
    :type prop: object
    :param etc: Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
    :type etc: dict
    :return: The group-data mapping, a generated property, or `None` for an unavailable property.
    :rtype: dict | object | None
    """
    ...

class CharacterTable:

    def __init__(self, characters, group_name=None, class_names=None, irrep_names=None, permutations=None, classes=None, matrices=None):
        """
        **LLM Docstring**

        Store a character table and derive its group order and conjugacy-class sizes from column norms.

        :param characters: Character table values with irreducible representations along rows.
        :type characters: object
        :param group_name: Optional label for the group. Defaults to `None`.
        :type group_name: object
        :param class_names: Value used as `class_names` by the implementation. Defaults to `None`.
        :type class_names: object
        :param irrep_names: Optional irreducible-representation labels. Defaults to `None`.
        :type irrep_names: object
        :param permutations: Atom permutations for each symmetry operation. Defaults to `None`.
        :type permutations: object
        :param classes: Conjugacy-class definitions or display labels. Defaults to `None`.
        :type classes: object
        :param matrices: Value used as `matrices` by the implementation. Defaults to `None`.
        :type matrices: object
        :return: No value is returned.
        :rtype: None
        """
        ...

    @classmethod
    def symmetric_group(cls, n):
        """
        **LLM Docstring**

        Construct a `CharacterTable` for the requested symmetric group using the module-level generators.

        :param n: Group order or problem size used to construct the requested representation.
        :type n: object
        :return: The populated character-table object.
        :rtype: CharacterTable
        """
        ...

    @classmethod
    def cyclic_group(cls, n):
        """
        **LLM Docstring**

        Construct a `CharacterTable` for the requested cyclic group using the module-level generators.

        :param n: Group order or problem size used to construct the requested representation.
        :type n: object
        :return: The populated character-table object.
        :rtype: CharacterTable
        """
        ...

    @classmethod
    def dihedral_group(cls, n):
        """
        **LLM Docstring**

        Construct a `CharacterTable` for the requested dihedral group using the module-level generators.

        :param n: Group order or problem size used to construct the requested representation.
        :type n: object
        :return: The populated character-table object.
        :rtype: CharacterTable
        """
        ...

    @classmethod
    def improper_rotation_group(cls, n):
        """
        **LLM Docstring**

        Construct a `CharacterTable` for the requested improper rotation group using the module-level generators.

        :param n: Group order or problem size used to construct the requested representation.
        :type n: object
        :return: The populated character-table object.
        :rtype: CharacterTable
        """
        ...

    @classmethod
    def point_group(cls, key, n=None):
        """
        **LLM Docstring**

        Construct a `CharacterTable` for the requested point group using the module-level generators.

        :param key: Point-group family key or fixed group name.
        :type key: object
        :param n: Group order or problem size used to construct the requested representation. Defaults to `None`.
        :type n: object
        :return: The populated character-table object.
        :rtype: CharacterTable
        """
        ...

    @classmethod
    def fixed_size_point_group(cls, key):
        """
        **LLM Docstring**

        Construct the hard-coded or analytic character table for the `fixed_size` group family.

        :param key: Point-group family key or fixed group name.
        :type key: object
        :return: The square character table with irreducible representations along rows.
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def format_character_table(self, table, group_name=None, classes=None, irrep_names=None):
        """
        **LLM Docstring**

        Construct the hard-coded or analytic character table for the `format` group family.

        :param table: Character table to format.
        :type table: object
        :param group_name: Optional label for the group. Defaults to `None`.
        :type group_name: object
        :param classes: Conjugacy-class definitions or display labels. Defaults to `None`.
        :type classes: object
        :param irrep_names: Optional irreducible-representation labels. Defaults to `None`.
        :type irrep_names: object
        :return: The square character table with irreducible representations along rows.
        :rtype: np.ndarray
        """
        ...

    @property
    def group_key(self):
        """
        **LLM Docstring**

        Convert stored group metadata into a compact point-group key such as `C3v`.

        :return: The normalized group key, or `None` when unnamed.
        :rtype: str | None
        """
        ...

    @classmethod
    def symmetry_symbol(cls, primary_axis, secondary_axis, type, axis, root, order):
        """
        **LLM Docstring**

        Translate a classified Cartesian transformation into a conventional symmetry-operation symbol.

        :param primary_axis: Primary molecular symmetry axis.
        :type primary_axis: object
        :param secondary_axis: Secondary reference axis.
        :type secondary_axis: object
        :param type: Cartesian transformation type code.
        :type type: object
        :param axis: Axis vector defining the symmetry operation.
        :type axis: object
        :param root: Integer power of the primitive rotation.
        :type root: object
        :param order: Order of the rotation or improper rotation.
        :type order: object
        :return: A symbol such as `E`, `i`, `Cn`, `Sn`, or a reflection-plane label.
        :rtype: str
        """
        ...

    def get_class_symbols(self):
        """
        **LLM Docstring**

        Classify representative matrices and produce display symbols for each conjugacy class.

        :return: The ordered class symbols.
        :rtype: list[str]
        """
        ...

    def format(self, classes=None, irrep_names=None, group_name=None):
        """
        **LLM Docstring**

        Format this table using stored metadata unless explicit labels are supplied.

        :param classes: Conjugacy-class definitions or display labels. Defaults to `None`.
        :type classes: object
        :param irrep_names: Optional irreducible-representation labels. Defaults to `None`.
        :type irrep_names: object
        :param group_name: Optional label for the group. Defaults to `None`.
        :type group_name: object
        :return: A formatted character-table string.
        :rtype: str
        """
        ...

    @property
    def character_basis(self):
        """
        **LLM Docstring**

        Return the class-weighted, group-order-normalized character basis used for projections.

        :return: The projection basis matrix.
        :rtype: np.ndarray
        """
        ...

    def extend_class_representation(self, rep):
        """
        **LLM Docstring**

        Expand class-level representation values to one value per concrete group element.

        :param rep: Character or class representation to transform or decompose.
        :type rep: object
        :return: The element-level representation array.
        :rtype: np.ndarray
        """
        ...

    def get_extended_character_table(self):
        """
        **LLM Docstring**

        Construct the hard-coded or analytic character table for the `get_extended` group family.

        :return: The square character table with irreducible representations along rows.
        :rtype: np.ndarray
        """
        ...

    def decompose_representation(self, rep):
        """
        **LLM Docstring**

        Project a representation onto irreducible characters using the weighted character inner product.

        :param rep: Character or class representation to transform or decompose.
        :type rep: object
        :return: Irreducible-representation multiplicities.
        :rtype: np.ndarray
        """
        ...

    def space_representation(self, mats, symms=None):
        """
        **LLM Docstring**

        Compute traces of transformation matrices, optionally after combining them with supplied symmetry operations.

        :param mats: Transformation matrices whose traces or actions define a representation.
        :type mats: object
        :param symms: Optional symmetry matrices associated with `mats`. Defaults to `None`.
        :type symms: object
        :return: The character vector of the matrix representation.
        :rtype: np.ndarray
        """
        ...

    def matrix_from_representation(self, vec):
        """
        **LLM Docstring**

        Form a matrix as a linear combination of the full group-operation matrices.

        :param vec: Representation coefficients or vector to convert into a matrix.
        :type vec: object
        :return: The resulting Cartesian matrix.
        :rtype: np.ndarray
        """
        ...

    def inverse_character_representation(self, chars):
        """
        **LLM Docstring**

        Map irreducible-character coefficients back into class-representation values.

        :param chars: Character coefficients to invert into class-space values.
        :type chars: object
        :return: The reconstructed class representation.
        :rtype: np.ndarray
        """
        ...

    def symmetry_permutations(self, coords):
        """
        **LLM Docstring**

        Generate permutation representatives for the requested cyclic action.

        :param coords: Cartesian coordinates, normally with shape `(n_atoms, 3)`.
        :type coords: object
        :return: An integer array whose rows are permutations.
        :rtype: np.ndarray
        """
        ...

    def axis_representation(self, include_rotations=True):
        """
        **LLM Docstring**

        Build the translational, and optionally rotational, Cartesian character representation from operation traces and determinants.

        :param include_rotations: Whether rotational components are included with translations. Defaults to `True`.
        :type include_rotations: object
        :return: The axis character representation.
        :rtype: np.ndarray
        """
        ...

    def fixed_permutation_representation(self, base_rep, perms):
        """
        **LLM Docstring**

        Combine a base representation with permutation matrices by applying the same Cartesian block to each permuted index.

        :param base_rep: Base representation matrix or tensor.
        :type base_rep: object
        :param perms: Precomputed atom permutations for symmetry operations.
        :type perms: object
        :return: The fixed-permutation representation tensors.
        :rtype: np.ndarray
        """
        ...

    def coordinate_representation(self, coords):
        """
        **LLM Docstring**

        Build the full Cartesian coordinate representation induced by molecular symmetry permutations.

        :param coords: Cartesian coordinates, normally with shape `(n_atoms, 3)`.
        :type coords: object
        :return: The coordinate representation matrices.
        :rtype: np.ndarray
        """
        ...

    def coordinate_mode_reduction(self, coords):
        """
        **LLM Docstring**

        Decompose the Cartesian coordinate representation and subtract translational/rotational content.

        :param coords: Cartesian coordinates, normally with shape `(n_atoms, 3)`.
        :type coords: object
        :return: Vibrational irreducible-representation multiplicities.
        :rtype: np.ndarray
        """
        ...

    def get_full_matrices(self):
        """
        **LLM Docstring**

        Build the three-dimensional Cartesian matrix representation for selected group elements.

        :return: An array of shape `(n_elements, 3, 3)`.
        :rtype: np.ndarray
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a compact representation containing the group key.

        :return: The representation string.
        :rtype: str
        """
        ...

    def _ipython_display_(self):
        """
        **LLM Docstring**

        Display the formatted character table in IPython.

        :return: No value is returned.
        :rtype: None
        """
        ...
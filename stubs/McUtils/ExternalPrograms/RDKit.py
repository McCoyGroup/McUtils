__all__ = ['RDMolecule']
import base64
import itertools
import functools
import tempfile as tf
import numpy as np, io, os
from .. import Numputils as nput
from .. import Devutils as dev
from ..Data import AtomData
from .ChemToolkits import RDKitInterface
from .ExternalMolecule import ExternalMolecule
from .. import Coordinerds as coordops
from ..Jupyter import DisplayImage

class RDMolecule(ExternalMolecule):
    """
    A simple interchange format for RDKit molecules
    """

    def __init__(self, rdconf, charge=None):
        """
        **LLM Docstring**

        Wrap an RDKit conformer (and its owning mol) as an `RDMolecule`.

        :param rdconf: the RDKit conformer
        :type rdconf: Chem.Conformer
        :param charge: the molecular charge
        :type charge: int | None
        """
        ...

    @property
    def rdmol(self):
        """
        **LLM Docstring**

        The underlying RDKit `Mol` object (recovered from the conformer if needed).

        :return: the RDKit mol
        :rtype: Chem.Mol
        """
        ...

    @property
    def atoms(self):
        """
        **LLM Docstring**

        The element symbols of the atoms, in order.

        :return: the atom symbols
        :rtype: list[str]
        """
        ...

    @property
    def bonds(self):
        """
        **LLM Docstring**

        The bonds as `[begin_atom, end_atom, order]` triples.

        :return: the bond list
        :rtype: list[list]
        """
        ...

    @property
    def coords(self):
        """
        **LLM Docstring**

        The atomic Cartesian coordinates (Angstroms). Setting this writes new positions
        onto the conformer.

        :return: the coordinates
        :rtype: np.ndarray
        """
        ...

    @coords.setter
    def coords(self, coords):
        """
        **LLM Docstring**

        The atomic Cartesian coordinates (Angstroms). Setting this writes new positions
        onto the conformer.

        :return: the coordinates
        :rtype: np.ndarray
        """
        ...

    @property
    def rings(self):
        """
        **LLM Docstring**

        The atom-index tuples of the rings found by RDKit's ring perception.

        :return: the ring atom indices
        :rtype: tuple
        """
        ...

    @property
    def meta(self):
        """
        **LLM Docstring**

        The molecule's RDKit properties as a dict.

        :return: the property dict
        :rtype: dict
        """
        ...

    def copy(self):
        """
        **LLM Docstring**

        Return a copy of this molecule, carrying over the current conformer and charge.

        :return: the copied molecule
        :rtype: RDMolecule
        """
        ...

    @property
    def charges(self):
        """
        **LLM Docstring**

        The per-atom Gasteiger partial charges (computed on access).

        :return: the partial charges
        :rtype: list[float]
        """
        ...

    @property
    def formal_charges(self):
        """
        **LLM Docstring**

        The per-atom formal charges.

        :return: the formal charges
        :rtype: list[int]
        """
        ...

    class NullContext:

        def __enter__(self):
            """
            **LLM Docstring**

            Enter the no-op context (used when error suppression is disabled).

            :return: None
            """
            ...

        def __exit__(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Exit the no-op context.

            :param exc_type: the exception type, if any
            :param exc_val: the exception value, if any
            :param exc_tb: the traceback, if any
            """
            ...

    @classmethod
    def quiet_errors(cls, verbose=False):
        """
        **LLM Docstring**

        Return a context manager that suppresses RDKit's C++ log output, unless
        `verbose` is set (in which case a no-op context is returned).

        :param verbose: don't suppress logging
        :type verbose: bool
        :return: the (log-blocking or no-op) context manager
        :rtype: object
        """
        ...

    @classmethod
    def chem_api(cls):
        """
        **LLM Docstring**

        Return the RDKit `Chem` submodule.

        :return: the `Chem` module
        :rtype: module
        """
        ...

    @classmethod
    def _prep_mol(cls, rdkit_mol):
        """
        **LLM Docstring**

        Do the minimal ring/hybridization/property-cache setup needed to work with a
        mol that hasn't been fully sanitized.

        :param rdkit_mol: the mol to prepare (modified in place)
        :type rdkit_mol: Chem.Mol
        """
        ...

    @classmethod
    def guess_rdmol_bonds(cls, rdmol, charge=None, determine_orders=True, in_place=False):
        """
        **LLM Docstring**

        Perceive the bonds (and, optionally, bond orders) of a mol from its atomic
        coordinates, falling back to connectivity-only perception when order
        determination fails.

        :param rdmol: the mol
        :type rdmol: Chem.Mol
        :param charge: the molecular charge (inferred if omitted)
        :type charge: int | None
        :param determine_orders: also perceive bond orders
        :type determine_orders: bool
        :param in_place: modify the mol in place rather than copying
        :type in_place: bool
        :return: the mol with perceived bonds
        :rtype: Chem.Mol
        """
        ...

    @classmethod
    def from_rdmol(cls, rdmol, conf_id=0, charge=None, guess_bonds=False, sanitize=True, add_implicit_hydrogens=False, sanitize_ops=None, allow_generate_conformers=False, num_confs=1, optimize=False, take_min=True, force_field_type='mmff'):
        """
        **LLM Docstring**

        Build an `RDMolecule` from an RDKit mol, adding hydrogens and optionally guessing
        bonds, sanitizing, and generating conformers.

        :param rdmol: the source mol
        :type rdmol: Chem.Mol
        :param conf_id: the conformer id to use
        :type conf_id: int
        :param charge: the molecular charge (inferred if omitted)
        :type charge: int | None
        :param guess_bonds: perceive bonds from geometry
        :type guess_bonds: bool
        :param sanitize: run RDKit sanitization
        :type sanitize: bool
        :param add_implicit_hydrogens: add implicit (not just explicit) hydrogens
        :type add_implicit_hydrogens: bool
        :param sanitize_ops: sanitization operation flags
        :param allow_generate_conformers: generate conformers if none exist
        :type allow_generate_conformers: bool
        :param num_confs: number of conformers to generate
        :type num_confs: int
        :param optimize: force-field optimize generated conformers
        :type optimize: bool
        :param take_min: keep only the lowest-energy generated conformer
        :type take_min: bool
        :param force_field_type: the force field for optimization
        :type force_field_type: str
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        ...

    @classmethod
    def resolve_bond_type(cls, t):
        """
        **LLM Docstring**

        Map a numeric bond order to the corresponding RDKit `BondType` (handling the
        aromatic/half-integer cases).

        :param t: the numeric bond order
        :type t: float
        :return: the RDKit bond type
        :rtype: Chem.BondType
        """
        ...
    default_new_coord_alignment_method = 'rigid'

    @classmethod
    def _align_new_conf_coords(cls, mol, coords, coords2, method=None):
        """
        **LLM Docstring**

        Align a freshly generated conformer's coordinates back onto a set of reference
        coordinates (e.g. after adding implicit hydrogens), placing the new atoms via a
        local rigid frame or a global Eckart embedding.

        :param mol: the mol (for connectivity)
        :type mol: Chem.Mol
        :param coords: the reference coordinates (heavy atoms)
        :type coords: np.ndarray
        :param coords2: the full generated coordinates
        :type coords2: np.ndarray
        :param method: `'rigid'`, `'eckart'`, or otherwise pass through
        :type method: str | None
        :return: the aligned coordinates
        :rtype: np.ndarray
        """
        ...
    implicit_hydrogen_to_conformer_method = 'builtin'

    @classmethod
    def from_coords(cls, atoms, coords, bonds=None, charge=None, formal_charges=None, guess_bonds=None, add_implicit_hydrogens=False, implicit_hydrogen_method=None, distance_matrix_tol=0.05, num_confs=None, optimize=False, take_min=None, force_field_type='mmff', confgen_opts=None, sanitize=False, **opts):
        """
        **LLM Docstring**

        Build an `RDMolecule` from atoms, coordinates, and (optional) bonds, optionally
        adding implicit hydrogens (placed by conformer generation) and guessing bonds.

        :param atoms: the element symbols
        :type atoms: Sequence[str]
        :param coords: the Cartesian coordinates
        :type coords: np.ndarray
        :param bonds: the bonds as `[i, j(, order)]`
        :type bonds: Sequence | None
        :param charge: the molecular charge
        :type charge: int | None
        :param formal_charges: per-atom formal charges
        :type formal_charges: Sequence | None
        :param guess_bonds: perceive bonds from geometry (defaults to when no bonds given)
        :type guess_bonds: bool | None
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param implicit_hydrogen_method: how to place added hydrogens (`'align'`/`'initial'`/`'builtin'`)
        :type implicit_hydrogen_method: str | None
        :param distance_matrix_tol: tolerance for distance constraints when aligning
        :type distance_matrix_tol: float
        :param num_confs: number of conformers to generate
        :type num_confs: int | None
        :param optimize: force-field optimize generated conformers
        :type optimize: bool
        :param take_min: keep only the lowest-energy conformer
        :type take_min: bool | None
        :param force_field_type: the force field for optimization
        :type force_field_type: str
        :param confgen_opts: extra conformer-generation options
        :type confgen_opts: dict | None
        :param sanitize: run sanitization
        :type sanitize: bool
        :return: the wrapped molecule (or a list, when multiple conformers are kept)
        :rtype: RDMolecule | list
        """
        ...

    @classmethod
    def from_mol(cls, mol, coord_unit='Angstroms', guess_bonds=None):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a generic molecule object, converting its coordinates
        to Angstroms.

        :param mol: the source molecule
        :param coord_unit: the source coordinate unit
        :type coord_unit: str
        :param guess_bonds: perceive bonds from geometry
        :type guess_bonds: bool | None
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        ...

    @classmethod
    def _load_sdf_conf(cls, stream, which=0):
        """
        **LLM Docstring**

        Read the `which`-th molecule from an SDF stream.

        :param stream: the SDF byte stream
        :param which: the index of the entry to read
        :type which: int
        :return: the RDKit mol
        :rtype: Chem.Mol
        """
        ...

    @classmethod
    def from_sdf(cls, sdf_string, which=0):
        """
        **LLM Docstring**

        Build an `RDMolecule` from an SDF file path or string.

        :param sdf_string: the SDF file path or content
        :type sdf_string: str
        :param which: the index of the entry to read
        :type which: int
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        ...

    @classmethod
    def get_confgen_opts(cls, version='v3', use_experimental_torsion_angle_prefs=True, use_basic_knowledge=True, **opts):
        """
        **LLM Docstring**

        Build an RDKit ETKDG conformer-generation parameter object of the requested
        version, applying the torsion/knowledge flags and any extra options.

        :param version: the ETKDG version (`'v1'`/`'v2'`/`'v3'`)
        :type version: str
        :param use_experimental_torsion_angle_prefs: use experimental torsion prefs
        :type use_experimental_torsion_angle_prefs: bool
        :param use_basic_knowledge: use basic chemical knowledge
        :type use_basic_knowledge: bool
        :param opts: extra parameters set on the params object (camel-cased)
        :return: the parameter object
        :rtype: object
        """
        ...

    @classmethod
    def parse_smiles(cls, smiles, sanitize=False, parse_name=True, allow_cxsmiles=True, strict_cxsmiles=True, remove_hydrogens=False, add_implicit_hydrogens=None, reorder_from_atom_map=False, replacements=None, quiet=False, **opts):
        """
        **LLM Docstring**

        Parse a SMILES (or CXSMILES) string into an RDKit mol, with control over
        sanitization, hydrogen handling, and atom-map-based reordering.

        :param smiles: the SMILES string
        :type smiles: str
        :param sanitize: run sanitization
        :type sanitize: bool
        :param parse_name: parse a trailing molecule name
        :type parse_name: bool
        :param allow_cxsmiles: allow CXSMILES extensions
        :type allow_cxsmiles: bool
        :param strict_cxsmiles: fail on bad CXSMILES rather than ignoring
        :type strict_cxsmiles: bool
        :param remove_hydrogens: remove explicit hydrogens
        :type remove_hydrogens: bool
        :param add_implicit_hydrogens: add hydrogens (or `'full'` to also re-enable implicit Hs)
        :type add_implicit_hydrogens: bool | str | None
        :param reorder_from_atom_map: renumber atoms by their atom-map numbers
        :type reorder_from_atom_map: bool
        :param replacements: SMILES token replacements
        :type replacements: dict | None
        :param quiet: suppress RDKit logging
        :type quiet: bool
        :return: the parsed mol, or `None` on failure
        :rtype: Chem.Mol | None
        """
        ...

    @classmethod
    def from_smiles(cls, smiles, sanitize=False, parse_name=True, allow_cxsmiles=True, strict_cxsmiles=True, remove_hydrogens=False, replacements=None, add_implicit_hydrogens=False, call_add_hydrogens=True, conf_id=None, num_confs=None, optimize=False, take_min=True, force_field_type='mmff', reorder_from_atom_map=True, confgen_opts=None, check_tag=True, coords=None, conf_tag=None, **opts):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a SMILES string (or file), embedding a conformer
        (generated, or decoded from a conformer tag / supplied coordinates).

        :param smiles: the SMILES string or file path
        :type smiles: str
        :param sanitize: run sanitization
        :type sanitize: bool
        :param parse_name: parse a trailing molecule name
        :type parse_name: bool
        :param allow_cxsmiles: allow CXSMILES extensions
        :type allow_cxsmiles: bool
        :param strict_cxsmiles: fail on bad CXSMILES
        :type strict_cxsmiles: bool
        :param remove_hydrogens: remove explicit hydrogens
        :type remove_hydrogens: bool
        :param replacements: SMILES token replacements
        :type replacements: dict | None
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param call_add_hydrogens: call `AddHs` before embedding
        :type call_add_hydrogens: bool
        :param conf_id: the conformer id to use
        :type conf_id: int | None
        :param num_confs: number of conformers to generate
        :type num_confs: int | None
        :param optimize: force-field optimize generated conformers
        :type optimize: bool
        :param take_min: keep only the lowest-energy conformer
        :type take_min: bool
        :param force_field_type: the force field for optimization
        :type force_field_type: str
        :param reorder_from_atom_map: renumber atoms by atom-map number
        :type reorder_from_atom_map: bool
        :param confgen_opts: extra conformer-generation options
        :type confgen_opts: dict | None
        :param check_tag: split off a trailing `_`-delimited conformer tag
        :type check_tag: bool
        :param coords: explicit coordinates to use instead of generating a conformer
        :type coords: np.ndarray | None
        :param conf_tag: an explicit conformer tag to decode
        :type conf_tag: str | None
        :return: the wrapped molecule (or list, for multiple conformers)
        :rtype: RDMolecule | list
        """
        ...

    @classmethod
    def from_base_mol(cls, mol, conf_id=None, num_confs=None, optimize=False, take_min=None, force_field_type='mmff', confgen_opts=None, **mol_opts):
        """
        **LLM Docstring**

        Build an `RDMolecule` from an RDKit mol, using an existing conformer when
        available and otherwise generating one.

        :param mol: the source mol
        :type mol: Chem.Mol
        :param conf_id: the conformer id to use
        :type conf_id: int | None
        :param num_confs: number of conformers to generate
        :type num_confs: int | None
        :param optimize: force-field optimize generated conformers
        :type optimize: bool
        :param take_min: keep only the lowest-energy conformer
        :type take_min: bool | None
        :param force_field_type: the force field for optimization
        :type force_field_type: str
        :param confgen_opts: extra conformer-generation options
        :type confgen_opts: dict | None
        :param mol_opts: extra options forwarded to `from_rdmol`
        :return: the wrapped molecule (or list)
        :rtype: RDMolecule | list
        """
        ...
    default_fragment_placement_method = 'centroid'
    different_fragment_embedding_distance = 5

    @classmethod
    def _set_fragment_centroids(cls, frag_inds, frag_atoms, frag_bonds, frag_coord_sets, frag_positions, min_dist=None):
        """
        **LLM Docstring**

        Place disconnected fragments relative to one another by offsetting each
        fragment's inertial frame along a fixed displacement, returning the combined
        per-conformer coordinate sets.

        :param frag_inds: the original atom indices of each fragment
        :type frag_inds: list
        :param frag_atoms: the element symbols of each fragment
        :type frag_atoms: list
        :param frag_bonds: the bonds of each fragment
        :type frag_bonds: list
        :param frag_coord_sets: the per-conformer coordinates of each fragment
        :type frag_coord_sets: list
        :param frag_positions: optional target positions per fragment
        :type frag_positions: list
        :param min_dist: the inter-fragment separation
        :type min_dist: float | None
        :return: the combined coordinate sets
        :rtype: list
        """
        ...

    @classmethod
    def _set_fragment_positions(cls, frag_inds, frag_atoms, frag_bonds, frag_coord_sets, frag_positions, use_actual=False):
        """
        **LLM Docstring**

        Place disconnected fragments by aligning each onto supplied target positions
        (via a shift for one point or an Eckart embedding for several), returning the
        combined per-conformer coordinate sets.

        :param frag_inds: the original atom indices of each fragment
        :type frag_inds: list
        :param frag_atoms: the element symbols of each fragment
        :type frag_atoms: list
        :param frag_bonds: the bonds of each fragment
        :type frag_bonds: list
        :param frag_coord_sets: the per-conformer coordinates of each fragment
        :type frag_coord_sets: list
        :param frag_positions: the target positions (per fragment, keyed by atom)
        :type frag_positions: list
        :param use_actual: pin the mapped atoms exactly to their targets
        :type use_actual: bool
        :return: the combined coordinate sets
        :rtype: list
        """
        ...

    @classmethod
    def _centroid_frag_dists(cls, mol, graph, fragments, min_dist=None):
        """
        **LLM Docstring**

        Compute the inter-fragment distance constraints between the fragments' graph
        centroids.

        :param mol: the mol
        :type mol: Chem.Mol
        :param graph: the molecular edge graph
        :param fragments: the fragment atom-index groups
        :type fragments: list
        :param min_dist: the minimum separation
        :type min_dist: float | None
        :return: the distance constraints between centroid atoms
        :rtype: object
        """
        ...

    @classmethod
    def _take_submol(cls, atoms, bonds, inds):
        """
        **LLM Docstring**

        Build a sub-mol containing only the given atom indices and the bonds among them.

        :param atoms: the full atom list
        :type atoms: list
        :param bonds: the full bond list
        :type bonds: list
        :param inds: the atom indices to keep
        :type inds: Sequence[int]
        :return: the sub-mol
        :rtype: Chem.Mol
        """
        ...

    @classmethod
    def generate_conformers_for_mol(cls, mol, *, num_confs=1, optimize=False, take_min=True, force_field_type='mmff', add_implicit_hydrogens=False, distance_constraints=None, initial_coordinates=None, fragment_placement_method=None, fragments=None, embedding_mol=None, verbose=False, **opts):
        """
        **LLM Docstring**

        Generate one or more conformers for a mol via RDKit's ETKDG embedding,
        handling disconnected fragments (embedded separately and placed), distance
        constraints, fixed initial coordinates, optional force-field optimization, and
        lowest-energy selection.

        :param mol: the mol to embed (modified in place; conformers are added)
        :type mol: Chem.Mol
        :param num_confs: number of conformers to generate
        :type num_confs: int
        :param optimize: force-field optimize the conformers
        :type optimize: bool
        :param take_min: return only the lowest-energy conformer id
        :type take_min: bool
        :param force_field_type: the force field for optimization/selection
        :type force_field_type: str
        :param add_implicit_hydrogens: add implicit hydrogens before embedding
        :type add_implicit_hydrogens: bool
        :param distance_constraints: pairwise distance bounds (or a full bounds matrix)
        :type distance_constraints: dict | list | None
        :param initial_coordinates: fixed starting coordinates for some/all atoms
        :type initial_coordinates: dict | Sequence | None
        :param fragment_placement_method: how to place disconnected fragments
        :type fragment_placement_method: str | Callable | None
        :param fragments: precomputed fragment atom groups
        :type fragments: list | None
        :param embedding_mol: a hydrogen-added mol to embed into
        :type embedding_mol: Chem.Mol | None
        :param verbose: don't suppress RDKit logging
        :type verbose: bool
        :return: the generated conformer id (or list of ids)
        :rtype: int | list
        """
        ...

    @classmethod
    def from_no_conformer_molecule(cls, mol, *, conf_id=None, num_confs=1, optimize=False, take_min=True, force_field_type='mmff', add_implicit_hydrogens=False, confgen_opts=None, **etc):
        """
        **LLM Docstring**

        Generate conformer(s) for a mol that has none, then wrap the result(s) as
        `RDMolecule`(s).

        :param mol: the source mol
        :type mol: Chem.Mol
        :param conf_id: a specific conformer id to keep (disables optimization)
        :type conf_id: int | None
        :param num_confs: number of conformers to generate
        :type num_confs: int
        :param optimize: force-field optimize the conformers
        :type optimize: bool
        :param take_min: keep only the lowest-energy conformer
        :type take_min: bool
        :param force_field_type: the force field for optimization
        :type force_field_type: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param confgen_opts: extra conformer-generation options
        :type confgen_opts: dict | None
        :param etc: extra options forwarded to `from_rdmol`
        :return: the wrapped molecule (or list)
        :rtype: RDMolecule | list
        """
        ...

    @staticmethod
    def _camel_case(o, caps_all=False):
        """
        **LLM Docstring**

        Convert a snake_case string to camelCase (or PascalCase when `caps_all` is set),
        for mapping option names onto RDKit's API.

        :param o: the snake_case string
        :type o: str
        :param caps_all: capitalize the first word too
        :type caps_all: bool
        :return: the camel-cased string
        :rtype: str
        """
        ...

    def to_smiles(self, remove_hydrogens=None, remove_implicit_hydrogens=None, include_tag=False, canonical=False, compute_stereo=False, remove_stereo=False, preserve_atom_order=False, binary=False, coords=None, mol=None, **opts):
        """
        **LLM Docstring**

        Serialize the molecule to a SMILES string, with options for hydrogen/stereo
        handling, atom-order preservation, and appending a conformer tag encoding the
        3D geometry.

        :param remove_hydrogens: remove explicit hydrogens
        :type remove_hydrogens: bool | None
        :param remove_implicit_hydrogens: remove only implicit hydrogens
        :type remove_implicit_hydrogens: bool | None
        :param include_tag: append a `_`-delimited conformer tag
        :type include_tag: bool
        :param canonical: emit canonical SMILES
        :type canonical: bool
        :param compute_stereo: assign stereochemistry from the 3D coordinates first
        :type compute_stereo: bool
        :param remove_stereo: strip stereochemistry
        :type remove_stereo: bool
        :param preserve_atom_order: keep the current atom ordering
        :type preserve_atom_order: bool
        :param binary: return/encode the tag in binary form
        :type binary: bool
        :param coords: coordinates to encode in the tag (defaults to the current ones)
        :type coords: np.ndarray | None
        :param mol: an explicit mol to serialize (defaults to this one)
        :type mol: Chem.Mol | None
        :return: the SMILES string (optionally with a conformer tag)
        :rtype: str | bytes
        """
        ...
    draw_options_mapping = {}
    drawing_defaults = {None: {'image_size': [500, 200]}}

    @classmethod
    def _draw_ipython(cls, mol, format='svg', **opts):
        """
        **LLM Docstring**

        Configure RDKit's IPython console drawing options and display the mol inline.

        :param mol: the mol to display
        :type mol: Chem.Mol
        :param format: `'svg'` or `'png'`
        :type format: str
        :param opts: drawing options (camel-cased onto the RDKit draw options)
        :return: the display result
        :rtype: object
        """
        ...

    @classmethod
    def _drawer_png(cls, *, image_size, plot_range=None, no_free_type=None, **opts):
        """
        **LLM Docstring**

        Build a PNG (raster) RDKit 2D drawer at the given image size, optionally with a
        fixed plot range/scale.

        :param image_size: the `(width, height)` of the image
        :type image_size: Sequence[int]
        :param plot_range: `((min_x, max_x), (min_y, max_y))` to fix the scale
        :type plot_range: tuple | None
        :param no_free_type: disable FreeType font rendering
        :type no_free_type: bool | None
        :param opts: remaining (unconsumed) options
        :return: `(drawer, remaining_opts)`
        :rtype: tuple
        """
        ...

    @classmethod
    def _drawer_svg(cls, *, image_size, plot_range=None, no_free_type=None, **opts):
        """
        **LLM Docstring**

        Build an SVG RDKit 2D drawer at the given image size, optionally with a fixed
        plot range/scale.

        :param image_size: the image size (a scalar is squared)
        :type image_size: Sequence[int] | int
        :param plot_range: `((min_x, max_x), (min_y, max_y))` to fix the scale
        :type plot_range: tuple | None
        :param no_free_type: disable FreeType font rendering
        :type no_free_type: bool | None
        :param opts: remaining (unconsumed) options
        :return: `(drawer, remaining_opts)`
        :rtype: tuple
        """
        ...

    @classmethod
    def _prep_draw_opts(cls, format, opts):
        """
        **LLM Docstring**

        Merge the default drawing options (global and per-format) with the supplied
        options, dropping any `None` values.

        :param format: the output format
        :type format: str
        :param opts: the user-supplied options
        :type opts: dict
        :return: the merged options
        :rtype: dict
        """
        ...

    @classmethod
    def _manage_draw_opts(cls, label_style=None, **etc):
        """
        **LLM Docstring**

        Translate high-level label-style options (font size, color) into the low-level
        RDKit annotation-scale/color options, returning the RDKit options plus the
        deferred style values.

        :param label_style: a `{font_size, color}` style dict
        :type label_style: dict | None
        :param etc: the remaining options
        :return: `(rdkit_options, deferred_style)`
        :rtype: tuple
        """
        ...

    @staticmethod
    def _set_font_file(draw_opts, font_name):
        """
        **LLM Docstring**

        Set the drawer's font file, resolving a font *name* to a file path via
        matplotlib's font manager when needed.

        :param draw_opts: the RDKit draw-options object (modified in place)
        :param font_name: a font file path or font family name
        :type font_name: str
        """
        ...

    @staticmethod
    def _get_font_file(draw_opts):
        """
        **LLM Docstring**

        Return the drawer's currently configured font file.

        :param draw_opts: the RDKit draw-options object
        :return: the font file path
        :rtype: str
        """
        ...
    _drawer_opts = {'fill_polys': 'fill_polys', 'color': (None, 'set_colour', 'black'), 'font_size': 'font_size'}

    @classmethod
    def _handle_color(cls, v):
        """
        **LLM Docstring**

        Normalize a color (name/string or RGB sequence) into an RDKit `(r, g, b)` tuple
        in `[0, 1]`.

        :param v: the color specification
        :type v: str | Sequence | None
        :return: the normalized color tuple, or `None`
        :rtype: tuple | None
        """
        ...

    @classmethod
    def _handle_draw_elements(cls, elements):
        """
        **LLM Docstring**

        Resolve a draw-element specification (names or flags) into the combined RDKit
        `DrawElement` bit mask.

        :param elements: the element name(s)/flag(s)
        :type elements: list | tuple | object
        :return: the element mask
        :rtype: object
        """
        ...

    @classmethod
    def _get_draw_opt(cls, drawer, draw_options, k):
        """
        **LLM Docstring**

        Read a drawing option, dispatching to the drawer method, the draw-options
        getter, or a plain attribute depending on where the option lives.

        :param drawer: the RDKit drawer
        :param draw_options: the drawer's options object
        :param k: the option name
        :type k: str
        :return: the option value
        :rtype: Any
        """
        ...

    @classmethod
    def _set_draw_opt(cls, drawer, draw_options, k, v):
        """
        **LLM Docstring**

        Set a drawing option, dispatching to the drawer method, the draw-options setter,
        or a plain attribute, and normalizing colors/element masks as needed.

        :param drawer: the RDKit drawer
        :param draw_options: the drawer's options object
        :param k: the option name
        :type k: str
        :param v: the value to set (ignored if `None`)
        :return: the setter's return value, if any
        :rtype: Any
        """
        ...

    @classmethod
    def _handle_annotation_draw(cls, caller, drawer, draw_options, *args, styles: dict, **kwargs):
        """
        **LLM Docstring**

        Temporarily apply a set of drawing-option overrides, invoke a draw callback, then
        restore the original options.

        :param caller: the draw callback to invoke
        :type caller: Callable
        :param drawer: the RDKit drawer
        :param draw_options: the drawer's options object
        :param args: positional arguments for the callback
        :param styles: the option overrides to apply during the call
        :type styles: dict
        :param kwargs: keyword arguments for the callback
        """
        ...

    @classmethod
    def _prep_draw_coords(cls, draw_coords):
        """
        **LLM Docstring**

        Normalize the various accepted `draw_coords` forms (dict, list of keys, list of
        dicts) into a uniform list of `{key, ...}` annotation dicts.

        :param draw_coords: the annotation coordinate specifications
        :type draw_coords: dict | list | None
        :return: the normalized annotation dicts
        :rtype: list[dict]
        """
        ...
    default_draw_options = {'annotation_font_scale': 1}

    @classmethod
    def _draw_non_interactive(cls, mol, figure=None, format='svg', drawer=None, drawer_options=None, legend=None, highlight_atoms=None, highlight_bonds=None, highlight_atom_colors=None, highlight_bond_colors=None, highlight_atom_radii=None, highlight_bond_radii=None, coords=None, draw_coords=None, plot_range=None, conf_id=None, predraw=None, return_splits=False, no_free_type=None, **opts):
        """
        **LLM Docstring**

        Render a mol to a static SVG/PNG with RDKit's 2D drawer, applying highlights,
        legends, coordinate annotations, a fixed plot range, and optional pre-draw
        callbacks.

        :param mol: the mol to draw
        :type mol: Chem.Mol
        :param figure: an existing figure/drawer to draw into
        :param format: `'svg'` or `'png'`
        :type format: str
        :param drawer: an explicit drawer to use
        :param drawer_options: extra drawer construction options
        :type drawer_options: dict | None
        :param legend: a legend string
        :type legend: str | None
        :param highlight_atoms: atoms to highlight
        :param highlight_bonds: bonds to highlight
        :param highlight_atom_colors: per-atom highlight colors
        :param highlight_bond_colors: per-bond highlight colors
        :param highlight_atom_radii: per-atom highlight radii
        :param highlight_bond_radii: per-bond highlight radii
        :param coords: 2D coordinates to draw at (defaults to the conformer's)
        :type coords: np.ndarray | None
        :param draw_coords: extra coordinate annotations
        :param plot_range: a fixed drawing range
        :type plot_range: tuple | None
        :param conf_id: the conformer id
        :type conf_id: int | None
        :param predraw: a callback invoked before finishing the drawing
        :type predraw: Callable | None
        :param return_splits: also return the drawing element split metadata
        :type return_splits: bool
        :param no_free_type: disable FreeType font rendering
        :type no_free_type: bool | None
        :return: the rendered image (and split metadata if requested)
        :rtype: object
        """
        ...

    def find_substructure(self, query):
        """
        **LLM Docstring**

        Return all substructure matches of a SMARTS query in the molecule.

        :param query: the SMARTS query
        :type query: str
        :return: the matching atom-index tuples
        :rtype: tuple
        """
        ...

    @classmethod
    def apply_smarts_to_mol(cls, mol, pattern, remove_hydrogens=True, readd_hydrogens=True):
        """
        **LLM Docstring**

        Apply a SMARTS reaction transform to a mol, running the reaction and
        reassembling the products while preserving atom mapping and re-adding
        hydrogens consistently.

        :param mol: the reactant mol
        :type mol: Chem.Mol
        :param pattern: the SMARTS reaction (string or reaction object)
        :type pattern: str | object
        :param remove_hydrogens: strip hydrogens before reacting
        :type remove_hydrogens: bool
        :param readd_hydrogens: re-add hydrogens to the products
        :type readd_hydrogens: bool
        :return: the product mols
        :rtype: list[Chem.Mol]
        :raises ValueError: if the pattern doesn't map all atoms
        """
        ...

    def apply_smarts(self, tf):
        """
        **LLM Docstring**

        Apply a SMARTS reaction transform to this molecule, returning the products as
        `RDMolecule`s carrying the current coordinates.

        :param tf: the SMARTS reaction
        :type tf: str | object
        :return: the product molecules
        :rtype: list[RDMolecule]
        """
        ...

    @classmethod
    def take_mol_fragment(cls, mol, inds, conf_id=None):
        """
        **LLM Docstring**

        Build a sub-mol from the given atom indices (with the bonds among them),
        optionally carrying over a conformer's coordinates.

        :param mol: the source mol
        :type mol: Chem.Mol
        :param inds: the atom indices to keep
        :type inds: Sequence[int]
        :param conf_id: a conformer id whose coordinates to copy
        :type conf_id: int | None
        :return: the sub-mol
        :rtype: Chem.Mol
        """
        ...

    def break_bonds(self, bonds, add_dummies=False, reguess_bonds=True, return_fragments=False):
        """
        **LLM Docstring**

        Break the given bonds and return the resulting (fragmented) molecule, carrying
        over coordinates and optionally re-perceiving bond orders.

        :param bonds: the `(i, j)` bonds to break
        :type bonds: Sequence
        :param add_dummies: add dummy atoms at the broken bonds
        :type add_dummies: bool
        :param reguess_bonds: re-perceive bond orders afterward
        :type reguess_bonds: bool
        :param return_fragments: unused flag
        :type return_fragments: bool
        :return: the fragmented molecule
        :rtype: RDMolecule
        """
        ...

    @classmethod
    def fragment_rdmol(cls, mol, inds):
        """
        **LLM Docstring**

        Build a sub-mol from the given atom indices and the bonds among them.

        :param mol: the source mol
        :type mol: Chem.Mol
        :param inds: the atom indices to keep
        :type inds: Sequence[int]
        :return: the sub-mol
        :rtype: Chem.Mol
        """
        ...

    @classmethod
    def fragment_rdmol_on_bonds(cls, mol, bonds, addDummies=True):
        """
        **LLM Docstring**

        Fragment a mol by breaking the given bonds, returning a mapping from each
        fragment's atom-index tuple to its sub-mol (with atom maps restored).

        :param mol: the source mol
        :type mol: Chem.Mol
        :param bonds: the `(i, j)` bonds to break (by atom-map number)
        :type bonds: Sequence
        :param addDummies: add dummy atoms at the broken bonds
        :type addDummies: bool
        :return: the `{fragment_indices: sub_mol}` mapping
        :rtype: dict
        """
        ...

    def get_atom_neighbors(self, i, n=1, mol=None, graph=None):
        """
        **LLM Docstring**

        Return the labels of the atoms within `n` bonds of a given atom.

        :param i: the central atom index
        :type i: int
        :param n: the neighborhood radius (in bonds)
        :type n: int
        :param mol: an explicit mol (defaults to this one)
        :type mol: Chem.Mol | None
        :param graph: a precomputed edge graph
        :return: the neighbor atom labels
        :rtype: list
        """
        ...
    default_up_vector = (0, 1, 0)
    default_right_vector = (1, 0, 0)
    default_view_vector = (0, 0, 1)

    def _get_view_settings(self, up_vector=None, right_vector=None, view_vector=None, view_matrix=None, view_distance=None, view_center=None):
        """
            **LLM Docstring**

            Build a 3D view specification (rotation matrix, distance, center) from any
            combination of up/right/view vectors, filling in the missing axes by cross
            products.

            :param up_vector: the up direction
            :param right_vector: the right direction
            :param view_vector: the view/forward direction
            :param view_matrix: an explicit view rotation matrix
            :param view_distance: the camera distance
            :param view_center: the view center
            :return: the `{matrix, distance, center}` view settings
            :rtype: dict
            """
        ...

    def draw(self, figure=None, background=None, remove_atom_numbers=None, remove_hydrogens=True, display_atom_numbers=False, format='svg', drawer=None, coords=None, use_coords=False, align_2d=None, view_settings=None, plot_range=None, atom_labels=None, bond_labels=None, blend_mixed_bonds=True, highlight_atoms=None, highlight_bonds=None, highlight_atom_colors=None, highlight_bond_colors=None, highlight_atom_radii=None, highlight_bond_radii=None, highlight_bond_width_multiplier=None, atom_radii=None, bond_radius=None, allow_radius_rescaling=True, draw_coords=None, highlight_rings=None, label_offset=1, conf_id=None, include_save_buttons=False, no_free_type=None, postdraw=None, return_splits=None, radius_to_range_scaling=None, **draw_opts):
        """
        **LLM Docstring**

        Draw the molecule in 2D (SVG/PNG), with extensive control over hydrogen removal,
        2D-coordinate generation and alignment, atom/bond labels and highlights, ring
        highlighting, and save buttons.

        :param figure: an existing figure/drawer to draw into
        :param background: the background color
        :param remove_atom_numbers: strip atom-map numbers from the drawing
        :type remove_atom_numbers: bool | None
        :param remove_hydrogens: hide hydrogens
        :type remove_hydrogens: bool
        :param display_atom_numbers: annotate atoms with their indices
        :type display_atom_numbers: bool
        :param format: `'svg'` or `'png'`
        :type format: str
        :param drawer: an explicit drawing function
        :param coords: explicit 2D coordinates to draw at
        :type coords: np.ndarray | None
        :param use_coords: draw using the molecule's own coordinates (projected)
        :type use_coords: bool
        :param align_2d: align the generated 2D coordinates to the view
        :type align_2d: bool | None
        :param view_settings: 3D view settings for coordinate alignment
        :type view_settings: dict | None
        :param plot_range: a fixed drawing range
        :type plot_range: tuple | None
        :param atom_labels: per-atom label overrides
        :param bond_labels: per-bond label overrides
        :param blend_mixed_bonds: blend colors on bonds between differently colored atoms
        :type blend_mixed_bonds: bool
        :param highlight_atoms: atoms to highlight
        :param highlight_bonds: bonds to highlight
        :param highlight_atom_colors: per-atom highlight colors
        :param highlight_bond_colors: per-bond highlight colors
        :param highlight_atom_radii: per-atom highlight radii
        :param highlight_bond_radii: per-bond highlight radii
        :param highlight_bond_width_multiplier: highlight bond-width multiplier
        :param atom_radii: per-atom radii
        :param bond_radius: the bond radius
        :param allow_radius_rescaling: allow radii to rescale with the plot range
        :type allow_radius_rescaling: bool
        :param draw_coords: extra coordinate annotations
        :param highlight_rings: rings to highlight
        :param label_offset: the annotation label offset
        :param conf_id: the conformer id
        :type conf_id: int | None
        :param include_save_buttons: include save buttons in the output
        :type include_save_buttons: bool
        :param no_free_type: disable FreeType font rendering
        :type no_free_type: bool | None
        :param postdraw: a callback invoked after drawing
        :type postdraw: Callable | None
        :param return_splits: also return drawing element split metadata
        :type return_splits: bool | None
        :param radius_to_range_scaling: radius-to-range scaling factor
        :param draw_opts: extra drawing options
        :return: the rendered drawing
        :rtype: object
        """
        ...

    def plot(self, conf_id=None, image_size=(450, 450), **opts):
        """
        **LLM Docstring**

        Display an interactive 3D rendering of the molecule (via RDKit's IPython 3D
        console).

        :param conf_id: the conformer id (defaults to the current one)
        :type conf_id: int | None
        :param image_size: the `(width, height)` of the view
        :type image_size: tuple
        :param opts: extra drawing options
        :return: the 3D display
        :rtype: object
        """
        ...

    @classmethod
    def _plain_encode(cls, flat_z, byte_size):
        """
        **LLM Docstring**

        Encode a flat coordinate array as raw bytes of the given float precision.

        :param flat_z: the flat values
        :type flat_z: Sequence[float]
        :param byte_size: the float bit width (16/32/64/128)
        :type byte_size: int
        :return: the encoded array
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def _plain_decode(cls, buffer, byte_size):
        """
        **LLM Docstring**

        Decode a raw-bytes buffer back into a float array of the given precision.

        :param buffer: the byte buffer
        :type buffer: bytes
        :param byte_size: the float bit width (16/32/64/128)
        :type byte_size: int
        :return: the decoded values
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def _compressed_encode(cls, flat_z, byte_size, primary_bond_range=(0.5, 2.5), pack_angles=True):
        """
        Compress distances such that if they are between 1 and 2 angstroms, we get
        an extra digit of precision
        :param flat_z:
        :param dtype:
        :return:
        """
        ...

    @classmethod
    def _compressed_decode(cls, buffer, byte_size, primary_bond_range=(0.5, 2.5), pack_angles=True):
        """
        Compress distances such that if they are between 1 and 2 angstroms, we get
        an extra digit of precision
        :param flat_z:
        :param dtype:
        :return:
        """
        ...
    defaul_conformer_compression = 'compressed'
    default_tag_byte_size = 16
    default_tag_byte_encoding = 64

    def conformer_smiles_tag(self, coords=None, graph=None, zmatrix=None, encoder=None, byte_size=None, byte_encoding=None, binary=False, include_zmatrix=False):
        """
        **LLM Docstring**

        Encode the molecule's 3D geometry into a compact string tag (a Z-matrix of the
        canonical-fragment internal coordinates, packed and base-N encoded) suitable for
        appending to a SMILES string.

        :param coords: the coordinates to encode (defaults to the current ones)
        :type coords: np.ndarray | None
        :param graph: the molecular edge graph (built if omitted)
        :param zmatrix: an explicit Z-matrix connectivity (built if omitted)
        :param encoder: the value encoder (`'plain'`/`'compressed'`/`'precision'` or a callable)
        :type encoder: str | Callable | None
        :param byte_size: the per-value bit width
        :type byte_size: int | None
        :param byte_encoding: the base-N text encoding (16/32/64/85)
        :type byte_encoding: int | Callable | None
        :param binary: return raw bytes rather than text
        :type binary: bool
        :param include_zmatrix: also return the encoded Z-matrix connectivity
        :type include_zmatrix: bool
        :return: the conformer tag (and Z-matrix data if requested)
        :rtype: str | bytes | tuple
        """
        ...

    @classmethod
    def conformer_from_smiles_tag(cls, tag, graph, decoder=None, byte_size=None, byte_encoding=None, zmatrix=None):
        """
        **LLM Docstring**

        Decode a conformer tag back into Cartesian coordinates, using the molecular graph
        to reconstruct the canonical-fragment Z-matrix.

        :param tag: the conformer tag
        :type tag: str
        :param graph: the molecular edge graph
        :param decoder: the value decoder (`'plain'`/`'compressed'`/`'precision'` or a callable)
        :type decoder: str | Callable | None
        :param byte_size: the per-value bit width
        :type byte_size: int | None
        :param byte_encoding: the base-N text encoding
        :type byte_encoding: int | Callable | None
        :param zmatrix: an explicit Z-matrix connectivity (built if omitted)
        :return: the decoded Cartesian coordinates
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def get_mol_edge_graph(cls, mol):
        """
        **LLM Docstring**

        Build an `EdgeGraph` of a mol's atom/bond connectivity.

        :param mol: the mol
        :type mol: Chem.Mol
        :return: the edge graph
        :rtype: EdgeGraph
        """
        ...

    def get_edge_graph(self, mol=None):
        """
        **LLM Docstring**

        Build an `EdgeGraph` of this molecule's connectivity (or of a supplied mol).

        :param mol: an explicit mol (defaults to this one)
        :type mol: Chem.Mol | None
        :return: the edge graph
        :rtype: EdgeGraph
        """
        ...

    def _ipython_display_(self):
        """
        **LLM Docstring**

        Display the molecule inline in IPython (delegates to `draw`).
        """
        ...

    @classmethod
    def _from_file_reader(cls, file_reader, block_reader, block, binary=False, add_implicit_hydrogens=False, guess_bonds=False, conf_id=0, charge=None, sanitize_ops=None, post_sanitize=True, allow_generate_conformers=False, num_confs=1, optimize=False, take_min=True, force_field_type='mmff', **kwargs):
        """
        **LLM Docstring**

        Shared helper for the `from_*` format importers: read a mol from a file path or
        an in-memory block using the supplied file/block reader functions, then wrap it
        via `from_rdmol`.

        :param file_reader: the file-reading function (or `None`)
        :type file_reader: Callable | None
        :param block_reader: the string/block-reading function
        :type block_reader: Callable
        :param block: the file path or block content
        :type block: str | bytes
        :param binary: treat the content as binary
        :type binary: bool
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param guess_bonds: perceive bonds from geometry
        :type guess_bonds: bool
        :param conf_id: the conformer id
        :type conf_id: int
        :param charge: the molecular charge
        :type charge: int | None
        :param sanitize_ops: sanitization flags
        :param post_sanitize: sanitize after reading
        :type post_sanitize: bool
        :param allow_generate_conformers: generate conformers if none exist
        :type allow_generate_conformers: bool
        :param num_confs: number of conformers to generate
        :type num_confs: int
        :param optimize: force-field optimize generated conformers
        :type optimize: bool
        :param take_min: keep only the lowest-energy conformer
        :type take_min: bool
        :param force_field_type: the force field for optimization
        :type force_field_type: str
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        ...

    @classmethod
    def from_molblock(cls, molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a MDL molblock/`.mol` file or string.

        :param molblock: the molblock file path or content
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param sanitize: run sanitization
        :type sanitize: bool
        :param remove_hydrogens: remove explicit hydrogens
        :type remove_hydrogens: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        ...

    @classmethod
    def from_mrv(cls, molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a Marvin `.mrv` file or string.

        :param molblock: the MRV file path or content
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param sanitize: run sanitization
        :type sanitize: bool
        :param remove_hydrogens: remove explicit hydrogens
        :type remove_hydrogens: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        ...

    @classmethod
    def from_xyz(cls, molblock, add_implicit_hydrogens=False, guess_bonds=True, **mol_opts):
        """
        **LLM Docstring**

        Build an `RDMolecule` from an XYZ file or string (perceiving bonds by default).

        :param molblock: the XYZ file path or content
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param guess_bonds: perceive bonds from geometry
        :type guess_bonds: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        ...

    @classmethod
    def from_mol2(cls, molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a Tripos `.mol2` file or string.

        :param molblock: the mol2 file path or content
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param sanitize: run sanitization
        :type sanitize: bool
        :param remove_hydrogens: remove explicit hydrogens
        :type remove_hydrogens: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        ...

    @classmethod
    def from_cdxml(cls, molblock, add_implicit_hydrogens=True, **mol_opts):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a ChemDraw `.cdxml` file or string.

        :param molblock: the CDXML file path or content
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        ...

    @classmethod
    def from_pdb(cls, molblock, add_implicit_hydrogens=True, **mol_opts):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a PDB file or string.

        :param molblock: the PDB file path or content
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        ...

    @classmethod
    def from_png(cls, molblock, add_implicit_hydrogens=False, **mol_opts):
        """
        **LLM Docstring**

        Build an `RDMolecule` from an RDKit-metadata-bearing PNG file or string.

        :param molblock: the PNG file path or content
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        ...

    @classmethod
    def from_fasta(cls, molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a FASTA sequence (generating a conformer by default).

        :param molblock: the FASTA content
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param allow_generate_conformers: generate a conformer
        :type allow_generate_conformers: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        ...

    @classmethod
    def from_inchi(cls, molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts):
        """
        **LLM Docstring**

        Build an `RDMolecule` from an InChI string (generating a conformer by default).

        :param molblock: the InChI string
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param allow_generate_conformers: generate a conformer
        :type allow_generate_conformers: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        ...

    @classmethod
    def from_helm(cls, molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts):
        """
        **LLM Docstring**

        Build an `RDMolecule` from a HELM (macromolecule) string (generating a conformer
        by default).

        :param molblock: the HELM string
        :type molblock: str
        :param add_implicit_hydrogens: add implicit hydrogens
        :type add_implicit_hydrogens: bool
        :param allow_generate_conformers: generate a conformer
        :type allow_generate_conformers: bool
        :param mol_opts: extra options forwarded to the reader
        :return: the wrapped molecule
        :rtype: RDMolecule
        """
        ...

    def _to_file_or_string(self, file_writer, string_writer, filename=None, mode='w+', binary=False, **converter_opts):
        """
        **LLM Docstring**

        Shared helper for the `to_*` exporters: write the mol either to a file (via a
        file writer) or to a returned string (via a string writer), synthesizing the
        missing path through a temporary file when only one writer is available.

        :param file_writer: the file-writing function (or `None`)
        :type file_writer: Callable | None
        :param string_writer: the string-writing function (or `None`)
        :type string_writer: Callable | None
        :param filename: the output file path (or `None` to return a string)
        :type filename: str | None
        :param mode: the file open mode
        :type mode: str
        :param binary: treat the content as binary
        :type binary: bool
        :param converter_opts: extra options for the writer
        :return: the file path, or the serialized string
        :rtype: str | bytes
        """
        ...

    def to_xyz(self, filename=None, conf_id=None, **opts):
        """
        **LLM Docstring**

        Serialize the molecule to XYZ (returned as a string, or written to a file).

        :param filename: the output file path (or `None` to return a string)
        :type filename: str | None
        :param conf_id: the conformer id
        :type conf_id: int | None
        :param opts: extra writer options
        :return: the file path or XYZ string
        :rtype: str
        """
        ...

    def to_molblock(self, filename=None, conf_id=None, **opts):
        """
        **LLM Docstring**

        Serialize the molecule to an MDL molblock (returned as a string, or written to a
        file).

        :param filename: the output file path (or `None` to return a string)
        :type filename: str | None
        :param conf_id: the conformer id
        :type conf_id: int | None
        :param opts: extra writer options
        :return: the file path or molblock string
        :rtype: str
        """
        ...

    def to_mrv(self, filename=None, conf_id=None, **opts):
        """
        **LLM Docstring**

        Serialize the molecule to Marvin MRV (returned as a string, or written to a
        file).

        :param filename: the output file path (or `None` to return a string)
        :type filename: str | None
        :param conf_id: the conformer id
        :type conf_id: int | None
        :param opts: extra writer options
        :return: the file path or MRV string
        :rtype: str
        """
        ...

    def to_pdb(self, filename=None, conf_id=None, **opts):
        """
        **LLM Docstring**

        Serialize the molecule to PDB (returned as a string, or written to a file).

        :param filename: the output file path (or `None` to return a string)
        :type filename: str | None
        :param conf_id: the conformer id
        :type conf_id: int | None
        :param opts: extra writer options
        :return: the file path or PDB string
        :rtype: str
        """
        ...

    def to_cml(self, filename=None, **opts):
        """
        **LLM Docstring**

        Serialize the molecule to CML (returned as a string, or written to a file).

        :param filename: the output file path (or `None` to return a string)
        :type filename: str | None
        :param opts: extra writer options
        :return: the file path or CML string
        :rtype: str
        """
        ...

    def _write_sdf(self, mol, file, base_writer=None, id_col=None, conf_ids=None):
        """
        **LLM Docstring**

        Write the mol (optionally multiple conformers) to an SDF stream, creating an
        `SDWriter` when one isn't supplied.

        :param mol: the mol to write
        :type mol: Chem.Mol
        :param file: the output file/stream
        :param base_writer: an existing SD writer to reuse
        :param id_col: the id column for the writer
        :param conf_ids: the conformer ids to write (all in one record if omitted)
        :type conf_ids: Sequence | None
        :return: the file that was written
        :rtype: object
        """
        ...

    def to_sdf(self, filename=None, **opts):
        """
        **LLM Docstring**

        Serialize the molecule to SDF (returned as a string, or written to a file).

        :param filename: the output file path (or `None` to return a string)
        :type filename: str | None
        :param opts: extra writer options (e.g. `conf_ids`)
        :return: the file path or SDF string
        :rtype: str
        """
        ...

    @classmethod
    def allchem_api(cls):
        """
        **LLM Docstring**

        Return the RDKit `Chem.AllChem` submodule.

        :return: the `AllChem` module
        :rtype: module
        """
        ...

    @classmethod
    def get_force_field_type(cls, ff_type):
        """
        **LLM Docstring**

        Resolve a force-field name to the RDKit `(force_field_getter, property_generator)`
        pair.

        :param ff_type: the force-field name (`'mmff'`/`'uff'`) or an existing pair
        :type ff_type: str | tuple
        :return: the force-field getter (and property generator)
        :rtype: tuple
        """
        ...

    def get_force_field(self, force_field_type='mmff', conf=None, mol=None, conf_id=None, **extra_props):
        """
        **LLM Docstring**

        Build an RDKit force-field object for a conformer, computing any needed
        force-field properties.

        :param force_field_type: the force-field name or getter pair
        :type force_field_type: str | tuple
        :param conf: an explicit conformer
        :param mol: an explicit mol
        :param conf_id: the conformer id
        :type conf_id: int | None
        :param extra_props: extra keyword arguments for the force-field getter
        :return: the force-field object
        :rtype: object
        """
        ...

    def evaluate_charges(self, coords, model='gasteiger'):
        """
        **LLM Docstring**

        Compute the per-atom partial charges for a set of coordinates (currently only
        the Gasteiger model).

        :param coords: the coordinates (used to set the conformer)
        :type coords: np.ndarray
        :param model: the charge model
        :type model: str
        :return: the partial charges
        :rtype: list[float]
        :raises ValueError: for an unsupported charge model
        """
        ...

    def calculate_energy(self, geoms=None, force_field_generator=None, force_field_type='mmff', conf_id=None):
        """
        **LLM Docstring**

        Compute the force-field energy of the current geometry, or of each geometry in a
        batch.

        :param geoms: a batch of geometries (or `None` for the current one)
        :type geoms: np.ndarray | None
        :param force_field_generator: a force-field factory (defaults to `get_force_field`)
        :type force_field_generator: Callable | None
        :param force_field_type: the force-field name
        :type force_field_type: str
        :param conf_id: the conformer id
        :type conf_id: int | None
        :return: the energy (or array of energies)
        :rtype: float | np.ndarray
        """
        ...

    def calculate_gradient(self, geoms=None, force_field_generator=None, force_field_type='mmff', conf_id=None):
        """
        **LLM Docstring**

        Compute the force-field energy gradient of the current geometry, or of each
        geometry in a batch.

        :param geoms: a batch of geometries (or `None` for the current one)
        :type geoms: np.ndarray | None
        :param force_field_generator: a force-field factory (defaults to `get_force_field`)
        :type force_field_generator: Callable | None
        :param force_field_type: the force-field name
        :type force_field_type: str
        :param conf_id: the conformer id
        :type conf_id: int | None
        :return: the gradient (or batch of gradients)
        :rtype: np.ndarray
        """
        ...

    def calculate_hessian(self, force_field_generator=None, force_field_type='mmff', stencil=5, mesh_spacing=0.01, **fd_opts):
        """
        **LLM Docstring**

        Compute the force-field Hessian at the current geometry by finite-differencing
        the analytic gradient.

        :param force_field_generator: a force-field factory
        :type force_field_generator: Callable | None
        :param force_field_type: the force-field name
        :type force_field_type: str
        :param stencil: the finite-difference stencil size
        :type stencil: int
        :param mesh_spacing: the finite-difference step
        :type mesh_spacing: float
        :param fd_opts: extra finite-difference options
        :return: the Hessian tensor
        :rtype: np.ndarray
        """
        ...

    def get_optimizer_params(self, maxAttempts=1000, useExpTorsionAnglePrefs=True, useBasicKnowledge=True, **etc):
        """
        **LLM Docstring**

        Build an RDKit ETKDGv3 parameter object for structure optimization/embedding.

        :param maxAttempts: the maximum embedding attempts
        :type maxAttempts: int
        :param useExpTorsionAnglePrefs: use experimental torsion prefs
        :type useExpTorsionAnglePrefs: bool
        :param useBasicKnowledge: use basic chemical knowledge
        :type useBasicKnowledge: bool
        :param etc: extra parameters set on the params object
        :return: the parameter object
        :rtype: object
        """
        ...

    def optimize_structure(self, geoms=None, force_field_type='mmff', optimizer=None, maxIters=1000, **opts):
        """
        **LLM Docstring**

        Force-field optimize the current geometry, or each geometry in a batch, returning
        the optimizer status and optimized coordinates.

        :param geoms: a batch of geometries (or `None` for the current one)
        :type geoms: np.ndarray | None
        :param force_field_type: the force-field name
        :type force_field_type: str
        :param optimizer: a custom optimizer callable
        :type optimizer: Callable | None
        :param maxIters: the maximum optimization iterations
        :type maxIters: int
        :param opts: extra optimizer options
        :return: `(status, optimized_coords, extra)`
        :rtype: tuple
        """
        ...

    def show(self):
        """
        **LLM Docstring**

        Display an interactive 3D rendering of the current conformer (via RDKit's
        IPython 3D console).

        :return: the 3D display
        :rtype: object
        """
        ...
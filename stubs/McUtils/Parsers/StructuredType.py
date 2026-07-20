import numpy as np
from collections import OrderedDict
__all__ = ['StructuredType', 'StructuredTypeArray', 'DisappearingType']

class StructuredType:
    """
    Represents a structured type with a defined calculus to simplify the construction of combined types when writing
    parsers that take multi-typed data

    Supports a compound StructuredType where the types are keyed
    """

    def __init__(self, base_type, shape=None, is_alternative=False, is_optional=False, default_value=None):
        """
        **LLM Docstring**

        Normalize a primitive, shaped primitive, alternative, optional, or compound dtype specification and choose an explicit or inferred missing-value sentinel.

        :param base_type: the primitive or compound type specification
        :type base_type: object

        :param shape: the required or inferred array shape
        :type shape: object

        :param is_alternative: whether the specification represents alternative accepted types
        :type is_alternative: object

        :param is_optional: whether missing values are allowed
        :type is_optional: object

        :param default_value: the value used for optional or unmatched data
        :type default_value: object
        """
        ...

    def _infer_default_value(self):
        """
        **LLM Docstring**

        Choose `[NaN]` for strings, a large negative integer sentinel for integer types, `NaN` for floating types, and `None` otherwise.

        :return: choose `[NaN]` for strings, a large negative integer sentinel for integer types, `NaN` for floating types, and `None` otherwise.
        :rtype: object
        """
        ...

    @property
    def is_simple(self):
        """
        **LLM Docstring**

        Report whether the specification is an unqualified primitive type (or `None`) rather than an optional, alternative, or compound structure.

        :return: `True` when the condition described above holds; otherwise `False`.
        :rtype: bool
        """
        ...

    def add_types(self, other):
        """
        Constructs a new type by treating the two objects as siblings, that is if they can be merged due to type and
        shape similarity they will be, otherwise a non-nesting structure will be constructed from them

        We'll also want a nesting version of this I'm guessing, which probably we hook into __call__

        :param other:
        :type other:
        :return:
        :rtype:
        """
        ...

    def __add__(self, other):
        """
        **LLM Docstring**

        Combine sibling type specifications using `add_types`.

        :param other: the pattern or type combined with this object
        :type other: object

        :return: combine sibling type specifications using `add_types`.
        :rtype: object
        """
        ...

    def compound_types(self, other):
        """Creates a structured type where rather than merging types they simply compound onto one another

        :param other:
        :type other:
        :return:
        :rtype:
        """
        ...

    def __call__(self, other):
        """
        **LLM Docstring**

        Request nested type composition through `compound_types`, which is currently unimplemented.

        :param other: the pattern or type combined with this object
        :type other: object

        :return: request nested type composition through `compound_types`, which is currently unimplemented.
        :rtype: object
        """
        ...

    def repeat(self, n=None, m=None):
        """Returns a new version of the type, but with the appropriate shape for being repeated n-to-m times

        :param n:
        :type n:
        :param m:
        :type m:
        :return:
        :rtype:
        """
        ...

    def drop_axis(self, axis=0):
        """Returns a new version of the type, but with the appropriate shape for dropping an axis

        :param axis:
        :type axis: int
        :return:
        :rtype:
        """
        ...

    def extend_shape(self, base_shape):
        """Extends the shape of the type such that base_shape precedes the existing shape

        :param base_shape:
        :type base_shape:
        :return:
        :rtype:
        """
        ...

    def _condense_types(self, base_types, shape):
        """
        **LLM Docstring**

        Collapse identical child primitive types into one type with an added length axis when no conflicting outer shape is supplied.

        :param base_types: the child structured types considered for condensation
        :type base_types: object

        :param shape: the required or inferred array shape
        :type shape: object

        :return: collapse identical child primitive types into one type with an added length axis when no conflicting outer shape is supplied.
        :rtype: object
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Show the represented dtype and shape.

        :return: The regex source or textual representation constructed by the operation.
        :rtype: str
        """
        ...

class DisappearingTypeClass(StructuredType):
    """
    A special type that is entirely ignored in the structured type algebra
    """

    def __init__(self):
        """
        **LLM Docstring**

        Create the singleton type marker that is ignored when structured types are added together.
        """
        ...
DisappearingType = DisappearingTypeClass()
DisappearingType.__name__ = 'DisappearingType'
"\nSomething to think about w.r.t the correspondance between the stype shape and the stated shape of the \narray. \n\nThere are two possible setups, really, in the first setup we have two cases:\n    Simple stype => no shape for the stype\n    Compound stype => shape of array is one _larger_ than shape of stype\n\nIn the second case:\n    Simple dtype => no shape for the stype\n    Compound dtype => shape of array is the shape of the stype\n\nIt's not clear that either is better than the other, but whichever one is chose, we need to be\nconsistent throughout the code in how we work with it.\n"

class StructuredTypeArray:
    """
    Represents an array of objects defined by the StructuredType spec provided
    mostly useful as it dispatches to NumPy where things are simple enough to do so

    It has a system to dispatch intelligently based on the type of array provided
    The kinds of structures supported are: OrderedDict, list, and np.ndarray

    A _simple_ StructuredTypeArray is one that can just be represented as a single np.ndarray
    A _compound_ StructuredTypeArray requires either a list or OrderedDict of StructuredTypeArray subarrays
    """

    def __init__(self, stype, num_elements=50, padding_mode='fill', padding_value=None):
        """
        :param stype:
        :type stype: StructuredType
        :param num_elements: number of default elements in dynamically sized arrays
        :type num_elements: int
        """
        ...

    @property
    def is_simple(self):
        """Just returns wheter the core datatype is simple

        :return:
        :rtype:
        """
        ...

    @property
    def dict_like(self):
        """
        **LLM Docstring**

        Report whether compound storage is keyed by a dictionary or `OrderedDict`.

        :return: `True` when the condition described above holds; otherwise `False`.
        :rtype: bool
        """
        ...

    @property
    def extension_axis(self):
        """Determines which axis to extend when adding more memory to the array
        :return:
        :rtype:
        """
        ...

    @extension_axis.setter
    def extension_axis(self, ax):
        """
        **LLM Docstring**

        Get or set the axis used for growth; when unset, choose the first indeterminate axis, falling back to axis zero.

        :param ax: the explicit extension axis
        :type ax: object

        :return: get or set the axis used for growth; when unset, choose the first indeterminate axis, falling back to axis zero.
        :rtype: object
        """
        ...

    @property
    def shape(self):
        """
        **LLM Docstring**

        Get the filled shape of simple storage or the component shapes of compound storage; the setter stores an explicit cached shape.

        :param s: the shape assigned to the object
        :type s: object

        :return: The populated shape for simple storage or component shapes for compound storage.
        :rtype: object
        """
        ...

    @shape.setter
    def shape(self, s):
        """
        **LLM Docstring**

        Get the filled shape of simple storage or the component shapes of compound storage; the setter stores an explicit cached shape.

        :param s: the shape assigned to the object
        :type s: object

        :return: The populated shape for simple storage or component shapes for compound storage.
        :rtype: object
        """
        ...

    @property
    def block_size(self):
        """
        **LLM Docstring**

        Return the number of scalar values in one element along the extension axis, summing component block sizes for compound storage.

        :return: return the number of scalar values in one element along the extension axis, summing component block sizes for compound storage.
        :rtype: object
        """
        ...

    @property
    def append_depth(self):
        """
        **LLM Docstring**

        Get or set recursive append depth; changing it propagates the same increment to all compound subarrays.

        :param d: the new recursive append depth
        :type d: object

        :return: get or set recursive append depth; changing it propagates the same increment to all compound subarrays.
        :rtype: object
        """
        ...

    @append_depth.setter
    def append_depth(self, d):
        """
        **LLM Docstring**

        Get or set recursive append depth; changing it propagates the same increment to all compound subarrays.

        :param d: the new recursive append depth
        :type d: object

        :return: get or set recursive append depth; changing it propagates the same increment to all compound subarrays.
        :rtype: object
        """
        ...

    def _invalidate_type_cache(self):
        """Whenever the dtype and stype are changed we can use this to invalidate the cached forms

        :return:
        :rtype:
        """
        ...

    def _get_complex_dtype(self):
        """
        **LLM Docstring**

        Materialize compound child `StructuredType` objects, push any outer shape into each child, or reconstruct the parent type from existing subarrays.

        :return: materialize compound child `StructuredType` objects, push any outer shape into each child, or reconstruct the parent type from existing subarrays.
        :rtype: object
        """
        ...

    @property
    def dtype(self):
        """Returns the core data type held by the StructuredType that represents the array

        :return:
        :rtype:
        """
        ...

    @property
    def stype(self):
        """Returns the StructuredType that the array holds data for

        :return:
        :rtype:
        """
        ...

    @property
    def array(self):
        """
        **LLM Docstring**

        Return the filled slice of simple NumPy storage, or the complete tuple/mapping of compound subarrays.

        :return: The populated NumPy view or compound collection of populated subarrays.
        :rtype: object
        """
        ...

    @property
    def _subarrays(self):
        """
        **LLM Docstring**

        Iterate over compound child arrays, using mapping values for keyed storage.

        :return: iterate over compound child arrays, using mapping values for keyed storage.
        :rtype: object
        """
        ...

    def axis_shape_indeterminate(self, axis):
        """Tries to determine if an axis has had any data placed into it or otherwise been given a determined shape

        :param axis:
        :type axis:
        :return:
        :rtype:
        """
        ...

    @property
    def has_indeterminate_shape(self):
        """Tries to determine if the entire array has a determined shape

        :param axis:
        :type axis:
        :return:
        :rtype:
        """
        ...

    @property
    def filled_to(self):
        """
        **LLM Docstring**

        Get per-axis populated extents for simple storage or nested extents for compound storage; setting accepts an integer or extent sequence only for simple storage.

        :param filling: the populated extent or sequence of per-axis extents to record
        :type filling: object

        :return: The populated extent of each axis.
        :rtype: object
        """
        ...

    @filled_to.setter
    def filled_to(self, filling):
        """
        **LLM Docstring**

        Get per-axis populated extents for simple storage or nested extents for compound storage; setting accepts an integer or extent sequence only for simple storage.

        :param filling: the populated extent or sequence of per-axis extents to record
        :type filling: object

        :return: The populated extent of each axis.
        :rtype: object
        """
        ...

    def set_filling(self, amt, axis=0):
        """
        **LLM Docstring**

        Set one populated extent directly, propagating the update through compound children.

        :param amt: the populated extent to assign
        :type amt: object

        :param axis: the axis being inspected, changed, or extended
        :type axis: object

        :return: None.
        :rtype: None
        """
        ...

    def increment_filling(self, inc=1, axis=0):
        """
        **LLM Docstring**

        Increase one populated extent, propagating the increment through compound children.

        :param inc: the amount added to the populated extent
        :type inc: object

        :param axis: the axis being inspected, changed, or extended
        :type axis: object

        :return: None.
        :rtype: None
        """
        ...

    def __len__(self):
        """
        **LLM Docstring**

        Return the length of the currently filled array view.

        :return: The number of populated top-level elements.
        :rtype: int
        """
        ...

    def empty_array(self, shape=None, num_elements=None):
        """Creates empty arrays with (potentially) default elements

        The shape handling rules operate like this:
            if shape is None, we assume we'll initialize this as an array with a single element to be filled out
            if shape is (None,) or (n,) we'll initialize this as an array with multiple elments to be filled out
            otherwise we'll just take the specified shape

        :param num_elements:
        :type num_elements:
        :return:
        :rtype:
        """
        ...

    def extend_array(self, axis=None):
        """
        **LLM Docstring**

        Grow storage by concatenating an equally shaped empty block along the extension axis, recursively growing compound children.

        :param axis: the axis being inspected, changed, or extended
        :type axis: object

        :return: None.
        :rtype: None
        """
        ...

    def __setitem__(self, key, value):
        """
        **LLM Docstring**

        Assign through `set_part`, including automatic growth and recursive compound dispatch.

        :param key: the name assigned to a captured group
        :type key: object

        :param value: the value assigned into the structured array
        :type value: object

        :return: None.
        :rtype: None
        """
        ...

    def set_part(self, key, value):
        """Recursively sets parts of an array if not simple, otherwise just delegates to NumPy

        :param key:
        :type key:
        :param value:
        :type value:
        :return:
        :rtype:
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Read through `get_part` from the filled array view rather than unused capacity.

        :param item: the child key or array index/slice being accessed
        :type item: object

        :return: The named child or populated array portion selected by the index.
        :rtype: object
        """
        ...

    def get_part(self, item, use_full_array=True):
        """If simple, delegates to NumPy, otherwise tries to recursively get parts...?
        Unclear how slicing is best handled here.

        :param item:
        :type item:
        :return:
        :rtype:
        """
        ...

    def add_axis(self, which=0, num_elements=None, change_shape=True):
        """Adds an axis to the array, generally used for expanding from singular or 1D data to higher dimensional
        This happens with parse_all and repeated things like that

        :param which:
        :type which:
        :param num_elements:
        :type num_elements:
        :return:
        :rtype:
        """
        ...

    def can_cast(self, val):
        """Determines whether val can probably be cast to the right return type and shape without further processing or if that's definitely not possible

        :param val:
        :type val:
        :return:
        :rtype:
        """
        ...

    def append(self, val, axis=0):
        """
        Puts val in the first empty slot in the array

        :param val:
        :type val:
        :return:
        :rtype:
        """
        ...

    def _get_casting_shape(self, val, axis=None):
        """
        **LLM Docstring**

        Determine whether input values can be reshaped by changing only the extension axis, returning the inferred axis length and any fractional remainder.

        :param val: the value or values being tested, appended, or extended
        :type val: object

        :param axis: the axis being inspected, changed, or extended
        :type axis: object

        :return: determine whether input values can be reshaped by changing only the extension axis, returning the inferred axis length and any fractional remainder.
        :rtype: object
        """
        ...

    def extend(self, val, single=True, prepend=False, axis=None):
        """Adds the sequence val to the array

        :param val:
        :type val:
        :param single: a flag that indicates whether val can be treated as a single object or if it needs to be reshapen when handling in non-simple case
        :type single: bool
        :return:
        :rtype:
        """
        ...

    def fill(self, array):
        """Sets the result array to be the passed array

        :param array:
        :type array: str | np.ndarray
        :return:
        :rtype:
        """
        ...

    def cast_to_array(self, txt):
        """Casts a string of things with a given data type to an array of that type and does some optional
        shape coercion

        :param txt:
        :type txt: str | iterable[str]
        :return:
        :rtype:
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Show the populated shape and resolved dtype.

        :return: The regex source or textual representation constructed by the operation.
        :rtype: str
        """
        ...

class StructuredTypeArrayException(Exception):
    ...
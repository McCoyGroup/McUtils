import ast, abc, copy
import numpy as np
ellipsis = type(...)
__all__ = ['Abstract']

class ASTUtils:
    """
    Provides utilities for writing easier AST expressions
    by essentially allowing for the creation of an alternate,
    less-annotated tree that can be manipulated naturally using
    python operations and then can record and replay those ops
    """

    @staticmethod
    def ast_var(var):
        ...

    @classmethod
    def ast_attr(cls, obj, attr):
        ...

    @classmethod
    def astify(cls, val):
        ...

    @classmethod
    def prep_args(cls, args):
        ...

    @classmethod
    def ast_call(cls, fn, *args, **kwargs):
        ...

    @classmethod
    def ast_arglist(cls, spec):
        ...

    @classmethod
    def ast_const(cls, value):
        ...

    @classmethod
    def ast_iterable(cls, otype, values):
        ...

    @classmethod
    def ast_list(cls, *values):
        ...

    @classmethod
    def ast_tuple(cls, *values):
        ...

    @classmethod
    def ast_set(cls, *values):
        ...

    @classmethod
    def ast_dict(cls, **key_pairs):
        ...

    @classmethod
    def ast_comprehension(cls, var, iterable, filter=None):
        ...

    @classmethod
    def ast_type_comprehension(cls, otype, expr, comprehension, iterable=None, filter=None):
        ...

    @classmethod
    def ast_generator(cls, expr, comprehension, iterable=None, filter=None):
        ...

    @classmethod
    def ast_list_comprehension(cls, expr, comprehension, iterable=None, filter=None):
        ...

    @classmethod
    def ast_set_comprehension(cls, expr, comprehension, iterable=None, filter=None):
        ...

    @classmethod
    def ast_dict_comprehension(cls, key_expr, value_expr, comprehension, iterable=None, filter=None):
        ...

    @classmethod
    def ast_lambda(cls, spec, body):
        ...

    class ContextModifier(ast.NodeTransformer):

        def __init__(self, ctx):
            ...

        def generic_visit(self, node: ast.AST) -> ast.AST:
            ...

    @classmethod
    def ast_assign(cls, targets, value):
        ...

    @classmethod
    def ast_boolop(cls, op, left, right, *extra):
        ...

    @classmethod
    def ast_and(cls, left, right, *extra):
        ...

    @classmethod
    def ast_or(cls, left, right, *extra):
        ...

    @classmethod
    def ast_binop(cls, op, left, right):
        ...

    @classmethod
    def ast_add(cls, left, right):
        ...

    @classmethod
    def ast_sub(cls, left, right):
        ...

    @classmethod
    def ast_mult(cls, left, right):
        ...

    @classmethod
    def ast_div(cls, left, right):
        ...

    @classmethod
    def ast_matmult(cls, left, right):
        ...

    @classmethod
    def ast_floordiv(cls, left, right):
        ...

    @classmethod
    def ast_pow(cls, left, right):
        ...

    @classmethod
    def ast_mod(cls, left, right):
        ...

    @classmethod
    def ast_bitxor(cls, left, right):
        ...

    @classmethod
    def ast_bitand(cls, left, right):
        ...

    @classmethod
    def ast_bitor(cls, left, right):
        ...

    @classmethod
    def ast_comp(cls, op, left, right, *extra):
        ...

    @classmethod
    def ast_eq(cls, left, right, *extra):
        ...

    @classmethod
    def ast_ne(cls, left, right, *extra):
        ...

    @classmethod
    def ast_lt(cls, left, right, *extra):
        ...

    @classmethod
    def ast_gt(cls, left, right, *extra):
        ...

    @classmethod
    def ast_lte(cls, left, right, *extra):
        ...

    @classmethod
    def ast_gte(cls, left, right, *extra):
        ...

    @classmethod
    def ast_in(cls, left, right, *extra):
        ...

    @classmethod
    def ast_ni(cls, left, right, *extra):
        ...

    @classmethod
    def ast_is(cls, left, right, *extra):
        ...

    @classmethod
    def ast_isnt(cls, left, right, *extra):
        ...

    @classmethod
    def ast_unop(cls, op, val):
        ...

    @classmethod
    def ast_not(cls, val):
        ...

    @classmethod
    def ast_inv(cls, val):
        ...

    @classmethod
    def ast_pos(cls, val):
        ...

    @classmethod
    def ast_neg(cls, val):
        ...

    @classmethod
    def ast_star(cls, iterable):
        ...

    @classmethod
    def ast_ternary(cls, test, body, orelse):
        ...

    @classmethod
    def ast_subscript(cls, value, index):
        ...

    @classmethod
    def ast_index(cls, value):
        ...

    @classmethod
    def ast_slice(cls, start=None, stop=None, step=None):
        ...

    @classmethod
    def convert(cls, val) -> 'AbstractExpr':
        ...

class AbstractExpr(metaclass=abc.ABCMeta):
    __tag__ = None
    __slots__ = []

    def __hash__(self):
        ...

    @abc.abstractmethod
    def to_ast(self) -> 'ast.AST':
        ...

    def to_eval_expr(self):
        ...

    def compile(self, namespace=None):
        ...

    def transmogrify(self, converter_dispatch: dict):
        ...

    def __call__(self, *args, **kwargs):
        ...

    def __not__(self):
        ...

    def __invert__(self):
        ...

    def __pos__(self):
        ...

    def __neg__(self):
        ...

    def __add__(self, other):
        ...

    def __radd__(self, other):
        ...

    def __sub__(self, other):
        ...

    def __mul__(self, other):
        ...

    def __rmul__(self, other):
        ...

    def __pow__(self, other):
        ...

    def __truediv__(self, other):
        ...

    def __floordiv__(self, other):
        ...

    def __xor__(self, other):
        ...

    def __rxor__(self, other):
        ...

    def __or__(self, other):
        ...

    def __ror__(self, other):
        ...

    def __and__(self, other):
        ...

    def __rand__(self, other):
        ...

    def __contains__(self, item):
        ...

    def __abs__(self):
        ...

    def __floor__(self):
        ...

    def __ceil__(self):
        ...

    def __iter__(self):
        ...

    def keys(self):
        ...

    def __getitem__(self, item):
        ...

    def __getattr__(self, item):
        ...

    def Equals(self, right):
        ...
    Eq = Equals

    def LessThan(self, right):
        ...
    Lt = LessThan

    def LessEquals(self, right):
        ...
    LtE = LessEquals

    def GreaterThan(self, right):
        ...
    Gt = GreaterThan

    def GreaterEquals(self, right):
        ...
    GtE = GreaterEquals

    def And(self, right):
        ...

    def Or(self, right):
        ...

    def Is(self, other):
        ...

    def IsNot(self, other):
        ...
    Isnt = IsNot

    def generator(self, expr, var, filter=None):
        ...
    Gen = generator

    def list_comp(self, expr, var, filter=None):
        ...
    LC = list_comp

    def set_comp(self, expr, var, filter=None):
        ...
    SC = set_comp

    def dict_comp(self, key_expr, value_expr, var, filter=None):
        ...
    DC = dict_comp

    def if_test(self, test, else_expr=None):
        ...

    def if_self(self, expr, else_expr=None):
        ...

    def __repr__(self):
        ...

class AbstractName(AbstractExpr):
    __tag__ = 'Name'
    __slots__ = ['name']

    def __init__(self, name):
        ...

    def to_ast(self) -> 'ast.Name':
        ...

    def __repr__(self):
        ...

class AbstractConstant(AbstractExpr):
    __tag__ = 'Const'
    __slots__ = ['value']

    def __init__(self, value):
        ...

    def to_ast(self):
        ...

    def __repr__(self):
        ...

class AbstractCall(AbstractExpr):
    __tag__ = 'Call'
    __slots__ = ['fn', 'args', 'kwargs']

    def __init__(self, fn, *args, **kwargs):
        ...

    def to_ast(self) -> 'ast.Call':
        ...

    def __repr__(self):
        ...

class AbstractAttribute(AbstractExpr):
    __tag__ = 'Attr'
    __slots__ = ['obj', 'attr']

    def __init__(self, obj, attr):
        ...

    def to_ast(self) -> 'ast.Attribute':
        ...

    def __repr__(self):
        ...

class AbstractBinOp(AbstractExpr):
    __slots__ = ['left', 'right']

    def __init__(self, left, right):
        ...

class AbstractAdd(AbstractBinOp):
    __tag__ = 'Add'

    def to_ast(self) -> 'ast.BinOp':
        ...

class AbstractSub(AbstractBinOp):
    __tag__ = 'Sub'

    def to_ast(self) -> 'ast.BinOp':
        ...

class AbstractMult(AbstractBinOp):
    __tag__ = 'Mul'

    def to_ast(self) -> 'ast.BinOp':
        ...

class AbstractDiv(AbstractBinOp):
    __tag__ = 'Div'

    def to_ast(self) -> 'ast.BinOp':
        ...

class AbstractMatMult(AbstractBinOp):
    __tag__ = 'MatMul'

    def to_ast(self) -> 'ast.BinOp':
        ...

class AbstractFloorDiv(AbstractBinOp):
    __tag__ = 'FloorDiv'

    def to_ast(self) -> 'ast.BinOp':
        ...

class AbstractPow(AbstractBinOp):
    __tag__ = 'Pow'

    def to_ast(self) -> 'ast.BinOp':
        ...

class AbstractMod(AbstractBinOp):
    __tag__ = 'Mod'

    def to_ast(self) -> 'ast.BinOp':
        ...

class AbstractBitXOr(AbstractBinOp):
    __tag__ = 'BitXOr'

    def to_ast(self) -> 'ast.BinOp':
        ...

class AbstractBitOr(AbstractBinOp):
    __tag__ = 'BitOr'

    def to_ast(self) -> 'ast.BinOp':
        ...

class AbstractBitAnd(AbstractBinOp):
    __tag__ = 'BitAnd'

    def to_ast(self) -> 'ast.BinOp':
        ...

class AbstractUnOp(AbstractExpr):
    __slots__ = ['operand']

    def __init__(self, operand):
        ...

class AbstractNot(AbstractUnOp):
    __tag__ = 'Not'

    def to_ast(self) -> 'ast.UnaryOp':
        ...

class AbstractInv(AbstractUnOp):
    __tag__ = 'Inv'

    def to_ast(self) -> 'ast.UnaryOp':
        ...

class AbstractPos(AbstractUnOp):
    __tag__ = 'Pos'

    def to_ast(self) -> 'ast.UnaryOp':
        ...

class AbstractNeg(AbstractUnOp):
    __tag__ = 'Neg'

    def to_ast(self) -> 'ast.UnaryOp':
        ...

class AbstractComp(AbstractExpr):
    __slots__ = ['left', 'right', 'extra']

    def __init__(self, left, right, *extra):
        ...

class AbstractEq(AbstractComp):
    __tag__ = 'Equals'

    def to_ast(self) -> 'ast.Compare':
        ...

class AbstractNotEq(AbstractComp):
    __tag__ = 'NotEquals'

    def to_ast(self) -> 'ast.Compare':
        ...

class AbstractLt(AbstractComp):
    __tag__ = 'Less'

    def to_ast(self) -> 'ast.Compare':
        ...

class AbstractGt(AbstractComp):
    __tag__ = 'Greater'

    def to_ast(self) -> 'ast.Compare':
        ...

class AbstractLtE(AbstractComp):
    __tag__ = 'LessEquals'

    def to_ast(self) -> 'ast.Compare':
        ...

class AbstractGtE(AbstractComp):
    __tag__ = 'GreaterEquals'

    def to_ast(self) -> 'ast.Compare':
        ...

class AbstractIn(AbstractComp):
    __tag__ = 'In'

    def to_ast(self) -> 'ast.Compare':
        ...

class AbstractNotIn(AbstractComp):
    __tag__ = 'NotIn'

    def to_ast(self) -> 'ast.Compare':
        ...

class AbstractIs(AbstractComp):
    __tag__ = 'Is'

    def to_ast(self) -> 'ast.Compare':
        ...

class AbstractIsNot(AbstractComp):
    __tag__ = 'IsNot'

    def to_ast(self) -> 'ast.Compare':
        ...

class AbstractSubscript(AbstractExpr):
    __tag__ = 'Subscript'
    __slots__ = ['obj', 'index']

    def __init__(self, obj, index):
        ...

    def to_ast(self):
        ...

class AbstractBoolOp(AbstractExpr):
    __slots__ = ['left', 'right', 'extra']

    def __init__(self, left, right, *extra):
        ...

class AbstractAnd(AbstractComp):
    __tag__ = 'And'

    def to_ast(self) -> 'ast.BoolOp':
        ...

class AbstractOr(AbstractComp):
    __tag__ = 'Or'

    def to_ast(self) -> 'ast.BoolOp':
        ...

class AbstractImportModule(AbstractCall):

    def __init__(self, mod):
        ...

class AbstractAbs(AbstractCall):

    def __init__(self, val):
        ...

class AbstractFloor(AbstractCall):

    def __init__(self, val):
        ...

class AbstractCeil(AbstractCall):

    def __init__(self, val):
        ...

class AbstractIter(AbstractCall):

    def __init__(self, val):
        ...

class AbstractStar(AbstractExpr):
    __tag__ = 'Star'
    __slots__ = ['iterable']

    def __init__(self, iterable):
        ...

    def to_ast(self) -> 'ast.Starred':
        ...

class AbstractStarOrIter(AbstractExpr):
    __tag__ = 'StarOrIter'
    __slots__ = ['val']

    def __init__(self, val):
        ...

    def to_iter(self):
        ...

    def to_star(self):
        ...

    def to_ast(self) -> 'ast.AST':
        ...

class AbstractUnwrapKeys(str):
    __tag__ = 'UnwrapKeys'
    __slots__ = ['val']

    def __new__(cls, content):
        ...

    def __init__(self, val):
        ...

    def to_iter(self):
        ...

    def to_starstar(self):
        ...

    def to_ast(self) -> 'ast.AST':
        ...

class AbstractStarStar(AbstractExpr):
    __tag__ = 'StarStar'
    __slots__ = ['var']

    def __init__(self, var):
        ...

    def to_ast(self):
        ...

class AbstractList(AbstractExpr):
    __tag__ = 'List'
    __slots__ = ['args']

    def __init__(self, *args):
        ...

    def to_ast(self) -> 'ast.List':
        ...

class AbstractTuple(AbstractExpr):
    __tag__ = 'Tuple'
    __slots__ = ['args']

    def __init__(self, *args):
        ...

    def to_ast(self) -> 'ast.Tuple':
        ...

class AbstractSet(AbstractExpr):
    __tag__ = 'Set'
    __slots__ = ['args']

    def __init__(self, *args):
        ...

    def to_ast(self) -> 'ast.Set':
        ...

class AbstractDict(AbstractExpr):
    __tag__ = 'Dict'
    __slots__ = ['kwargs']

    def __init__(self, **kwargs):
        ...

    def to_ast(self) -> 'ast.Dict':
        ...

class AbstractListComp(AbstractExpr):
    __tag__ = 'ListComp'
    __slots__ = ['expr', 'var', 'iterable', 'filter']

    def __init__(self, expr, var, iterable, filter=None):
        ...

    def to_ast(self) -> 'ast.ListComp':
        ...

class AbstractGenerator(AbstractExpr):
    __tag__ = 'Generator'
    __slots__ = ['expr', 'var', 'iterable', 'filter']

    def __init__(self, expr, var, iterable, filter=None):
        ...

    def to_ast(self) -> 'ast.GeneratorExp':
        ...

class AbstractSetComp(AbstractExpr):
    __tag__ = 'SetComp'
    __slots__ = ['expr', 'var', 'iterable', 'filter']

    def __init__(self, expr, var, iterable, filter=None):
        ...

    def to_ast(self) -> 'ast.SetComp':
        ...

class AbstractDictComp(AbstractExpr):
    __tag__ = 'DictComp'
    __slots__ = ['key_expr', 'value_expr', 'var', 'iterable', 'filter']

    def __init__(self, key_expr, value_expr, var, iterable, filter=None):
        ...

    def to_ast(self) -> 'ast.DictComp':
        ...

class AbstractArgSpec(AbstractExpr):
    __tag__ = 'ArgSpec'
    __slots__ = ['args', 'kwargs']

    def __init__(self, *args, **kwargs):
        ...

    def to_ast(self) -> 'ast.arguments':
        ...

    def __repr__(self):
        ...

class AbstractLambda(AbstractExpr):
    __tag__ = 'Lambda'
    __slots__ = ['spec', 'body']

    def __init__(self, *args, **kwargs):
        ...

    def __call__(self, *args, **kwargs):
        ...

    def to_ast(self) -> 'ast.Lambda':
        ...

    def __repr__(self):
        ...

class AbstractIfExp(AbstractExpr):
    __tag__ = 'If'
    __slots__ = ['test', 'body', 'else_branch']

    def __init__(self, test, body, orelse=None):
        ...

    def orelse(self, orelse):
        ...

    def to_ast(self):
        ...

class Abstract:
    """
    Provides a namespace for the different abstract classes
    """

    @classmethod
    def vars(cls, *spec, symbol_type=None):
        ...
    Expr = AbstractExpr
    Name = AbstractName
    Lambda = AbstractLambda
    List = AbstractList
    Tuple = AbstractTuple
    Set = AbstractSet
    Dict = AbstractDict
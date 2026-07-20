import sys, os, pathlib, abc, enum, types, string, inspect
import ast, functools, re, fnmatch, collections
import typing, itertools, builtins
from typing import *

from ... import Devutils as dev
from .ObjectWalker import *
__reload_hook__ = [".ObjectWalker"]

__all__ = [
    "TemplateFormatter",
    "FormatDirective",
    "TemplateFormatDirective",
    "TemplateOps",
    "TemplateEngine",
    "ResourceLocator",
    "TemplateResourceExtractor",
    "TemplateWalker",
    "TemplateHandler",
    "ModuleTemplateHandler",
    "ClassTemplateHandler",
    "FunctionTemplateHandler",
    "MethodTemplateHandler",
    "ObjectTemplateHandler",
    "IndexTemplateHandler",
    "TemplateInterfaceEngine",
    "TemplateInterfaceFormatter"
]

class TemplateOps:
    @staticmethod
    def loop(caller: typing.Callable, *args, joiner="", formatter=None, **kwargs):
        """
        **LLM Docstring**

        Call a template operation over synchronized positional and keyword iterables and optionally join the results.

        :param caller: the callable applied to each synchronized argument group
        :type caller: typing.Callable
        :param joiner: the string used to combine generated values, or `None` to keep a list
        :type joiner: Any
        :param formatter: the active template formatter
        :type formatter: Any
        :param args: positional arguments forwarded to the wrapped callable
        :type args: Any
        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Any

        :return: A joined string when `joiner` is not `None`; otherwise the list of callback results.
        :rtype: Any
        """
        if len(kwargs) == 0:
            res = [caller(*a) for a in zip(*args)]
        elif len(args) == 0:
            res = [
                caller(**{k:v for k,v in zip(kwargs.keys(), kv)})
                for kv in zip(*kwargs.values())
            ]
        else:
            res = [
                caller(*a, **{k:v for k,v in zip(kwargs.keys(), kv)})
                for a,kv in zip(zip(*args), zip(*kwargs.values()))
            ]
        if joiner is not None:
            res = joiner.join(res)
        return res
    @classmethod
    def loop_template(cls, template:str, *args, joiner="", formatter=None, **kwargs):
        """
        **LLM Docstring**

        Format a string template over synchronized iterables using `loop`.

        :param template: the template name, template text, or template callable
        :type template: str
        :param joiner: the string used to combine generated values, or `None` to keep a list
        :type joiner: Any
        :param formatter: the active template formatter
        :type formatter: Any
        :param args: positional arguments forwarded to the wrapped callable
        :type args: Any
        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Any

        :return: The rendered iterations joined by `joiner`, or the list of rendered values when `joiner` is `None`.
        :rtype: Any
        """
        return cls.loop(
            template.format,
            *args,
            joiner=joiner,
            formatter=formatter,
            **kwargs
        )
    @staticmethod
    def join(*args, joiner=" ", formatter=None):
        """
        **LLM Docstring**

        Join a sequence of strings, accepting either separate values or one non-string iterable.

        :param joiner: the string used to combine generated values, or `None` to keep a list
        :type joiner: Any
        :param formatter: the active template formatter
        :type formatter: Any
        :param args: positional arguments forwarded to the wrapped callable
        :type args: Any

        :return: The input strings combined with `joiner`.
        :rtype: Any
        """
        if len(args) == 1 and not isinstance(args[0], str):
            args = args[0]
        return joiner.join(args)
    @classmethod
    def load(cls, template, formatter=None):
        """
        **LLM Docstring**

        Load a named template through the active formatter.

        :param template: the template name, template text, or template callable
        :type template: Any
        :param formatter: the active template formatter
        :type formatter: Any

        :return: The template content returned by the formatter.
        :rtype: Any
        """
        return formatter.load_template(template)
    @classmethod
    def include(cls, template, formatter=None):
        """
        **LLM Docstring**

        Load and immediately render another template using the current format parameters.

        :param template: the template name, template text, or template callable
        :type template: Any
        :param formatter: the active template formatter
        :type formatter: Any

        :return: The included template rendered with the current parameter scope.
        :rtype: Any
        """
        return formatter.vformat(formatter.load_template(template), (), formatter.format_parameters)
    @classmethod
    def apply(cls, template, *args, formatter=None, **kwargs):
        """
        **LLM Docstring**

        Render a template with explicit arguments through the active formatter.

        :param template: the template name, template text, or template callable
        :type template: Any
        :param formatter: the active template formatter
        :type formatter: Any
        :param args: positional arguments forwarded to the wrapped callable
        :type args: Any
        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Any

        :return: The rendered template string.
        :rtype: Any
        """
        if formatter is None:
            raise ValueError("`{}` can't be `None`".format('formatter'))
        return formatter.format(template, *args, **kwargs)
    @classmethod
    def nonempty(cls, data, formatter=None):
        """
        **LLM Docstring**

        Test whether a value is non-`None` and has positive length.

        :param data: the value or collection being tested
        :type data: Any
        :param formatter: the active template formatter
        :type formatter: Any

        :return: `True` when `data` is non-`None` and nonempty; otherwise `False`.
        :rtype: Any
        """
        return data is not None and len(data) > 0
    @classmethod
    def wrap(cls, fn):
        """
        **LLM Docstring**

        Adapt a callable so it accepts and ignores the formatter keyword injected into directives.

        :param fn: the callable to wrap
        :type fn: Any

        :return: A wrapper callable that ignores the injected formatter keyword.
        :rtype: Any
        """
        @functools.wraps(fn)
        def f(*args, formatter=None, **kwargs):
            """
            **LLM Docstring**

            Forward directive arguments to the wrapped callable while discarding the formatter keyword.

            :param formatter: the active template formatter
            :type formatter: Any
            :param args: positional arguments forwarded to the wrapped callable
            :type args: Any
            :param kwargs: keyword arguments forwarded to the wrapped callable
            :type kwargs: Any

            :return: The value returned by the wrapped callable.
            :rtype: Any
            """
            return fn(*args, **kwargs)
        return f
    @staticmethod
    def cleandoc(txt, formatter=None):
        """
        **LLM Docstring**

        Normalize indentation and surrounding whitespace in documentation text.

        :param txt: the text to normalize
        :type txt: Any
        :param formatter: the active template formatter
        :type formatter: Any

        :return: The cleaned documentation text.
        :rtype: Any
        """
        return inspect.cleandoc(txt)
    @staticmethod
    def wrap_str(obj, formatter=None):
        """
        **LLM Docstring**

        Convert an object to an escaped string literal, using triple quotes for multiline text.

        :param obj: the object to inspect or dispatch
        :type obj: Any
        :param formatter: the active template formatter
        :type formatter: Any

        :return: An escaped single-line or triple-quoted string representation.
        :rtype: Any
        """
        txt = str(obj)
        txt = txt.replace('"', '\\"').replace("'", "\\'")
        if '\n' in txt:
            txt = '"""'+txt+'"""'
        return txt
    @staticmethod
    def optional(key, default="", formatter=None):
        """
        **LLM Docstring**

        Retrieve an optional formatting parameter with a fallback value.

        :param key: the lookup, assignment, or formatting key
        :type key: Any
        :param default: fallback callable or value used when no match is found
        :type default: Any
        :param formatter: the active template formatter
        :type formatter: Any

        :return: The current parameter value for `key`, or `default` when it is absent.
        :rtype: Any
        """
        return formatter.format_parameters.get(key, default)

class FormatDirective(enum.Enum):
    """
    Base class for directives -- shouldn't be an enum really...
    """
    def __init__(self, name, callback=None):
        """
        **LLM Docstring**

        Initialize an enum directive with its template key and normalized callback.

        :param name: an explicit display name
        :type name: Any
        :param callback: the function receiving each generated comprehension result
        :type callback: Any

        :return: `None`.
        :rtype: None
        """
        self.key = name
        if isinstance(callback, str):
            callback = callback.format
        elif isinstance(callback, (staticmethod, classmethod, property)):
            callback = callback.__get__(self)
        self.callback = callback if not isinstance(callback, str) else callback.format
    def _call(self, *data, **kwargs):
        """
        **LLM Docstring**

        Invoke the callback associated with this directive.

        :param data: the value or collection being tested
        :type data: Any
        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Any

        :return: The callback result for this directive.
        :rtype: Any
        """
        return self.callback(*data, **kwargs)
    @classmethod
    def _keymap(cls):
        """
        **LLM Docstring**

        Return the lazily initialized directive-key cache for the enumeration.

        :return: The cached directive-key mapping, or `None` before initialization.
        :rtype: Any
        """
        if not hasattr(cls, '_keymap_dict'):
            cls._keymap_dict = None
        return cls._keymap_dict
    @classmethod
    def _load(cls, name:str):
        """
        **LLM Docstring**

        Resolve a directive member by its external template key.

        :param name: an explicit display name
        :type name: str

        :return: The directive member registered under `name`.
        :rtype: Any
        """
        k = cls._keymap()
        if k is None:
            cls._keymap_dict = {c.key:c for c in cls}
            k = cls._keymap_dict
        return k[name]
    @classmethod
    def extend(cls, *others):
        """
        **LLM Docstring**

        Create a new directive enumeration containing members from this class and additional enumerations.

        :param others: additional directive enumerations to merge
        :type others: Any

        :return: A new `FormatDirective` enumeration containing the merged members.
        :rtype: Any
        """
        vals = {
            o.name:o.value
            for c in (cls,) + others
            for o in c
        }
        return FormatDirective(cls.__name__, vals)

class TemplateFormatDirective(FormatDirective):
    Loop = "loop", TemplateOps.loop
    LoopTemplate = "loop_template", TemplateOps.loop_template
    Join = "join", TemplateOps.join
    Load = "load", TemplateOps.load
    Include = "include", TemplateOps.include
    Apply = "apply", TemplateOps.apply
    NonEmpty = "nonempty", TemplateOps.nonempty
    CleanDoc = "cleandoc", TemplateOps.cleandoc
    Optional = "optional", TemplateOps.optional

    Str = "str", TemplateOps.wrap_str
    Int = "int", TemplateOps.wrap(int)
    Float = "float", TemplateOps.wrap(float)
    Round = "round", TemplateOps.wrap(round)
    Len = "len", TemplateOps.wrap(len)
    Dict = "dict", TemplateOps.wrap(dict)
    List = "list", TemplateOps.wrap(list)
    Tuple = "tuple", TemplateOps.wrap(tuple)
    Set = "set", TemplateOps.wrap(set)

class TemplateFormatterError(ValueError):
    ...
class TemplateASTEvaluator:
    def __init__(self, formatter, directives, format_parameters:dict):
        """
        **LLM Docstring**

        Store the formatter, directive set, and mutable variable mapping used for AST evaluation.

        :param formatter: the active template formatter
        :type formatter: Any
        :param directives: the directive enumeration available to expressions
        :type directives: Any
        :param format_parameters: the mutable mapping of template variables
        :type format_parameters: dict

        :return: `None`.
        :rtype: None
        """
        self.formatter = formatter
        self.directives = directives
        self.format_parameters = format_parameters
    def handle_comprehension(self, g, expr, callback):
        """
        **LLM Docstring**

        Evaluate one comprehension generator while temporarily binding its target variable.

        :param g: the comprehension generator node
        :type g: Any
        :param expr: the expression evaluated for each accepted item
        :type expr: Any
        :param callback: the function receiving each generated comprehension result
        :type callback: Any

        :return: `None`; accepted values are delivered through `callback`.
        :rtype: Any
        """
        target = g.target.id
        restore = False
        if target in self.format_parameters:
            restore = True
            old = self.format_parameters[target]
        try:
            itt = self.evaluate_node(g.iter)
            for v in itt:
                self.format_parameters[target] = v
                if all(self.evaluate_node(e) for e in g.ifs):
                    callback(self.evaluate_node(expr))
        finally:
            if restore:
                self.format_parameters[target] = old
            else:
                if target in self.format_parameters:
                    del self.format_parameters[target]
    def evaluate_node(self, node:typing.Union[ast.AST,ast.expr,tuple]):
        """
        **LLM Docstring**

        Recursively interpret the supported subset of Python AST nodes used by template expressions.

        :param node: the AST node or node tuple to evaluate
        :type node: typing.Union[ast.AST, ast.expr, tuple]

        :return: The Python value produced by interpreting the supported AST node.
        :rtype: Any
        """
        if isinstance(node, tuple):
            return tuple(self.evaluate_node(n) for n in node)
        elif isinstance(node, ast.Module):
            bits = []
            for e in node.body:
                res = self.evaluate_node(e)
                if res is None:
                    res = ""
                bits.append(str(res))
            return "".join(bits)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            name = node.id
            try:
                val = self.format_parameters[name]
            except KeyError:
                need_raise = False
                try:
                    val = getattr(builtins, name)
                except AttributeError:
                    need_raise = True
                if need_raise:
                    raise
            return val
        elif isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Load):
            return getattr(self.evaluate_node(node.value), node.attr)
        elif isinstance(node, ast.Assign):
            if len(node.targets) > 1:
                raise TemplateFormatterError("Template assignments are restricted to single reassignments")
            if not isinstance(node.targets[0], ast.Name):
                raise TemplateFormatterError("Template assignments are restricted to variable names")
            self.format_parameters[node.targets[0].id] = self.evaluate_node(node.value)
        elif isinstance(node, ast.Expr):
            return self.evaluate_node(node.value)
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.List):
            return [self.evaluate_node(e) for e in node.elts]
        elif isinstance(node, ast.ListComp):
            l = []
            for g in node.generators:
                if isinstance(g, ast.comprehension):
                    self.handle_comprehension(
                        g,
                        node.elt,
                        l.append
                    )
            return l
        elif isinstance(node, ast.Tuple):
            return tuple(self.evaluate_node(e) for e in node.elts)
        elif isinstance(node, ast.Set):
            return {self.evaluate_node(e) for e in node.elts}
        elif isinstance(node, ast.SetComp):
            l = set
            for g in node.generators:
                if isinstance(g, ast.comprehension):
                    self.handle_comprehension(
                        g,
                        node.elt,
                        l.add
                    )
            return l
        elif isinstance(node, ast.Dict):
            return {self.evaluate_node(k):self.evaluate_node(v) for k,v in zip(node.keys, node.values)}
        elif isinstance(node, ast.DictComp):
            l = {}
            add = lambda kv:l.__setitem__(*kv)
            for g in node.generators:
                if isinstance(g, ast.comprehension):
                    self.handle_comprehension(
                        g,
                        (node.key, node.value),
                        add
                    )
            return l

        elif isinstance(node, ast.UnaryOp):
            val = self.evaluate_node(node.operand)
            if isinstance(node.op, ast.Not):
                return not val
            else:
                raise TemplateFormatterError("unsupported operation {}".format(ast.dump(node.op)))
        elif isinstance(node, ast.BinOp):
            left = self.evaluate_node(node.left)
            right = self.evaluate_node(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            elif isinstance(node.op, ast.Sub):
                return left - right
            elif isinstance(node.op, ast.Mult):
                return left * right
            elif isinstance(node.op, ast.Div):
                return left / right
            elif isinstance(node.op, ast.FloorDiv):
                return left // right
            elif isinstance(node.op, ast.MatMult):
                return left @ right
            elif isinstance(node.op, ast.And):
                return left and right
            elif isinstance(node.op, ast.Or):
                return left or right
            elif isinstance(node.op, ast.BitOr):
                return left | right
            elif isinstance(node.op, ast.BitAnd):
                return left & right
            elif isinstance(node.op, ast.Pow):
                return left ** right
            else:
                raise TemplateFormatterError("unsupported operation {}".format(ast.dump(node.op)))
        elif isinstance(node, ast.BoolOp):
            if isinstance(node.op, ast.Or):
                return self.evaluate_node(node.values[0]) or self.evaluate_node(node.values[1])
            elif isinstance(node.op, ast.And):
                return self.evaluate_node(node.values[0]) and self.evaluate_node(node.values[1])
            else:
                raise TemplateFormatterError("unsupported operation {}".format(ast.dump(node.op)))
        elif isinstance(node, ast.Compare):
            left = self.evaluate_node(node.left)
            op = node.ops[0]
            right = self.evaluate_node(node.comparators[0])
            if isinstance(op, ast.Eq):
                return left == right
            elif isinstance(op, ast.NotEq):
                return left != right
            elif isinstance(op, ast.Lt):
                return left < right
            elif isinstance(op, ast.Gt):
                return left > right
            elif isinstance(op, ast.LtE):
                return left <= right
            elif isinstance(op, ast.GtE):
                return left >= right
            elif isinstance(op, ast.In):
                return left in right
            elif isinstance(op, ast.NotIn):
                return left not in right
            elif isinstance(op, ast.Is):
                return left is right
            elif isinstance(op, ast.IsNot):
                return left is not right
            else:
                raise TemplateFormatterError("unsupported comparison {}".format(ast.dump(op)))
        elif isinstance(node, ast.IfExp):
            if self.evaluate_node(node.test):
                return self.evaluate_node(node.body)
            else:
                return self.evaluate_node(node.orelse)
        elif isinstance(node, ast.Subscript):
            return self.evaluate_node(node.value).__getitem__(self.evaluate_node(node.slice))
        elif isinstance(node, ast.Index):
            return self.evaluate_node(node.value)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute): # subattr of some object...I guess we can call it?
                directive = self.evaluate_node(node.func)
            directive = None
            if isinstance(node.func, ast.Name):
                name = node.func.id
                if name == 'raw':
                    return TemplateOps.wrap_str(node.args[0])
                elif name == 'assign':
                    self.format_parameters[self.evaluate_node(node.args[0])] = self.evaluate_node(node.args[1])
                    return ""
                try:
                    directive = self.directives._load(name)
                except KeyError:
                    need_raise = name in {'open'}
                    if not need_raise:
                        try:
                            directive = getattr(builtins, name)
                        except AttributeError:
                            need_raise = True
                    if need_raise:
                        raise
                else:
                    directive = lambda *a, _d=directive, **k: _d._call(*a, formatter=self.formatter, **k)
            if directive is None:
                directive = self.evaluate_node(node.func)
            args = [self.evaluate_node(a) for a in node.args]
            kwargs = {k.arg: self.evaluate_node(k.value) for k in node.keywords}
            return directive(*args, **kwargs)
        else:
            raise TemplateFormatterError("Node {} unsupported".format(ast.dump(node)))
class TemplateFormatter(string.Formatter):
    """
    Provides a formatter for fields that allows for
    the inclusion of standard Bootstrap HTML elements
    alongside the classic formatting
    """
    max_recusion=6
    directives = TemplateFormatDirective
    class frozendict(dict):
        def __setitem__(self, key, value):
            """
            **LLM Docstring**

            Reject mutation attempts on the template mapping.

            :param key: the lookup, assignment, or formatting key
            :type key: Any
            :param value: the value associated with the key
            :type value: Any

            :return: `None`.
            :rtype: None
            """
            raise TypeError("`frozendict` is immutable")
    def __init__(self, templates):
        """
        **LLM Docstring**

        Store an immutable template mapping and initialize the stack of active formatting scopes.

        :param templates: the mapping of template identifiers to resources
        :type templates: Any

        :return: `None`.
        :rtype: None
        """
        self.__templates = self.frozendict(templates)
        self._fmt_stack = []
    @property
    def format_parameters(self):
        """
        **LLM Docstring**

        Return the parameter mapping for the innermost active formatting operation.

        :return: The innermost parameter mapping, or `None` outside formatting.
        :rtype: dict | None
        """
        return self._fmt_stack[-1] if len(self._fmt_stack) > 0 else None
    @property
    def templates(self):
        """
        **LLM Docstring**

        Expose the immutable template-resource mapping.

        :return: The immutable template mapping.
        :rtype: Mapping
        """
        return self.__templates
    @property
    def special_callbacks(self):
        """
        **LLM Docstring**

        Map special format-field markers to evaluation, directive, comment, raw, and assignment handlers.

        :return: A mapping from special field markers to their handler methods.
        :rtype: dict
        """
        return {"%":self.apply_eval_tree, "$":self.apply_directive_tree, "#":self.apply_comment, 'raw$':self.apply_raw, 'assign%':self.apply_assignment}
    @property
    def callback_map(self):
        """
        **LLM Docstring**

        Combine special markers with every registered directive marker.

        :return: The complete mapping from special and directive markers to handlers.
        :rtype: dict
        """
        return dict(
            self.special_callbacks,
            **{d.key+"$":self.apply_directive for d in self.directives}
        )

    def apply_eval_tree(self, _, spec) -> str:
        """
        **LLM Docstring**

        Parse and evaluate a cleaned Python expression or statement block against the active parameters.

        :param _: an unused callback key
        :type _: Any
        :param spec: the object specification or template expression
        :type spec: Any

        :return: The evaluated expression result, with `None` converted to an empty string.
        :rtype: str
        """
        tree = ast.parse(inspect.cleandoc(spec))
        ev = TemplateASTEvaluator(self, self.directives, self.format_parameters).evaluate_node(tree)
        if ev is None:
            ev = ""
        return ev
    def apply_directive_tree(self, _, spec) -> str:
        """
        **LLM Docstring**

        Evaluate a directive expression after wrapping it in parentheses.

        :param _: an unused callback key
        :type _: Any
        :param spec: the object specification or template expression
        :type spec: Any

        :return: The evaluated directive-expression result.
        :rtype: str
        """
        return self.apply_eval_tree(_, "("+spec+")")
    def apply_assignment(self, key, spec) -> str:
        """
        **LLM Docstring**

        Assign the literal right-hand text from an inline assignment into the active parameter mapping.

        :param key: the lookup, assignment, or formatting key
        :type key: Any
        :param spec: the object specification or template expression
        :type spec: Any

        :return: An empty string after updating the active parameter mapping.
        :rtype: str
        """
        key, val = spec.split("=", 1)
        self.format_parameters[key] = val
        return ""
    def apply_raw(self, key, spec) -> str:
        """
        **LLM Docstring**

        Return a format specification unchanged.

        :param key: the lookup, assignment, or formatting key
        :type key: Any
        :param spec: the object specification or template expression
        :type spec: Any

        :return: The unmodified format specification.
        :rtype: str
        """
        return spec
    def apply_comment(self, key, spec) -> str:
        """
        **LLM Docstring**

        Discard a template comment field.

        :param key: the lookup, assignment, or formatting key
        :type key: Any
        :param spec: the object specification or template expression
        :type spec: Any

        :return: An empty string, removing the comment from output.
        :rtype: str
        """
        return ""
    def apply_directive(self, key, spec) -> str:
        """
        **LLM Docstring**

        Convert a directive marker and argument text into an evaluable directive call.

        :param key: the lookup, assignment, or formatting key
        :type key: Any
        :param spec: the object specification or template expression
        :type spec: Any

        :return: The evaluated result of the named directive call.
        :rtype: str
        """
        return self.apply_directive_tree(
            key,
            "{}({})".format(key.strip("$"), spec)
        )
    def format_field(self, value: Any, format_spec: str) -> str:
        """
        **LLM Docstring**

        Route special string-valued fields through callback handlers and otherwise use standard formatting.

        :param value: the value associated with the key
        :type value: Any
        :param format_spec: the format specification associated with the field
        :type format_spec: str

        :return: The special-callback result or the standard formatted field text.
        :rtype: str
        """
        if self.format_parameters is None:
            raise NotImplementedError("{}.{} called outside of `vformat`".format(
                type(self).__name__,
                'format_field'
            ))
        callback = (
            self.callback_map.get(value, None)
            if isinstance(value, str)
            else None
        )
        if callback is None:
            return super().format_field(value, format_spec)
        else:
            return callback(value, format_spec)

    _template_cache = {}
    def load_template(self, template):
        """
        **LLM Docstring**

        Resolve a registered template and read file-backed content with caching.

        :param template: the template name, template text, or template callable
        :type template: Any

        :return: The registered template text, read from disk when the resource is a file path.
        :rtype: Any
        """
        if template not in self.__templates:
            raise ValueError("can't load templates on the fly ({} not in {})".format(
                template, self.__templates
            ))
        template = self.templates[template]
        if os.path.exists(template):
            if template not in self._template_cache:
                with open(template) as file:
                    template = file.read()
                self._template_cache[template] = template
            else:
                template = self._template_cache[template]
        return template

        # if value in s
        #     ...
        # else:
        #     super()
        # directive, args = self.parse_spec(format_spec)
        # self.directives(directive).apply(
        #     value, *args
        # )

    def vformat(self, format_string: str, args: Sequence[Any], kwargs: Mapping[str, Any]):
        """
        **LLM Docstring**

        Render a template within a temporary parameter scope populated with special callback markers.

        :param format_string: the template string being formatted
        :type format_string: str
        :param args: positional arguments forwarded to the wrapped callable
        :type args: Sequence[Any]
        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Mapping[str, Any]

        :return: The fully rendered template string.
        :rtype: Any
        """
        try:
            self._fmt_stack.append(kwargs.copy())
            for k in self.special_callbacks:
                kwargs[k] = k
            for d in self.directives:
                if d.key+"$" not in kwargs:
                    kwargs[d.key+"$"] = d.key+"$"
            used_args = set()
            result, _ = self._vformat(format_string, args, kwargs, used_args, self.max_recusion)
            self.check_unused_args(used_args, args, kwargs)
            return result
        finally:
            self._fmt_stack.pop()

class OrderedSet(dict):
    def __init__(self, *iterable):
        """
        **LLM Docstring**

        Initialize insertion-ordered unique keys from an optional iterable.

        :param iterable: the iterable used to initialize the ordered set
        :type iterable: Any

        :return: `None`.
        :rtype: None
        """
        if len(iterable) > 0:
            iterable = iterable[0]
        super().__init__({k:None for k in iterable})
    def union(self, other:'OrderedSet'):
        """
        **LLM Docstring**

        Return a new ordered set containing this set followed by unseen keys from another set.

        :param other: another ordered set
        :type other: 'OrderedSet'

        :return: A new ordered set containing keys from both operands without duplicates.
        :rtype: Any
        """
        return type(self)(itertools.chain(self.keys(), other.keys()))
    def __repr__(self):
        """
        **LLM Docstring**

        Return a constructor-style representation containing the ordered keys.

        :return: A constructor-style string showing the ordered keys.
        :rtype: Any
        """
        return "{}({})".format(type(self).__name__, list(self.keys()))
    def __iter__(self):
        """
        **LLM Docstring**

        Iterate over keys in insertion order.

        :return: An iterator over keys in insertion order.
        :rtype: Any
        """
        return iter(self.keys())
    def add(self, k):
        """
        **LLM Docstring**

        Add a key while preserving insertion order and uniqueness.

        :param k: a dispatch key or parameter name
        :type k: Any

        :return: `None`.
        :rtype: None
        """
        self[k] = None
    def update(self, ks):
        """
        **LLM Docstring**

        Add every key from an iterable.

        :param ks: keys to add
        :type ks: Any

        :return: `None`.
        :rtype: None
        """
        super().update({k:None for k in ks})
    def __delitem__(self, k):
        """
        **LLM Docstring**

        Delete a key from the ordered set.

        :param k: a dispatch key or parameter name
        :type k: Any

        :return: `None`.
        :rtype: None
        """
        del self[k]
class Locator(typing.Protocol):
    def locate(self, identifier):
        """
        **LLM Docstring**

        Define the protocol operation that resolves a resource identifier.

        :param identifier: the resource or Python object identifier
        :type identifier: Any

        :return: The resolved resource for `identifier`.
        :rtype: Any
        """
        ...
    def paths(self, **opts)->"Iterable":
        """
        **LLM Docstring**

        Define the protocol operation that enumerates available resource identifiers.

        :param opts: additional protocol-specific path enumeration options
        :type opts: Any

        :return: An iterable of available resource identifiers.
        :rtype: 'Iterable'
        """
        ...
class ResourcePathLocator(Locator):
    def __init__(self, path:Iterable[str]):
        """
        **LLM Docstring**

        Normalize one or more filesystem search roots into a list.

        :param path: one or more resource search roots
        :type path: Iterable[str]

        :return: `None`.
        :rtype: None
        """
        if isinstance(path, str):
            path = [path]
        self.path = list(path)
    def locate(self, identifier):
        """
        **LLM Docstring**

        Resolve an existing absolute or relative identifier, searching configured roots in order.

        :param identifier: the resource or Python object identifier
        :type identifier: Any

        :return: The first existing path matching `identifier`, or `None` when no resource exists.
        :rtype: Any
        """
        if os.path.exists(identifier):
            return os.path.abspath(identifier)
        else:
            for d in self.path:
                f = self.resource_path(d, identifier)
                if os.path.exists(f):
                    return f
    def resource_path(self, d, f):
        """
        **LLM Docstring**

        Join a search root with a resource-relative path.

        :param d: a resource root directory
        :type d: Any
        :param f: a resource-relative file name
        :type f: Any

        :return: The filesystem path formed from the root and relative resource name.
        :rtype: Any
        """
        return os.path.join(d, f)
    def paths(self, max_depth=7, **_):
        """
        **LLM Docstring**

        Walk search roots and collect resource-relative file paths up to a maximum depth.

        :param max_depth: the maximum traversal depth, with negative values meaning unlimited
        :type max_depth: Any
        :param _: an unused callback key
        :type _: Any

        :return: An ordered set of resource-relative file paths.
        :rtype: Iterable[str]
        """
        s = OrderedSet()
        for d in self.path:
            base = self.resource_path(d, "")
            base_depth = len(pathlib.Path(base).parts)
            for root, dirs, files in os.walk(base, topdown=True):
                br = pathlib.Path(root).parts[base_depth:]
                if len(br) > max_depth:
                    break
                s.update(os.path.join(*br, f) for f in files)
        return s
    def directories(self):
        """
        **LLM Docstring**

        Return the concrete root directories searched by this locator.

        :return: The concrete directories searched by this locator.
        :rtype: Iterable[str]
        """
        return [self.resource_path(d, "") for d in self.path]
    def __repr__(self):
        """
        **LLM Docstring**

        Return a constructor-style representation of the configured search paths.

        :return: A constructor-style string containing the configured roots.
        :rtype: Any
        """
        return "{}({})".format(
            type(self).__name__,
            self.path
        )
class SubresourcePathLocator(ResourcePathLocator):
    def __init__(self, roots, extension):
        """
        **LLM Docstring**

        Initialize a path locator that inserts a fixed subresource directory below each root.

        :param roots: the base search roots
        :type roots: Any
        :param extension: the subdirectory extension appended below each root
        :type extension: Any

        :return: `None`.
        :rtype: None
        """
        self.ext = extension
        super().__init__(roots)
    def resource_path(self, d, f):
        """
        **LLM Docstring**

        Join a root, fixed subresource directory, and resource-relative path.

        :param d: a resource root directory
        :type d: Any
        :param f: a resource-relative file name
        :type f: Any

        :return: The path formed from the root, fixed subresource directory, and resource name.
        :rtype: Any
        """
        return os.path.join(d, self.ext, f)
    def __repr__(self):
        """
        **LLM Docstring**

        Return a constructor-style representation of roots and subresource extension.

        :return: A constructor-style string containing roots and the subresource extension.
        :rtype: Any
        """
        return "{}({}, {})".format(
            type(self).__name__,
            self.path,
            self.ext
        )
class ResourceLocator(Locator):
    def __init__(self,
                 locators:Iterable[Union[ResourcePathLocator,Iterable[str], Tuple[Iterable[str], Union[str, Iterable[str]]]]]
                 ):
        """
        **LLM Docstring**

        Normalize heterogeneous locator specifications into a flat sequence of path locators.

        :param locators: resource locator definitions to combine
        :type locators: Iterable[Union[ResourcePathLocator, Iterable[str], Tuple[Iterable[str], Union[str, Iterable[str]]]]]

        :return: `None`.
        :rtype: None
        """
        if isinstance(locators, str):
            locators = [locators]
        self.locators = []
        for s in locators:
            if isinstance(s, ResourcePathLocator):
                s = [s]
            elif isinstance(s[0], str):
                s = [ResourcePathLocator(s)]
            elif isinstance(s[1], str):
                s = [SubresourcePathLocator(*s)]
            else:
                s = [SubresourcePathLocator(s[0], e) for e in s[1]]
            self.locators.extend(s)
    def locate(self, identifier):
        """
        **LLM Docstring**

        Return the first resource path resolved by the configured locators.

        :param identifier: the resource or Python object identifier
        :type identifier: Any

        :return: The first resource resolved by any component locator, or `None`.
        :rtype: Any
        """
        for l in self.locators:
            res = l.locate(identifier)
            if res is not None:
                return res
    def paths(self, filter_pattern=None, **_):
        """
        **LLM Docstring**

        Combine resource paths from all locators and optionally filter them by regex or glob.

        :param filter_pattern: a regular expression or glob used to filter resource paths
        :type filter_pattern: Any
        :param _: an unused callback key
        :type _: Any

        :return: The combined resource identifiers, optionally filtered by the supplied pattern.
        :rtype: Iterable[str]
        """
        paths = {r for l in self.locators for r in l.paths()}
        if filter_pattern is not None:
            if isinstance(filter_pattern, str):
                try:
                    filter_pattern = re.compile(filter_pattern)
                except (re.error, ValueError):
                    filter_pattern = re.compile(fnmatch.translate(filter_pattern))
            paths = OrderedSet(p for p in paths if filter_pattern.match(p))
        return paths
    def directories(self):
        """
        **LLM Docstring**

        Return unique search directories from all component locators in encounter order.

        :return: The unique component search directories in encounter order.
        :rtype: Iterable[str]
        """
        return OrderedSet(r for l in self.locators for r in l.directories())
    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation based on the combined search directories.

        :return: A constructor-style string containing the combined directories.
        :rtype: Any
        """
        return "{}({})".format(
            type(self).__name__,
            self.directories()
        )

class TemplateEngine:
    """
    Provides an engine for generating content using a
    `TemplateFormatter` and `ResourceLocator`
    """

    formatter_class = TemplateFormatter
    def __init__(self,
                 locator:Locator,
                 template_pattern="*.*",
                 ignore_missing=False,
                 formatter_class=None,
                 ignore_paths=()
                 ):
        """
        **LLM Docstring**

        Discover matching template resources, construct the formatter, and store output-control options.

        :param locator: the resource locator supplying templates
        :type locator: Locator
        :param template_pattern: the pattern selecting template resources
        :type template_pattern: Any
        :param ignore_missing: whether missing format fields should resolve through a default mapping
        :type ignore_missing: Any
        :param formatter_class: the formatter implementation to instantiate
        :type formatter_class: Any
        :param ignore_paths: target paths that should not be written
        :type ignore_paths: Any

        :return: `None`.
        :rtype: None
        """
        self.locator = locator
        self.templates = {
            k:self.locator.locate(k)
            for k in self.locator.paths(filter_pattern=template_pattern)
        }
        if formatter_class is None:
            formatter_class = self.formatter_class
        self.formatter = formatter_class(self.templates)
        self.ignore_missing = ignore_missing
        self.ignore_paths = ignore_paths
    def __repr__(self):
        """
        **LLM Docstring**

        Return an elided representation containing the locator.

        :return: An elided constructor-style string identifying the locator.
        :rtype: Any
        """
        cls = type(self)
        return dev.str_elide(f"{cls.__name__}({self.locator})", width=50)


    def format_map(self, template, parameters):
        """
        **LLM Docstring**

        Resolve a template identifier when registered and render it with a parameter mapping.

        :param template: the template name, template text, or template callable
        :type template: Any
        :param parameters: the values exposed while formatting
        :type parameters: Any

        :return: The rendered template text.
        :rtype: Any
        """
        if template in self.templates:
            template = self.formatter.load_template(template)
        return self.formatter.vformat(
            template,
            (),
            parameters if not self.ignore_missing else collections.defaultdict(parameters)
        )
    def format(self, template, **parameters):
        """
        **LLM Docstring**

        Render a template using keyword parameters.

        :param template: the template name, template text, or template callable
        :type template: Any
        :param parameters: the values exposed while formatting
        :type parameters: Any

        :return: The rendered template text.
        :rtype: Any
        """
        return self.format_map(template, parameters)

    class outStream:
        def __init__(self, file, mode='w+', **kw):
            """
            **LLM Docstring**

            Store a destination and deferred file-opening options for the output context.

            :param file: a path or writable stream
            :type file: Any
            :param mode: the mode used when opening a path
            :type mode: Any
            :param kw: additional arguments passed to `open`
            :type kw: Any

            :return: `None`.
            :rtype: None
            """
            self.file = file
            self.file_handle = None
            self.mode = mode
            self.kw = kw

        def __enter__(self):
            """
            **LLM Docstring**

            Open a path on first entry, creating its parent directory when possible, or reuse a supplied stream.

            :return: The opened file handle or supplied writable stream.
            :rtype: Any
            """
            if self.file_handle is None:
                if isinstance(self.file, str):
                    try:
                        os.makedirs(os.path.dirname(self.file))
                    except OSError:
                        pass
                    self.file_handle = open(self.file, self.mode, **self.kw)
                else:
                    self.file_handle = self.file
            return self.file_handle

        def __exit__(self, exc_type, exc_val, exc_tb):
            """
            **LLM Docstring**

            Close path-backed output and clear the cached handle.

            :param exc_type: the exception class raised inside the context, if any
            :type exc_type: Any
            :param exc_val: the exception instance raised inside the context, if any
            :type exc_val: Any
            :param exc_tb: the traceback associated with the exception, if any
            :type exc_tb: Any

            :return: `None`.
            :rtype: None
            """
            if isinstance(self.file, str):
                self.file_handle.close()
            self.file_handle = None

        def write(self, s):
            """
            **LLM Docstring**

            Open the output context, write one string, and return the original destination.

            :param s: the string written to the output stream
            :type s: Any

            :return: The original destination path or stream after writing.
            :rtype: Any
            """
            with self as out:
                out.write(s)
            return self.file
    def write_string(self, target, txt):
        """
        **LLM Docstring**

        Write rendered text to a target through `outStream`.

        :param target: the destination path, stream, or key
        :type target: Any
        :param txt: the text to normalize
        :type txt: Any

        :return: The destination returned by `outStream.write`.
        :rtype: Any
        """
        return self.outStream(target).write(txt)
    def apply(self, template, target, **template_params):
        """
        **LLM Docstring**

        Render a template and either return the string or write it unless the target is ignored.

        :param template: the template name, template text, or template callable
        :type template: Any
        :param target: the destination path, stream, or key
        :type target: Any
        :param template_params: values supplied to the template
        :type template_params: Any

        :return: The rendered text when `target` is `None`, the written target otherwise, or `None` for ignored paths.
        :rtype: Any
        """
        try:
            if target is None:
                return self.format_map(template, template_params)
            elif target not in self.ignore_paths:
                return self.write_string(target, self.format_map(template, template_params))
        except:
            raise ValueError("{}: error in filling template {}".format(
                type(self).__name__,
                template
            ))

class TemplateHandler(ObjectHandler):
    template = None
    extension = ".md"
    squash_repeat_packages=True
    def __init__(self,
                 obj,
                 *,
                 out=None,
                 engine:TemplateEngine=None,
                 root=None,
                 squash_repeat_packages=True,
                 is_package_root=False,
                 **extra_fields
                 ):
        """
        **LLM Docstring**

        Initialize object-handling state, resolve the output target, and choose an object-specific or default template.

        :param obj: the object to inspect or dispatch
        :type obj: Any
        :param out: the output root, file, or stream
        :type out: Any
        :param engine: the template engine used to render content
        :type engine: TemplateEngine
        :param root: the output root used to compute relative URLs
        :type root: Any
        :param squash_repeat_packages: whether repeated package components are collapsed
        :type squash_repeat_packages: Any
        :param is_package_root: whether the documented object represents a package root
        :type is_package_root: Any
        :param extra_fields: additional fields exposed to handlers and templates
        :type extra_fields: Any

        :return: `None`.
        :rtype: None
        """
        super().__init__(obj, **extra_fields)
        self.is_package_root = is_package_root
        self.squash_repeat_packages = squash_repeat_packages
        self.target = self.get_output_file(out)
        # if root is None:
        #     root = os.path.dirname(self.target)
        if root is None and out is not None and os.path.isdir(out):
            root = out
        self.root = root
        if engine is None:
            raise ValueError("{}:`engine` can't be None".format(type(self).__name__))
        self.engine = engine

        test_path = os.path.join(*self.identifier.split(".")) + ".md"
        if self.engine.locator.locate(test_path) is not None:
            self.template = test_path
        if self.template is None:
            raise ValueError("{}: template can't be None".format(type(self).__name__))

    def template_params(self, **kwargs):
        """
        **LLM Docstring**

        Merge handler extra fields with parameters computed for the current object.

        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Any

        :return: The merged mapping of extra fields and object-specific template parameters.
        :rtype: Any
        """
        base_parms = self.extra_fields.copy()
        base_parms.update(self.get_template_params(**kwargs))
        return base_parms
    @abc.abstractmethod
    def get_template_params(self, **kwargs):
        """
        Returns the parameters that should be inserted into the template

        :return:
        :rtype: dict
        """
        raise NotImplementedError("abstract base class")

    @property
    def package_path(self):
        """
        **LLM Docstring**

        Return the package name and source URL tuple for the handled object.

        :return: A `(package_name, source_url)` tuple.
        :rtype: Any
        """
        return self.get_package_and_url()
    def get_package_and_url(self, include_url_base=True):
        """
        Returns package name and corresponding URL for the object
        being documented
        :return:
        :rtype:
        """
        ident = self.identifier
        if self.squash_repeat_packages:
            ident = self.squash_reps(ident)
        pkg_split = ident.split(".", 1)

        if len(pkg_split) == 1:
            pkg = pkg_split[0]
            rest = ""
        elif len(pkg_split) == 0:
            pkg = ""
            rest = "Not.A.Real.Package"
        else:
            pkg, rest = pkg_split

        # if self.squash_repeat_packages:
        #     base_id = rest.split(".")
        #     new_id = [base_id[0]]
        #     for i,k in enumerate(base_id[1:]):
        #         if new_id[-1] != k:
        #             new_id.extend(base_id[1+i:])
        #             break
        #     rest = ".".join(new_id)

        # if len(rest) == 0:
        #     file_url = "__init__.py"
        # else:
        file_url = ident.replace(".", "/")
        if self.is_package_root:
            file_url += "/__init__.py"
        else:
            file_url += '.py'

        if include_url_base and 'url_base' in self.extra_fields:
            file_url = self.extra_fields['url_base'] + "/" + file_url
        return pkg, file_url

    @property
    def target_identifier(self):
        """
        **LLM Docstring**

        Return the normalized dotted identifier used for the output target.

        :return: The normalized dotted target identifier.
        :rtype: Any
        """
        return ".".join(self.get_target_extension())
    @classmethod
    def squash_reps(cls, ident):
        """
        **LLM Docstring**

        Collapse the leading repeated package components in a dotted identifier.

        :param ident: the dotted identifier to normalize
        :type ident: Any

        :return: The dotted identifier with leading repeated package components removed.
        :rtype: Any
        """
        ident = ident.split('.')
        up = ident[0]
        i = -1
        for i,r in enumerate(ident[1:]):
            if r != up:
                i = i - 1
                break
        return '.'.join(ident[i+1:])
    def get_target_extension(self, identifier=None):
        """
        **LLM Docstring**

        Split an object identifier into normalized path components for output and resource lookup.

        :param identifier: the resource or Python object identifier
        :type identifier: Any

        :return: The normalized identifier components used as a resource or output path.
        :rtype: Any
        """
        if identifier is None:
            identifier = self.identifier
        elif not isinstance(identifier, str):
            identifier = self.get_identifier(identifier)
        base_id = identifier.split(".")
        if self.squash_repeat_packages:
            new_id = [base_id[0]]
            for i, k in enumerate(base_id[1:]):
                if new_id[-1] != k:
                    new_id.extend(base_id[1 + i:])
                    break
            base_id = new_id
        return base_id
    def get_output_file(self, out):
        """
        Returns package name and corresponding URL for the object
        being documented
        :return:
        :rtype:
        """
        if out is None:
            out = sys.stdout
        elif isinstance(out, str):# and os.path.isdir(out):
            base_id = self.identifier.split(".")
            if self.squash_repeat_packages:
                new_id = [base_id[0]]
                for i, k in enumerate(base_id[1:]):
                    if new_id[-1] != k:
                        new_id.extend(base_id[1 + i:])
                        break
                base_id = new_id
            out = os.path.join(out, *base_id) + self.extension
        return out
    def handle(self, template=None, target=None, write=True):
        """
        Formats the documentation Markdown from the supplied template

        :param template:
        :type template:
        :return:
        :rtype:
        """
        if self.check_should_write():
            if template is None:
                template = self.template
            params = self.template_params()
            if target is None:
                out_file = self.target
            else:
                out_file = target
            if isinstance(out_file, str):
                pkg, file_url = self.package_path
                params['package_name'] = pkg
                params['file_url'] = file_url
                params['package_url'] = os.path.dirname(file_url)

                if self.root is not None:
                    root = self.root
                    root_split = pathlib.Path(root).parts
                    out_split = pathlib.Path(out_file).parts
                    root_depth = len(root_split)
                    out_url = "/".join(out_split[root_depth:])
                else:
                    file_split = pathlib.Path(file_url).parts
                    out_split = pathlib.Path(out_file).parts
                    out_url = "/".join(out_split[-len(file_split):])
                params['file'] = out_file
                params['url'] = out_url
            try:
                out = self.engine.apply(template, out_file if write else None, _self=self, **params)
            except KeyError as e:
                raise ValueError("{} ({}): template needs key {}".format(
                    type(self).__name__,
                    self.obj,
                    e.args[0]
                ))
            except IndexError as e:
                raise ValueError("{} ({}): template index {} out of range...".format(
                    type(self).__name__,
                    self.obj,
                    e.args[0]
                ))
            except Exception as e:
                raise ValueError("{} ({}): {}".format(
                    type(self).__name__,
                    self.obj,
                    self.template,
                    e
                ))
            return out
        else:
            if not write:
                return ""

    blacklist_packages = {
        'numpy', 'scipy', 'matplotlib',
        # chemistry
        "ase", "rdkit", "numba",  "mpi4py", "h5py", "pysisyphus", "sympy",
        # jupyter
        "plotly", "IPython", "ipykernel", "ipywidgets", "ipyevents",
        "cycler", "traitlets", "nglview",
        "nbformat", "nbformat", "markdown",
        # misc,
        "orjson",
        # top 100 packages on PyPI
        'aiobotocore', 'aiohappyeyeballs', 'aiohttp',
        'aiosignal', 'annotated_doc', 'annotated_types', 'anyio',
        'attr', 'attrs', 'boto3', 'botocore',
        'bs4', 'certifi', 'cffi', 'charset_normalizer',
        'click', 'colorama', 'cryptography', 'dateutil',
        'dotenv', 'fastapi', 'filelock', 'frozenlist',
        'fsspec', 'google', 'greenlet', 'grpc',
        'grpc_status', 'h11', 'hatchling', 'httpcore',
        'httpx', 'huggingface_hub', 'idna', 'importlib_metadata',
        'iniconfig', 'jinja2', 'jmespath', 'jsonschema',
        'jsonschema_specifications', 'jwt', 'litellm', 'markdown_it',
        'markupsafe', 'mdurl', 'multidict',
        'opentelemetry', 'packaging', 'pandas',
        'pathspec', 'PIL', 'pip', 'platformdirs', 'pluggy',
        'propcache', 'pyarrow', 'pyasn1', 'pyasn1_modules',
        'pycparser', 'pydantic', 'pydantic_core', 'pygments',
        'pyparsing', 'pytest', 'pytz', 'referencing',
        'requests', 'rich', 'rpds', 's3fs',
        's3transfer', 'scikit-image', 'scikit-image', 'setuptools',
        'sglang', 'shellingham', 'six', 'sniffio',
        'sqlalchemy', 'starlette', 'tenacity', 'tqdm',
        'trove_classifiers', 'typer', 'typing_extensions', 'typing_inspection',
        'tzdata', 'urllib3', 'uvicorn', 'virtualenv',
        'websockets', 'wheel', 'wrapt', 'yaml',
        'yarl', 'zipp'
    } #TODO: more sophisticated blacklisting
    def check_should_write(self):
        """
        Determines whether the object really actually should be
        documented (quite permissive)
        :return:
        :rtype:
        """
        base = self.identifier.split(".", 1)[0]
        stdlib = base == 'builtins'
        if not stdlib:
            if hasattr(sys, "stdlib_module_names"):
                stdlib = base in sys.stdlib_module_names
        return not stdlib and base not in self.blacklist_packages

class TemplateResourceExtractor(ResourceLocator):
    extension = '.md'
    def path_extension(self, handler:TemplateHandler):
        """
        Provides the default examples path for the object
        :return:
        :rtype:
        """
        return os.path.join(*handler.get_target_extension()) + self.extension
    resource_keys = []
    resource_attrs = []
    def get_resource(self, handler:TemplateHandler, keys=None, attrs=None):
        """
        **LLM Docstring**

        Locate a resource using configured handler fields, object attributes, or the default derived path.

        :param handler: the handler whose resource should be located
        :type handler: TemplateHandler
        :param keys: handler fields checked for an explicit resource
        :type keys: Any
        :param attrs: object attributes checked for an explicit resource
        :type attrs: Any

        :return: The resolved resource identifier or path, or `None` when none can be found.
        :rtype: Any
        """
        if keys is None:
            keys = self.resource_keys
        if attrs is None:
            attrs = self.resource_attrs
        for k in keys:
            res = handler[k]
            if res is not None:
                res_file = self.locate(res)
                if res_file is not None:
                    res = res
                break
        else:
            for a in attrs:
                res = getattr(handler.obj, a, None)
                if res is not None:
                    res_file = self.locate(res)
                    if res_file is not None:
                        res = res
                    break
            else:
                ext = self.path_extension(handler)
                if isinstance(ext, str):
                    res = self.locate(ext)
                else:
                    for e in ext:
                        res = self.locate(e)
                        if res is not None:
                            break
                    else:
                        res = None
        return res
    def load(self, handler:TemplateHandler):
        """
        Loads examples for the stored object if provided
        :return:
        :rtype:
        """

        resource = self.get_resource(handler)
        if resource is not None and os.path.isfile(resource):
            with open(resource) as f:
                resource = f.read()
        return resource

class ModuleTemplateHandler(TemplateHandler):
    template = 'module.md'
class ClassTemplateHandler(TemplateHandler):
    template = 'class.md'
class FunctionTemplateHandler(TemplateHandler):
    template = 'function.md'
class MethodTemplateHandler(TemplateHandler):
    template = 'method.md'
class ObjectTemplateHandler(TemplateHandler):
    template = 'object.md'
class IndexTemplateHandler(TemplateHandler):
    template = 'index.md'

class TemplateWalker(ObjectWalker):
    module_handler = ModuleTemplateHandler
    class_handler = ClassTemplateHandler
    function_handler = FunctionTemplateHandler
    method_handler = MethodTemplateHandler
    object_handler = ObjectTemplateHandler
    index_handler = IndexTemplateHandler
    def __init__(self, engine:TemplateEngine, out=None, description=None, **extra_fields):
        """
        **LLM Docstring**

        Store template-engine output settings and initialize the underlying object walker.

        :param engine: the template engine used to render content
        :type engine: TemplateEngine
        :param out: the output root, file, or stream
        :type out: Any
        :param description: the description passed to the generated index
        :type description: Any
        :param extra_fields: additional fields exposed to handlers and templates
        :type extra_fields: Any

        :return: `None`.
        :rtype: None
        """
        self.engine = engine
        self.out_dir = out
        self.description = description
        super().__init__(**extra_fields)

    @property
    def default_handlers(self):
        """
        **LLM Docstring**

        Build the ordered mapping from modules, classes, functions, and fallback objects to handler classes.

        :return: The ordered mapping from dispatch tests to handler classes.
        :rtype: Any
        """
        return collections.OrderedDict((
            ((str, types.ModuleType), self.module_handler),
            ((type,), self.class_handler),
            ((types.FunctionType,), self.function_handler),
            (None, self.object_handler)
        ))

    def get_handler(self, obj, *, out=None, engine=None, tree=None, **kwargs):
        """
        **LLM Docstring**

        Construct a handler while injecting this walker’s output directory and template engine.

        :param obj: the object to inspect or dispatch
        :type obj: Any
        :param out: the output root, file, or stream
        :type out: Any
        :param engine: the template engine used to render content
        :type engine: Any
        :param tree: the shared object-documentation tree
        :type tree: Any
        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Any

        :return: The handler constructed with this walker’s engine and output settings.
        :rtype: Any
        """
        return super().get_handler(
            obj,
            out=self.out_dir,
            engine=self.engine,
            tree=tree,
            **kwargs
        )

    def visit_root(self, o, **kwargs): # here for overloading
        """
        **LLM Docstring**

        Visit a root object through the standard traversal implementation.

        :param o: the object or import path to resolve
        :type o: Any
        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Any

        :return: The result returned by visiting the root object.
        :rtype: Any
        """
        return self.visit(o, **kwargs)

    def write(self, objects, max_depth=-1, index='index.md'):
        """
        Walks through the objects supplied and applies the appropriate templates
        :return: index of written files
        :rtype: str
        """

        if self.out_dir is not None and index is not None:
            try:
                os.makedirs(self.out_dir)
            except OSError:
                pass
            out_file = os.path.join(self.out_dir, index)
        else:
            out_file = None

        files = [
            self.visit_root(o, max_depth=max_depth)
            for o in objects
        ]
        files = [f for f in files if f is not None]
        w = self.get_handler(files,
                             cls=self.index_handler,
                             out=out_file,
                             engine=self.engine,
                             root=self.out_dir,
                             extra_fields=self.extra_fields,
                             description=self.description
                             )
        return w.handle()

class TemplateResourceList(Locator):
    """
    Implements the `ResourceLocator` interface, but is backed by a `dict` of
    explicit resources rather than a set of paths.
    """
    def __init__(self, resource_dict:Mapping[str, Any]):
        """
        **LLM Docstring**

        Store an explicit identifier-to-resource mapping.

        :param resource_dict: the explicit resource mapping
        :type resource_dict: Mapping[str, Any]

        :return: `None`.
        :rtype: None
        """
        self.dict = resource_dict
    def paths(self, **_):
        """
        **LLM Docstring**

        Return the identifiers available in the explicit resource mapping.

        :param _: an unused callback key
        :type _: Any

        :return: A dynamic view of the stored resource identifiers.
        :rtype: Iterable[str]
        """
        return self.dict.keys()
    def locate(self, identifier):
        """
        **LLM Docstring**

        Retrieve the resource associated with an identifier, returning `None` when absent.

        :param identifier: the resource or Python object identifier
        :type identifier: Any

        :return: The resource mapped to `identifier`, or `None` when absent.
        :rtype: Any
        """
        return self.dict.get(identifier, None)
class TemplateInterfaceList(TemplateResourceList):
    """
    A set of functions to be used to construct interfaces
    """
    def __init__(self, resource_dict:Mapping[str, Callable]):
        """
        **LLM Docstring**

        Initialize an explicit mapping of interface names to template callables.

        :param resource_dict: the explicit resource mapping
        :type resource_dict: Mapping[str, Callable]

        :return: `None`.
        :rtype: None
        """
        super().__init__(resource_dict)
class TemplateInterfaceFormatter:
    """
    Provides an interface that mimics a `TemplateFormatter`
    but does nothing more than route to a set of template functions
    """
    def __init__(self, templates):
        """
        **LLM Docstring**

        Store callable templates and initialize the active parameter-scope stack.

        :param templates: the mapping of template identifiers to resources
        :type templates: Any

        :return: `None`.
        :rtype: None
        """
        self.__templates = templates
        self._fmt_stack = []
    @property
    def format_parameters(self):
        """
        **LLM Docstring**

        Return the innermost active interface parameter mapping.

        :return: The active interface parameter mapping, or `None` outside invocation.
        :rtype: dict | None
        """
        return self._fmt_stack[-1] if len(self._fmt_stack) > 0 else None
    @property
    def templates(self):
        """
        **LLM Docstring**

        Expose the callable-template mapping.

        :return: The stored mapping of interface template callables.
        :rtype: Mapping
        """
        return self.__templates
    @property
    def special_callbacks(self):
        """
        **LLM Docstring**

        Return the currently empty special-callback mapping for interface templates.

        :return: An empty mapping; interface templates do not define special field callbacks.
        :rtype: dict
        """
        return {
            # "%":self.apply_eval_tree,
            # "$":self.apply_directive_tree,
            # "#":self.apply_comment,
            # 'raw$':self.apply_raw,
            # 'assign%':self.apply_assignment
        }
    # @property
    # def callback_map(self):
    #     return dict(
    #         self.special_callbacks,
    #         **{d.key+"$":self.apply_directive for d in self.directives}
    #     )
    #
    # def apply_eval_tree(self, _, spec) -> str:
    #     tree = ast.parse(inspect.cleandoc(spec))
    #     ev = TemplateASTEvaluator(self, self.directives, self.format_parameters).evaluate_node(tree)
    #     if ev is None:
    #         ev = ""
    #     return ev
    # def apply_directive_tree(self, _, spec) -> str:
    #     return self.apply_eval_tree(_, "("+spec+")")
    # def apply_assignment(self, key, spec) -> str:
    #     key, val = spec.split("=", 1)
    #     self.format_parameters[key] = val
    #     return ""
    # def apply_raw(self, key, spec) -> str:
    #     return spec
    # def apply_comment(self, key, spec) -> str:
    #     return ""
    # def apply_directive(self, key, spec) -> str:
    #     return self.apply_directive_tree(
    #         key,
    #         "{}({})".format(key.strip("$"), spec)
    #     )
    # def format_field(self, value: Any, format_spec: str) -> str:
    #     if self.format_parameters is None:
    #         raise NotImplementedError("{}.{} called outside of `vformat`".format(
    #             type(self).__name__,
    #             'format_field'
    #         ))
    #     callback = (
    #         self.callback_map.get(value, None)
    #         if isinstance(value, str)
    #         else None
    #     )
    #     if callback is None:
    #         return super().format_field(value, format_spec)
    #     else:
    #         return callback(value, format_spec)

    # _template_cache = {}
    def load_template(self, template):
        """
        **LLM Docstring**

        Retrieve a callable template by identifier.

        :param template: the template name, template text, or template callable
        :type template: Any

        :return: The callable registered under the template identifier.
        :rtype: Any
        """
        return self.templates[template]

        # if value in s
        #     ...
        # else:
        #     super()
        # directive, args = self.parse_spec(format_spec)
        # self.directives(directive).apply(
        #     value, *args
        # )

    def vformat(self, template: Callable, args: Sequence[Any], kwargs: Mapping[str, Any]):
        """
        **LLM Docstring**

        Invoke a callable template inside a temporary formatting-parameter scope.

        :param template: the template name, template text, or template callable
        :type template: Callable
        :param args: positional arguments forwarded to the wrapped callable
        :type args: Sequence[Any]
        :param kwargs: keyword arguments forwarded to the wrapped callable
        :type kwargs: Mapping[str, Any]

        :return: The value returned by invoking the callable template.
        :rtype: Any
        """
        try:
            self._fmt_stack.append(kwargs.copy())
            for k in self.special_callbacks:
                kwargs[k] = k
            return template(*args, **kwargs)
            # for d in self.directives:
            #     if d.key+"$" not in kwargs:
            #         kwargs[d.key+"$"] = d.key+"$"
            # used_args = set()
            # result, _ = self._vformat(format_string, args, kwargs, used_args, self.max_recusion)
            # self.check_unused_args(used_args, args, kwargs)
            # return result
        finally:
            self._fmt_stack.pop()

class TemplateInterfaceEngine(TemplateEngine):
    """
    A variant on a template engine designed for more interactive use.
    In many ways, _not_ a template engine, but too useful to ignore while I
    find a more uniform abstraction.
    Generates _interfaces_ from a set of interface template functions
    rather than strings from template files.
    """

    formatter_class = TemplateInterfaceFormatter
    def __init__(self,
                 templates: 'TemplateInterfaceList|dict',
                 ignore_missing=False,
                 formatter_class=None,
                 ignore_paths=()
                 ):
        """
        **LLM Docstring**

        Normalize a dictionary of callables into an interface resource list and initialize the base engine.

        :param templates: the mapping of template identifiers to resources
        :type templates: 'TemplateInterfaceList|dict'
        :param ignore_missing: whether missing format fields should resolve through a default mapping
        :type ignore_missing: Any
        :param formatter_class: the formatter implementation to instantiate
        :type formatter_class: Any
        :param ignore_paths: target paths that should not be written
        :type ignore_paths: Any

        :return: `None`.
        :rtype: None
        """
        if isinstance(templates, dict):
            templates = TemplateInterfaceList(templates)
        super().__init__(
            templates,
            template_pattern=None,
            ignore_missing=ignore_missing,
            formatter_class=formatter_class,
            ignore_paths=ignore_paths
        )

    def format_map(self, template, parameters):
        """
        **LLM Docstring**

        Resolve and invoke a callable template with the supplied parameter mapping.

        :param template: the template name, template text, or template callable
        :type template: Any
        :param parameters: the values exposed while formatting
        :type parameters: Any

        :return: The value returned by the resolved interface template.
        :rtype: Any
        """
        if template in self.templates:
            template = self.formatter.load_template(template)
        return self.formatter.vformat(
            template,
            (),
            parameters if not self.ignore_missing else collections.defaultdict(parameters)
        )

    def apply(self, template, target, **template_params):
        """
        **LLM Docstring**

        Return an interface result directly or map it to a non-ignored target key.

        :param template: the template name, template text, or template callable
        :type template: Any
        :param target: the destination path, stream, or key
        :type target: Any
        :param template_params: values supplied to the template
        :type template_params: Any

        :return: The direct interface value, a `{target: value}` mapping, or `None` for ignored targets.
        :rtype: Any
        """
        try:
            if target is None or target is sys.stdout:
                return self.format_map(template, template_params)
            elif target not in self.ignore_paths:
                return {target:self.format_map(template, template_params)}
        except:
            raise ValueError("{}: error in filling template {}".format(
                type(self).__name__,
                template
            ))
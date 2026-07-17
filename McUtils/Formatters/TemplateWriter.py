import os, shutil
from string import Formatter
from .FileMatcher import *

__all__ = [
    "TemplateWriter",
    "OptionalTemplate"
]

class TemplateWriter:
    """
    A general class that can take a directory layout and apply template parameters to it
    Very unsophisticated but workable. For a more sophisticated take that walks through
    object trees, see `TemplateEngine`.
    """

    ignored_files = [".DS_Store"]

    def __init__(self, template_dir, replacements = None, file_filter = None, **opts):
        """
        **LLM Docstring**

        Initialize `TemplateWriter` state from the supplied configuration.

        :param template_dir: template-root directory used to compute relative output paths
        :type template_dir: object
        :param replacements: value consumed as `replacements` by the documented formatting path
        :type replacements: object
        :param file_filter: value consumed as `file_filter` by the documented formatting path
        :type file_filter: object
        :param opts: additional keyword options forwarded to the underlying formatter or operation
        :type opts: dict
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        if replacements is not None:
            opts = replacements
        self._rep_dict = opts
        self._reps = None

        if file_filter is None:
            file_filter = FileMatcher(MatchList(*self.ignored_files, negative_match=True), use_basename=True)
        self.filter = FileMatcher(file_filter) if not isinstance(file_filter, StringMatcher) else file_filter
        self.template_dir = os.path.abspath(template_dir)

    @property
    def replacements(self):
        """
        **LLM Docstring**

        Lazily compile replacement keys into backtick-delimited string substitution pairs.
        :return: compiled `(placeholder, replacement)` pairs
        :rtype: tuple[tuple[str, str], ...]
        """
        if self._reps is None:
            self._reps =  tuple(("`"+k+"`", str(v)) for k,v in self._rep_dict.items())
        return self._reps

    def apply_replacements(self, string):
        """Applies the defined replacements to the

        :param string:
        :type string:
        :return:
        :rtype:
        """
        import functools

        return functools.reduce(lambda s, r: s.replace(*r), self.replacements, string)

    def write_file(self, template_file, out_dir, apply_template = True, template_dir = None):
        """writes a single _file_ to _dir_ and fills the template from the parameters passed when intializing the class

        :param template_file: the file to load and write into
        :type template_file: str
        :param out_dir: the directory to write the file into
        :type out_dir: str
        :param apply_template: whether to apply the template parameters to the file content or not
        :type apply_template: bool
        :return:
        :rtype:
        """

        if template_dir is None:
            template_dir = self.template_dir

        stripped_loc = template_file.split(template_dir, 1)[-1]
        rep_loc = self.apply_replacements(stripped_loc).strip(os.sep)
        new_file = os.path.join(out_dir, rep_loc)

        os.makedirs(os.path.dirname(new_file), exist_ok = True)

        if apply_template:
            with open(template_file) as tf:
                try:
                    content = tf.read()
                except:
                    raise IOError("Couldn't read content from {}".format(template_file))
                with open(new_file, "w+") as out:
                    out.write(self.apply_replacements(content))
        else:
            shutil.copy(template_file, new_file)

        return new_file

    def iterate_write(self, out_dir, apply_template = True, src_dir = None, template_dir = None):
        """Iterates through the files in the template_dir and writes them out to dir

        :return:
        :rtype:
        """

        if template_dir is None:
            template_dir = self.template_dir
        if src_dir is None:
            src_dir = template_dir

        files = os.listdir(src_dir)
        for f in files:
            f = os.path.join(src_dir, f)
            if self.filter.matches(f.split(template_dir, 1)[-1]):
                if not os.path.isdir(f):
                    self.write_file(f, out_dir, apply_template = apply_template, template_dir = template_dir)
                else:
                    self.iterate_write(out_dir, apply_template = apply_template, src_dir = f, template_dir = template_dir)


class OptionalTemplate:
    def __init__(self, template, **opts):
        """
        **LLM Docstring**

        Initialize `OptionalTemplate` state from the supplied configuration.

        :param template: template text or template-file path
        :type template: object
        :param opts: additional keyword options forwarded to the underlying formatter or operation
        :type opts: dict
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        self.opts = opts
        if os.path.isfile(template):
            with open(template) as t:
                template = t.read()
        self.template = template

    class DefaultFormatter(Formatter):
        default_key = "-MISSING-"

        def get_value(self, key, args, kwds):
            """
            **LLM Docstring**

            Resolve and return the requested derived value from the object’s current configuration.

            :param key: field name requested by `string.Formatter`
            :type key: object
            :param args: command arguments enclosed in braces
            :type args: object
            :param kwds: keyword formatting arguments
            :type kwds: object
            :return: resolved field value or the missing-value sentinel
            :rtype: object
            """
            if isinstance(key, str):
                try:
                    return kwds[key]
                except KeyError:
                    return self.default_key
            else:
                return Formatter.get_value(key, args, kwds)

    @classmethod
    def apply_template(cls, template, opts, formatter=None, strip_missing_blocks=None, strip_missing=True):
        """
        **LLM Docstring**

        Format optional placeholders with a sentinel for missing keys, then remove missing values or entire missing lines as configured.

        :param template: template text or template-file path
        :type template: object
        :param opts: replacement values or formatter options
        :type opts: object
        :param formatter: `string.Formatter`-compatible formatter
        :type formatter: object
        :param strip_missing_blocks: whether lines containing unresolved placeholders are removed
        :type strip_missing_blocks: object
        :param strip_missing: whether unresolved placeholder sentinels are removed
        :type strip_missing: object
        :return: formatted template text
        :rtype: str
        """
        if formatter is None:
            formatter = cls.DefaultFormatter()
        applied_template = formatter.format(template, **opts)
        if strip_missing_blocks is None: strip_missing_blocks = strip_missing
        if strip_missing_blocks:
            applied_template = applied_template.replace(formatter.default_key + "\n", "")
        if strip_missing:
            applied_template = applied_template.replace(formatter.default_key, "")
        return applied_template

    def apply(self, **opts):
        """
        **LLM Docstring**

        Merge instance defaults with call-time options and apply them to the stored optional template.

        :param opts: additional keyword options forwarded to the underlying formatter or operation
        :type opts: dict
        :return: formatted template text
        :rtype: str
        """
        return self.apply_template(self.template, dict(self.opts, **opts))
import os, shutil
from .DocWalker import DocWalker
from ..Formatters.TemplateEngine import ResourceLocator
__all__ = ['DocBuilder']

class DocBuilder:
    """
    A documentation builder class that uses a `DocWalker`
    to build documentation, but which also has support for more
    involved use cases, like setting up a `_config.yml` or other
    documentation template things.


    :related: .DocWalker.DocWalker, .DocWalker.ModuleWriter, .DocWalker.ClassWriter,
              .DocWalker.FunctionWriter, .DocWalker.MethodWriter, .DocWalker.ObjectWriter, .DocWalker.IndexWriter
    """
    defaults_root = os.path.dirname(__file__)
    default_config_file = '_config.yml'

    def __init__(self, packages=None, config=None, target=None, root=None, config_file=None, templates_directory=None, examples_directory=None, tests_directory=None, readme=None):
        """
        :param packages: list of package configs to write
        :type packages: Iterable[str|dict]
        :param config: parameters for _config.yml file
        :type config: dict
        :param target: target directory to which files should be written
        :type target: str
        :param root: root directory
        :type root: str
        :param root: root directory
        :type root: str
        """
        ...
    default_template_extension = 'templates'
    default_repo_extension = 'repo_templates'

    def get_template_locator(self, template_directory, use_repo_templates=False):
        """
        **LLM Docstring**

        Builds the resource search path used to locate documentation templates.

        Bundled paths are rooted beside this module. When repository templates are enabled, `repo_templates` is searched before `templates`.

        :param template_directory: an optional custom template directory or existing locator
        :type template_directory: None | str | Iterable[str] | ResourceLocator

        :param use_repo_templates: whether repository-specific templates should be searched before the defaults
        :type use_repo_templates: bool
        :return: an existing locator unchanged, or a locator combining custom and bundled template directories
        :rtype: ResourceLocator
        """
        ...
    config_defaults = {'theme': 'McCoyGroup/finx', 'gh_username': 'McCoyGroup-bot', 'footer': ''}

    def load_config(self):
        """
        Loads the config file to be used and fills in template parameters

        :return:
        :rtype:
        """
        ...

    def create_layout(self):
        """
        Creates the documentation layout that will be expanded upon by
        a `DocWalker`

        :return:
        :rtype:
        """
        ...

    def load_walker(self):
        """
        Loads the `DocWalker` used to write docs.
        A hook that can be overriden to sub in different walkers.

        :return:
        :rtype:
        """
        ...

    def build(self):
        """
        Writes documentation layout to `self.target`

        :return:
        :rtype:
        """
        ...
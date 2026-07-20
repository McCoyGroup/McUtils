from .NodeCommServer import ShellCommHandler
__all__ = ['GitClient']

class GitClient(ShellCommHandler):
    DEFAULT_CONNECTION = None
    DEFAULT_PORT_ENV_VAR = 'GIT_SOCKET_PORT'

    def get_methods(self) -> 'dict[str,method]':
        ...

    def do_git(self, args, kwargs):
        ...
from .NodeCommServer import ShellCommHandler
__all__ = ['SLURMClient']

class SLURMClient(ShellCommHandler):
    DEFAULT_CONNECTION = None
    DEFAULT_PORT_ENV_VAR = 'SLURM_SOCKET_PORT'

    def get_methods(self) -> 'dict[str,method]':
        ...

    def do_sbatch(self, args, kwargs):
        ...
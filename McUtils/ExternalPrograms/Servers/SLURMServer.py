from .NodeCommServer import ShellCommHandler

__all__ = [
    "SLURMClient"
]

class SLURMClient(ShellCommHandler):

    DEFAULT_CONNECTION = None
    DEFAULT_PORT_ENV_VAR = 'SLURM_SOCKET_PORT'
    # DEFAULT_CONNECTION = os.path.expanduser("~/.gitsocket")
    def get_methods(self) -> 'dict[str,method]':
        return {
            'sbatch':self.do_sbatch
        }
    def do_sbatch(self, args, kwargs):
        # turn kwargs into sbatch flags and place them before the script/args
        cli = self.kwargs_to_cli(kwargs)
        return self.subprocess_response("sbatch", [*cli, *args])
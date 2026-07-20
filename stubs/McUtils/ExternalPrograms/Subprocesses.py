import sys
import os
import shlex
import subprocess
__all__ = ['env_proc_call', 'env_pip']

def env_proc_call(*args, executable=None, text=True, env=None, shell=False, **subprocess_run_kwargs):
    """
    **LLM Docstring**

    Run a command with an environment-specific executable directory prepended to `PATH`; string commands are shell-split, and non-shell mode currently prefixes non-PATH assignments as literal argv entries.

    :param executable: Python or environment executable whose directory is added to `PATH`
    :type executable: object

    :param text: whether subprocess streams use text mode
    :type text: object

    :param env: environment mapping passed to the child process
    :type env: object

    :param shell: whether `subprocess.run` uses a shell
    :type shell: object

    :param args: positional command or function arguments
    :type args: object

    :param subprocess_run_kwargs: remaining options forwarded to `subprocess.run`
    :type subprocess_run_kwargs: object

    :return: run a command with an environment-specific executable directory prepended to `PATH`; string commands are shell-split, and non-shell mode currently prefixes non-PATH assignments as literal argv entries.
    :rtype: subprocess.CompletedProcess
    """
    ...

def env_pip(*args):
    """
    **LLM Docstring**

    Invoke `env_proc_call` with `pip` as the command.

    :param args: positional command or function arguments
    :type args: object

    :return: invoke `env_proc_call` with `pip` as the command.
    :rtype: subprocess.CompletedProcess
    """
    ...
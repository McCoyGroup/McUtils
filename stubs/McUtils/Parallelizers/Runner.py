import typing
from .Parallelizers import Parallelizer
__all__ = ['ClientServerRunner']

class ClientServerRunner:
    """
    Provides a framework for running MPI-like scripts in a client/server
    model
    """

    def __init__(self, client_runner: typing.Callable, server_runner: typing.Callable, parallelizer: Parallelizer):
        """
        **LLM Docstring**

        Store client and server callables together with the parallelizer used to choose between them.

        :param client_runner: Value supplied for `client_runner`.
        :type client_runner: typing.Callable
        :param server_runner: Value supplied for `server_runner`.
        :type server_runner: typing.Callable
        :param parallelizer: Value supplied for `parallelizer`.
        :type parallelizer: Parallelizer
        :return: None.
        :rtype: None
        """
        ...

    def run(self):
        """
        Runs the client/server processes depending on if the parallelizer
        is on the main or server processes

        :return:
        :rtype:
        """
        ...
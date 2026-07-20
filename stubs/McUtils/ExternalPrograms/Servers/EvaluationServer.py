import abc
import functools
import os
import numpy as np
import uuid
from .NodeCommServer import NodeCommHandler, NodeCommClient
__all__ = ['EvaluationHandler', 'EvaluationClient']

class EvaluationHandler(NodeCommHandler):

    @abc.abstractmethod
    def get_evaluators(self) -> 'dict[str,method]':
        ...

    def wrap_evaluator(self, name, evaluation_function):
        ...

    def get_methods(self) -> 'dict[str,method]':
        ...

class EvaluationClient(NodeCommClient):

    def call(self, evaluator: str, coords: np.ndarray, filename=None, **kwargs):
        ...
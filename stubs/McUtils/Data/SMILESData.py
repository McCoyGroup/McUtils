from .CommonData import DataHandler
import random
__all__ = ['SMILESData']
__reload_hook__ = ['.CommonData']

class SMILESDataHandler(DataHandler):

    def __init__(self):
        ...

    def functional_group(self, name, return_string=True):
        ...

    def scaffold(self, name, return_string=True):
        ...

    def random_scaffold(self, return_string=True):
        ...

    def random_functional_group(self, return_string=True):
        ...
SMILESData = SMILESDataHandler()
SMILESData.__doc__ = 'An instance of `SMILESDataHandler` that can be used for looking up data on pre-baked smiles strings'
SMILESData.__name__ = 'SMILESData'
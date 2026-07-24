from .CommonData import DataHandler
import random

__all__ = [ "SMILESData" ]
__reload_hook__ = [".CommonData"]

class SMILESDataHandler(DataHandler):
    def __init__(self):
        super().__init__("SMILESData", extension='.json')#:, record_type=ColorDataRecord)
    def functional_group(self, name, return_string=True):
        data = self["FunctionalGroups", name]
        if return_string:
            data = data['mapped_smiles']
        return data
    def scaffold(self, name, return_string=True):
        data = self["Scaffolds", name]
        if return_string:
            data = data['mapped_smiles']
        return data
    def random_scaffold(self, return_string=True):
        return self.scaffold(random.choice(list(self['Scaffolds'].keys())), return_string=return_string)
    def random_functional_group(self, return_string=True):
        return self.functional_group(random.choice(list(self['FunctionalGroups'].keys())), return_string=return_string)

SMILESData=SMILESDataHandler()
SMILESData.__doc__ = """An instance of `SMILESDataHandler` that can be used for looking up data on pre-baked smiles strings"""
SMILESData.__name__ = "SMILESData"
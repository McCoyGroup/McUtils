import numpy as np
from .CommonData import DataHandler, DataRecord

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

SMILESData=SMILESDataHandler()
SMILESData.__doc__ = """An instance of `SMILESDataHandler` that can be used for looking up data on pre-baked smiles strings"""
SMILESData.__name__ = "SMILESData"
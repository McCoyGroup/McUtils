from .CommonData import DataHandler, DataRecord
__all__ = ['PotentialData']
__reload_hook__ = ['.CommonData']

class PotentialDataHandler(DataHandler):

    def __init__(self):
        ...

    def __getitem__(self, item):
        """
        :param item:
        :type item: str
        :return:
        :rtype: PotentialDataRecord
        """
        ...

class PotentialDataRecord(DataRecord):
    """
    Represents a simple callable wavefunction...
    """

    def __init__(self, data_handler, key, records):
        ...

    def __call__(self, *args, **kwargs):
        ...

    def __repr__(self):
        ...
PotentialData = PotentialDataHandler()
PotentialData.__doc__ = 'An instance of PotentialDataHandler that can be used for looking up data on potentials'
PotentialData.__name__ = 'PotentialData'
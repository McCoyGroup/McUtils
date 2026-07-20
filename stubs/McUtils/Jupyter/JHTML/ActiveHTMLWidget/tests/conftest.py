import pytest
from ipykernel.comm import Comm
from ipywidgets import Widget

class MockComm(Comm):
    """A mock Comm object.

    Can be used to inspect calls to Comm's open/send/close methods.
    """
    comm_id = 'a-b-c-d'
    kernel = 'Truthy'

    def __init__(self, *args, **kwargs):
        ...

    def open(self, *args, **kwargs):
        ...

    def send(self, *args, **kwargs):
        ...

    def close(self, *args, **kwargs):
        ...
_widget_attrs = {}
undefined = object()

@pytest.fixture
def mock_comm():
    ...
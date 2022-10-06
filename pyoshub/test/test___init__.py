import pytest
import pyoshub.pyoshub as pyoshub 

osh_api = pyoshub.OSH_API()

_ = """
@pytest.mark.vcr()
def test___init__():
    global osh_api
    result = osh_api.__init__()
    """
import pytest
import pyosh 

osh_api = pyosh.OSH_API()

_ = """
@pytest.mark.vcr()
def test___init__():
    global osh_api
    result = osh_api.__init__()
    """
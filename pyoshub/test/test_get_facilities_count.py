import pytest
import pyoshub.pyoshub as pyoshub 

@pytest.fixture(scope='module')
def vcr_config():
    return {
        "filter_headers": [('authorization', 'HIDETOKEN')],
    }
    
osh_api = pyoshub.OSH_API()

@pytest.mark.vcr()
def test_get_facilities_count():
    global osh_api
    result = osh_api.get_facilities_count()
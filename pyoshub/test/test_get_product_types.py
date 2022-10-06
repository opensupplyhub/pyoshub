import pytest
import pyosh 

@pytest.fixture(scope='module')
def vcr_config():
    return {
        "filter_headers": [('authorization', 'HIDETOKEN')],
    }
    
osh_api = pyosh.OSH_API()

@pytest.mark.vcr()
def test_get_product_types():
    global osh_api
    result = osh_api.get_product_types()
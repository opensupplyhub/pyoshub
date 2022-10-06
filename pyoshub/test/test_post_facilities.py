import pytest
import pyosh 

@pytest.fixture(scope='module')
def vcr_config():
    return {
        "filter_headers": [('authorization', 'HIDETOKEN')],
    }
    
osh_api = pyosh.OSH_API()

@pytest.mark.vcr()
def test_post_facilities_match():
    global osh_api
    result = osh_api.post_facilities(
        name="Place A",
        country="DE",
        address="Nowhere, 12345 Somewhere"
    )

@pytest.mark.vcr()
def test_post_facilities_potential_match():
    global osh_api
    result = osh_api.post_facilities(
        name="Place B",
        country="DE",
        address="Nowhere, 12346 Somewhere"
    )

@pytest.mark.vcr()
def test_post_facilities_new():
    global osh_api
    result = osh_api.post_facilities(
        name="Place C",
        country="DE",
        address="Nowhere, 12347 Somewhere"
    )

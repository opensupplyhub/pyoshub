import pytest
import pyosh

@pytest.fixture(scope='module')
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [('authorization', 'DUMMY')],
    }

#@pytest.fixture(scope='module')
#def vcr_cassette_dir(request):
#    # Put all cassettes in vhs/{module}/{test}.yaml
#    #eturn os.path.join('vhs', request.module.__name__)
#    return("/tmp")

osh_api = pyosh.OSH_API()

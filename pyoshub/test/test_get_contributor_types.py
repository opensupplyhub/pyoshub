import pytest
import pyoshub.pyoshub as pyoshub 
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope='module')
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [
            ('authorization', 'HIDDEN')],
        "record_mode":'new'
    }


@pytest.mark.vcr()
class Test_get_contributor_types:
    def test_get_contributor_types(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_contributor_types()
        assert(len(result) == 8)
        assert('contributor_type' in result[0].keys())
        assert(result == [
                {'contributor_type': 'Academic / Researcher / Journalist / Student'},
                {'contributor_type': 'Auditor / Certification Scheme / Service Provider'},
                {'contributor_type': 'Brand / Retailer'},
                {'contributor_type': 'Civil Society Organization'},
                {'contributor_type': 'Facility / Factory / Manufacturing Group / Supplier / Vendor'},
                {'contributor_type': 'Multi-Stakeholder Initiative'},
                {'contributor_type': 'Union'},
                {'contributor_type': 'Other'}
            ]
        )
        assert(osh_api.ok)
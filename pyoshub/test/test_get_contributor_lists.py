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
class Test_get_contributor_lists:
    def test_get_contributor_lists_valid(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_contributor_lists(25)
        assert(result == [
            {'list_id': 1562, 'list_name': 'Levi Strauss & Co. Factory List Q1 2022'},
            {'list_id': 1563, 'list_name': 'Levi Strauss & Co. Mill List Q1 2022'}
        ])
        assert("list_id" in result[0].keys())
        assert("list_name" in result[0].keys())
        assert(osh_api.ok)



    def test_get_contributor_lists_invalid(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_contributor_lists(1234567890123)
        assert(result == [])
        assert(osh_api.ok)
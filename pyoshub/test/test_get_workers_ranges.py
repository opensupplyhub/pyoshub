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
class Test_get_workers_ranges:
    def test_get_workers_ranges(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_workers_ranges()
        assert(len(result) == 4)
        assert(result[0]["lower"] == 1)
        assert(result[-1]["upper"] > 1000000)
        lower = -1
        upper = -1
        for wr in result:
            assert(wr["lower"] > lower)
            assert(wr["upper"] > wr["lower"])
            lower = wr["lower"]
            upper = wr["upper"]
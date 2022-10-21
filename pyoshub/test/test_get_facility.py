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
class Test_get_facility:
    def test_get_facility_valid(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_facility("DE20211253G9MQX")
        assert(result == {
            'id': 'DE20211253G9MQX', 
            'lon': 13.40625, 
            'lat': 52.52341, 
            'name': 'Footwear studios', 
            'address': 'Stadtbahnbogen 135, 10178 Berlin, Germany', 
            'country_code': 'DE', 
            'os_id': 'DE20211253G9MQX', 
            'other_names': '', 
            'other_addresses': '', 
            'contributors': 'id:1319|name:Find Sourcing (Find Sourcing Facility List May 2021)|is_verified:False|contributor_name:Find Sourcing|list_name:Find Sourcing Facility List May 2021', 
            'country_name': 'Germany', 
            'claim_info': '', 
            'other_locations': '', 
            'is_closed': '', 
            'activity_reports': '', 
            'contributor_fields': '', 
            'has_inexact_coordinates': False, 
            'created_from': 'created_at:2021-05-05T13:58:25.354748Z|contributor:Find Sourcing', 
            'sector': "updated_at:2022-01-27T17:39:55.089265Z|contributor_id:1319|contributor_name:Find Sourcing|values:['Apparel']|is_from_claim:False"}
        )
        assert(osh_api.ok)
        assert(osh_api.status_code == 0)
        assert(osh_api.reason == "200")


    def test_get_facility_invalid(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_facility("inexistant")
        assert(result == {})
        assert(not osh_api.ok)
        assert(osh_api.status_code == -1)
        assert(osh_api.reason == "404")
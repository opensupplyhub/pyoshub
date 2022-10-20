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
class Test_get_facilities:
    def test_get_facilities_country_CH(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_facilities(countries="CH")
        assert(result[0] == {
            'os_id': 'CH2022234TE4H2S', 
            'lon': 9.1461813, 
            'lat': 46.2477371, 
            'name': 'AGEMEAT AND TRADING AG', 
            'address': 'Via Pascolet, 41 Grono', 
            'country_code': 'CH', 
            'country_name': 'Switzerland', 
            'has_approved_claim': False, 
            'is_closed': None
            }
        )
        assert(len(result)==82)


    def test_get_facilities_query_light(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_facilities(q="light")
        assert(result[12] == {
            'os_id': 'TR2020034N6R7S4', 
            'lon': 27.4868765, 
            'lat': 40.9585877, 
            'name': 'BLUE LIGHT TEKSTİL İNŞAAT TAŞIMACILIK SAN. VE TİC. LTD. ŞTİ.', 
            'address': 'NUSRATLI MAH. İSMET INONU BULV. 80 SULEYMANPASA / TEKİRDAG,59000,TEKIRDAG', 
            'country_code': 'TR', 
            'country_name': 'Turkey', 
            'has_approved_claim': False, 
            'is_closed': None
            }
        )
        assert(len(result)==264)


    def test_get_facilities_list_859(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_facilities(lists=859)
        assert(result[7] == {
            'os_id': 'PL2021057HKNX9C', 
            'lon': 19.3935024, 
            'lat': 51.8025525, 
            'name': 'Eko Niko', 
            'address': 'Lodz,Traktorowa148/158, Łódź', 
            'country_code': 'PL', 
            'country_name': 'Poland', 
            'has_approved_claim': False, 
            'is_closed': None
            }
        )
        assert(len(result)==30)


    def test_get_facilities_contributor_union(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_facilities(contributor_types="union")
        print(result)
        print(len(result))
        assert(result == [])
        assert(len(result)==0)

    def test_get_facilities_contributor_union(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_facilities(contributor_types="union,other")
        print(result)
        print(len(result))
        assert(result == [])
        assert(len(result)==0)
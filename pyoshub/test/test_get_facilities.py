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


    def test_get_facilities_contributor_types_union(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_facilities(contributor_types="union")
        #print(result)
        #print(len(result))
        assert(result == [])
        assert(len(result)==0)


    def test_get_facilities_contributor_types_union_other(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_facilities(contributor_types=["Union","Other"])
        assert(result[334] == {
            'os_id': 'BD2019248FM2409', 
            'lon': 90.4077333, 
            'lat': 24.0081001, 
            'name': 'BEA-CON Knitwear Ltd. (Factory-2)', 
            'address': 'BEA-CON Bhaban, Minister Bari Road, South Salna, Joydebpur, Gazipur-1703', 
            'country_code': 'BD', 
            'country_name': 'Bangladesh', 
            'has_approved_claim': False, 
            'is_closed': None
            }
        )
        assert(len(result)==3505)


    def test_get_facilities_contributor_127(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_facilities(contributors=127)
        #print(result[31])
        #print(len(result))
        #print(osh_api.api_call_count)
        assert(result[31] == {
            'os_id': 'PK2019143PF0KX4', 
            'lon': 74.4871193, 
            'lat': 32.4413553, 
            'name': 'Awan Sports Unit 5', 
            'address': '9km Daska Road   Adha Sialkot 51310 Punjab Pakistan', 
            'country_code': 'PK', 
            'country_name': 'Pakistan', 
            'has_approved_claim': False, 
            'is_closed': None}
        )
        assert(len(result)==589)
        assert(osh_api.api_call_count == 13)



    def test_get_facilities_contributor_127_and_2729_714(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_facilities(contributors=[127,"2729",714])
        #print(result[1157])
        #print(len(result))
        #print(osh_api.api_call_count)
        assert(result[1157] == {
            'os_id': 'TR20210067JTXST', 
            'lon': 32.683128, 
            'lat': 41.249306, 
            'name': 'SAFRANLAR DERI. TEKS. IMALAT VE PAZ. LTD. STI. (Previous name:SAFRAN MOD DERI SANAYI VE TICARET LIMITED SIRKETI )', 
            'address': 'Baris Mah. Kucuk Sanayi Sitesi, Mezbaha Sk. No: 2  Safranbolu, Karabuk', 
            'country_code': 'TR', 
            'country_name': 'Turkey', 
            'has_approved_claim': False, 
            'is_closed': None
            }
        )
        assert(len(result)==1592)
        assert(osh_api.api_call_count == 33)

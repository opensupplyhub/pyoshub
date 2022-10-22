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
class Test_post_facilities_match:
    def test_post_facilities_new(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.post_facilities(
            name="This is definitely a new facility",
            country="Colombia",
            address="Cl 29 No. 37-02 MARINILLA, Medellín",
            sector="Computers"
        )
        assert(result == [
            {
                'item_id': 804344, 
                'lon': -75.56581530000001, 
                'lat': 6.2476376, 
                'geocoded_address': 'Medellín, Medellin, Antioquia, Colombia', 
                'status': 'NEW_FACILITY', 
                'os_id': 'CO2022294AJ8TBG'
            }
        ])
        assert(osh_api.ok)
        assert(osh_api.reason=="201")

    def test_post_facilities_match(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.post_facilities(
            name="This is definitely a similar facility",
            country="Colombia",
            address="Cl 29 No. 37 MARINILLA, Medellín",
            sector="Computers"
        )
        assert(result == [
            {
                'match_no': 1, 
                'item_id': 804345, 
                'lon': -75.3378851, 
                'lat': 6.1731064, 
                'geocoded_address': 'Marinilla, Antioquia, Colombia', 
                'status': 'MATCHED', 
                'os_id': 'CO2022294AJ8TBG', 
                'match_id': 'CO2022294AJ8TBG', 
                'match_lon': -75.56581530000001, 
                'match_lat': 6.2476376, 
                'match_name': 'This is definitely a new facility', 
                'match_address': 
                'Cl 29 No. 37-02 MARINILLA, Medellín', 
                'match_country_code': 'CO', 
                'match_os_id': 'CO2022294AJ8TBG', 
                'match_other_names': 'This is definitely a similar facility', 
                'match_other_addresses': 'Cl 29 No. 37 MARINILLA, Medellín', 
                'match_contributors': 'id:2757|name:Klaus (Openapparel)|is_verified:False|contributor_name:Klaus (Openapparel)|list_name:None', 
                'match_country_name': 'Colombia', 'match_claim_info': '', 
                'match_other_locations': 'lat:6.1731064|lon:-75.3378851|contributor_id:2757|contributor_name:Klaus (Openapparel)|notes:None', 
                'match_is_closed': '', 
                'match_activity_reports': '', 
                'match_contributor_fields': '', 
                'match_new_os_id': '', 
                'match_has_inexact_coordinates': False, 
                'match_ef_name': 'value:This is definitely a new facility|field_name:name|contributor_id:2757|contributor_name:Klaus (Openapparel)|updated_at:2022-10-21T15:21:20.781209Z\nvalue:This is definitely a similar facility|field_name:name|contributor_id:2757|contributor_name:Klaus (Openapparel)|updated_at:2022-10-21T15:24:42.639399Z', 
                'match_ef_address': 'value:Cl 29 No. 37-02 MARINILLA, Medellín|field_name:address|contributor_id:2757|contributor_name:Klaus (Openapparel)|updated_at:2022-10-21T15:21:20.781209Z|is_from_claim:False\nvalue:Cl 29 No. 37 MARINILLA, Medellín|field_name:address|contributor_id:2757|contributor_name:Klaus (Openapparel)|updated_at:2022-10-21T15:24:42.639399Z|is_from_claim:False', 
                'match_ef_number_of_workers': '', 
                'match_ef_native_language_name': '', 
                'match_ef_facility_type': '', 
                'match_ef_processing_type': '', 
                'match_ef_product_type': "id:152004|is_verified:False|value:{'raw_values': ['Computers']}|updated_at:2022-10-21T15:24:42.758565Z|contributor_name:Klaus (Openapparel)|contributor_id:2757|value_count:2|is_from_claim:False|field_name:product_type|verified_count:0\nid:152003|is_verified:False|value:{'raw_values': ['Computers']}|updated_at:2022-10-21T15:21:20.896425Z|contributor_name:Klaus (Openapparel)|contributor_id:2757|value_count:2|is_from_claim:False|field_name:product_type|verified_count:0", 
                'match_ef_parent_company': '', 
                'match_created_from_created_at': '2022-10-21T15:21:20.439396Z', 
                'match_created_from_contributor': 'Klaus (Openapparel)', 
                'match_sector': "updated_at:2022-10-21T15:24:42.639399Z|contributor_id:2757|contributor_name:Klaus (Openapparel)|values:['Unspecified']|is_from_claim:False", 
                'match_confidence': 0.8985
            }
        ])

    def test_post_facilities_possible_match(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.post_facilities(
            name="ZHEJIANG ZHENGHAO GARMENT CO .,LTD",
            country="CN",
            address="HENGGENGTOU TOWN, GUALI, XIAOSHAN, HANGZHOU 311200 CN",
            sector="Apparel"
        )
        expect = [
            {
                "match_no": 1,
                "item_id": 804349,
                "lon": 120.45824,
                "lat": 30.19035,
                "geocoded_address": "Gualizhen, Xiaoshan District, Hangzhou, Zhejiang, China, 311241",
                "status": "POTENTIAL_MATCH",
                "match_id": "CN2020016QWVKKG",
                "match_lon": 120.4577832,
                "match_lat": 30.1749702,
                "match_name": "ZHEJIANG ZHENGHAO GARMENT CO., LTD. \u00a0 \u00a0",
                "match_address": "HENGGENENGTOU VILLAGE, GUALI TOWN\u00a0 , HANGZHOU, Zhejiang, 311241",
                "match_country_code": "CN",
                "match_os_id": "CN2020016QWVKKG",
                "match_other_names": "Zhejiang Zhenghao Garment Co., Ltd.",
                "match_other_addresses": "Henggengtou Village, Guali Town, Xiaoshan District\nHENGGENENGTOU VILLAGE, GUALI TOWN, Hangzhou, Zhejiang, 311241",
                "match_contributors": "id:1083|name:Amazon (Amazon Apparel Supplier List 2021)|is_verified:False|contributor_name:Amazon|list_name:Amazon Apparel Supplier List 2021\nid:2736|name:Mike Maurizi (test)|is_verified:False|contributor_name:Mike Maurizi|list_name:test\nname:2 Brands / Retailers\nname:A Multi-Stakeholder Initiative",
                "match_country_name": "China",
                "match_claim_info": "",
                "match_other_locations": "lat:30.174964|lon:120.456922|contributor_id:1083|contributor_name:Amazon|notes:None\nlat:30.19035|lon:120.45824|contributor_id:2736|contributor_name:Mike Maurizi|notes:None\nlat:30.19035|lon:120.45824|contributor_id:2736|contributor_name:Mike Maurizi|notes:None\nlat:30.19035|lon:120.45824|contributor_id:2736|contributor_name:Mike Maurizi|notes:None\nlat:30.19035|lon:120.45824|contributor_id:2736|contributor_name:Mike Maurizi|notes:None\nlat:30.19035|lon:120.45824|contributor_id:2736|contributor_name:Mike Maurizi|notes:None",
                "match_is_closed": "",
                "match_activity_reports": "",
                "match_contributor_fields": "",
                "match_new_os_id": "",
                "match_has_inexact_coordinates": False,
                "match_ef_name": "value:Zhejiang Zhenghao Garment Co., Ltd.|field_name:name|contributor_id:1083|contributor_name:Amazon|updated_at:2022-01-27T17:44:46.463277Z\nvalue:Zhejiang Zhenghao Garment Co., Ltd.|field_name:name|contributor_id:2736|contributor_name:Mike Maurizi|updated_at:2022-06-06T18:10:14.562198Z\nvalue:Zhejiang Zhenghao Garment Co., Ltd.|field_name:name|contributor_id:2736|contributor_name:Mike Maurizi|updated_at:2022-06-06T18:10:14.866662Z\nvalue:Zhejiang Zhenghao Garment Co., Ltd.|field_name:name|contributor_id:2736|contributor_name:Mike Maurizi|updated_at:2022-06-06T18:10:15.176560Z\nvalue:Zhejiang Zhenghao Garment Co., Ltd.|field_name:name|contributor_id:2736|contributor_name:Mike Maurizi|updated_at:2022-06-06T18:10:15.493182Z\nvalue:Zhejiang Zhenghao Garment Co., Ltd.|field_name:name|contributor_id:2736|contributor_name:Mike Maurizi|updated_at:2022-06-06T18:10:15.795101Z",
                "match_ef_address": "value:Henggengtou Village, Guali Town, Xiaoshan District|field_name:address|contributor_id:1083|contributor_name:Amazon|updated_at:2022-01-27T17:44:46.463277Z|is_from_claim:False\nvalue:HENGGENENGTOU VILLAGE, GUALI TOWN, Hangzhou, Zhejiang, 311241|field_name:address|contributor_id:2736|contributor_name:Mike Maurizi|updated_at:2022-06-06T18:10:14.562198Z|is_from_claim:False\nvalue:HENGGENENGTOU VILLAGE, GUALI TOWN, Hangzhou, Zhejiang, 311241|field_name:address|contributor_id:2736|contributor_name:Mike Maurizi|updated_at:2022-06-06T18:10:14.866662Z|is_from_claim:False\nvalue:HENGGENENGTOU VILLAGE, GUALI TOWN, Hangzhou, Zhejiang, 311241|field_name:address|contributor_id:2736|contributor_name:Mike Maurizi|updated_at:2022-06-06T18:10:15.176560Z|is_from_claim:False\nvalue:HENGGENENGTOU VILLAGE, GUALI TOWN, Hangzhou, Zhejiang, 311241|field_name:address|contributor_id:2736|contributor_name:Mike Maurizi|updated_at:2022-06-06T18:10:15.493182Z|is_from_claim:False\nvalue:HENGGENENGTOU VILLAGE, GUALI TOWN, Hangzhou, Zhejiang, 311241|field_name:address|contributor_id:2736|contributor_name:Mike Maurizi|updated_at:2022-06-06T18:10:15.795101Z|is_from_claim:False",
                "match_ef_number_of_workers": "",
                "match_ef_native_language_name": "",
                "match_ef_facility_type": "",
                "match_ef_processing_type": "",
                "match_ef_product_type": "",
                "match_ef_parent_company": "",
                "match_created_from_created_at": "2020-01-16T15:30:17.313926Z",
                "match_created_from_contributor": "a Brand / Retailer",
                "match_sector": "updated_at:2022-06-06T18:10:15.795101Z|contributor_id:2736|contributor_name:Mike Maurizi|values:['Apparel']|is_from_claim:False\nupdated_at:2022-03-18T02:53:17.982930Z|contributor_id:None|contributor_name:a Brand / Retailer|values:['Apparel']|is_from_claim:False\nupdated_at:2022-01-27T17:52:15.840861Z|contributor_id:None|contributor_name:a Brand / Retailer|values:['Apparel']|is_from_claim:False\nupdated_at:2022-01-27T17:44:46.463277Z|contributor_id:1083|contributor_name:Amazon|values:['Apparel']|is_from_claim:False\nupdated_at:2022-01-27T17:44:15.272839Z|contributor_id:None|contributor_name:a Multi-Stakeholder Initiative|values:['Apparel']|is_from_claim:False",
                "match_confidence": 0.5375,
                "match_confirm_match_url": "/api/facility-matches/699466/confirm/",
                "match_reject_match_url": "/api/facility-matches/699466/reject/"
            }
        ]
        assert(result == expect)
        assert(osh_api.ok)
        assert(osh_api.result == {'code': 0, 'message': '201'})

    
    def test_post_facilities_possible_match_confirm(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.post_facility_match_confirm(match_url="/api/facility-matches/699466/confirm/")
        expect = {
            'id': 804349,
            'country_name': 'China',
            'matched_os_id': 'CN2020016QWVKKG',
            'matched_address': 'HENGGENENGTOU VILLAGE, GUALI TOWN\xa0 , HANGZHOU, Zhejiang, 311241',
            'matched_name': 'ZHEJIANG ZHENGHAO GARMENT CO., LTD. \xa0 \xa0',
            'matched_lat': 30.1749702,
            'matched_lon': 120.4577832,
            'status': 'CONFIRMED_MATCH',
            'name': 'ZHEJIANG ZHENGHAO GARMENT CO .,LTD',
            'address': 'HENGGENGTOU TOWN, GUALI, XIAOSHAN, HANGZHOU 311200 CN',
            'country_code': 'CN',
            'sector': 'Apparel'
        }
        assert(result == expect)
        assert(osh_api.ok)
        assert(osh_api.reason == "200")


    def test_post_facilities_invalid_country(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.post_facilities(
            name="A",
            country="BX",
            address="C",
        )
        assert(result == {r.status_code})
        assert(osh_api.result == {'code': -1, 'message': '400'})


    def test_post_facilities_invalid_country(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.post_facilities(
            name="Nocountry, Inc.",
            address="Somestreet 12, City 1AB 2CD",
            sector="Toys"
        )
        #assert(result == {r.status_code})
        #assert(osh_api.result == {'code': -1, 'message': '400'})
        assert(result == {'status': 'PYTHON_PARAMETER_ERROR'})
        assert(osh_api.result == {'code': -102, 'message': 'Error: Empty country name given, we need a country.'})
        assert(osh_api.error)


    def test_post_facilities_new_with_additional_dict(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.post_facilities(
            name="Another new facility",
            country="Algeria",
            address="Zone Industrielle BP 14",
            sector="Food",
            data={
                "my_field_1":"data_1",
                "my_field_2":12
            }
        )
        assert(result == [
            {
                'item_id': 804380, 
                'lon': 1.659626, 
                'lat': 28.033886, 
                'geocoded_address': 'Algeria', 
                'status': 'NEW_FACILITY', 
                'os_id': 'DZ2022294Y5EP82'
            }
        ])
        assert(osh_api.ok)
        assert(osh_api.reason=="201")


    def test_post_facilities_with_timeout_handling(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.post_facilities(
            name="Another new facility",
            country="Algeria",
            address="Zone Industrielle BP 14",
            sector="Food"
        )
        assert(osh_api.ok)
        import json
        #print(json.dumps(result,indent=2))
        assert(result[0]['status']=="MATCHED")
        result = osh_api.post_facilities(
            name="Another new facility",
            country="Algeria",
            address="Zone Industrielle BP 14",
            sector="Food"
        )
        assert(osh_api.ok)
        assert(result[0]['status']=="MATCHED")


    def test_post_facilities_with_timeout_handling_trigger_timeout(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.post_facilities(
            name="Another new facility",
            country="Algeria",
            address="Zone Industrielle BP 14",
            sector="Food"
        )
        assert(osh_api.ok)
        import json
        #print(json.dumps(result,indent=2))
        assert(result[0]['status']=="MATCHED")
        result = osh_api.post_facilities(
            name="Another new facility",
            country="Algeria",
            address="Zone Industrielle BP 14",
            sector="Food",
            timeout_secs=10
        )
        assert(result['status'] == 'TIMEOUT')
        assert(osh_api.result["code"] == -2)
        assert('429 Exceeded timeout after' in osh_api.result['message'])
        print(osh_api.result["message"])

        #assert(result[0]['status']=="MATCHED")

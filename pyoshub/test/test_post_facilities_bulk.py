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
        "record_mode": 'new'
    }


@pytest.mark.vcr()
class Test_post_facilities_bulk:
    def test_post_facilities_bulk_missing_field_country(self):
        osh_api = pyoshub.OSH_API(
            url=os.environ["TEST_OSH_URL"],
            token=os.environ["TEST_OSH_TOKEN"])
        result = osh_api.post_facilities_bulk(
            [
                {
                    "name":"This could be a new facility",
                    "address":"Cl 29 No. 37-02 MARINILLA, Medellín",
                    "sector":"Construction",
                },
            ]
        )
        assert (result == [
            {
                'name': 'This could be a new facility',
                'address': 'Cl 29 No. 37-02 MARINILLA, Medellín',
                'sector': 'Construction',
                'diagnosis': 'MISSING column(s) country',
                'cleansed': False
            }
        ])

    def test_post_facilities_bulk_missing_field_country_name(self):
        osh_api = pyoshub.OSH_API(
            url=os.environ["TEST_OSH_URL"],
            token=os.environ["TEST_OSH_TOKEN"])
        result = osh_api.post_facilities_bulk(
            [
                {
                    "name":"This could be a new facility",
                    "address":"Cl 29 No. 37-02 MARINILLA, Medellín",
                    "sector":"Construction",
                },
                {
                    "address":"Cl 29 No. 37-02 MARINILLA, Medellín",
                    "sector":"Construction",
                    "country":"US"
                },
            ]
        )
        assert (result == [
            {
                'name': 'This could be a new facility',
                'address': 'Cl 29 No. 37-02 MARINILLA, Medellín',
                'sector': 'Construction',
                'diagnosis': 'MISSING column(s) country',
                'cleansed': False
            },
            {
                'address': 'Cl 29 No. 37-02 MARINILLA, Medellín',
                'sector': 'Construction',
                'country': 'US',
                'diagnosis': 'MISSING column(s) name',
                'cleansed': False
            }
        ])
        assert (osh_api.error)
        assert (osh_api.status_code == -3)

    def test_post_facilities_bulk_missing_field_country_cleansing(self):
        osh_api = pyoshub.OSH_API(
            url=os.environ["TEST_OSH_URL"],
            token=os.environ["TEST_OSH_TOKEN"])
        result = osh_api.post_facilities_bulk(
            [
                {
                    "name":"This could be,, a new N/Afacility",
                    "address":"Cl 29 No. 37-02 MARINILLA,,  , Medellín, N/A,  ,",
                    "sector":"Construction",
                },
            ],
            cleanse = True,
        )
        assert (result ==
            [
                {
                    "name": "This could be, a new facility",
                    "address": "Cl 29 No. 37-02 MARINILLA, , Medell\u00edn",
                    "sector": "Construction",
                    "diagnosis": "MISSING column(s) country",
                    "cleansed": True
                }
            ])

    def test_post_facilities_bulk_check_matches_cleansing_keep_fields(self):
        osh_api = pyoshub.OSH_API(
            url=os.environ["TEST_OSH_URL"],
            token=os.environ["TEST_OSH_TOKEN"])
        result = osh_api.post_facilities_bulk(
            [
                {
                    "name":"Some Test Facility",
                    "address":"1F Jln 2/38 Seksyen 2 Petaling Jaya, N/A, Selangor ,",
                    "sector":"Construction",
                    "country":"Malaysia",
                    "my_field":"ID12345"
                },
            ],
            cleanse = True,
        )
        #import json
        #print(json.dumps(result,indent=2))
        assert (result ==
            [
                {
                    "name": "Some Test Facility",
                    "address": "1F Jln 2/38 Seksyen 2 Petaling Jaya, Selangor",
                    "sector": "Construction",
                    "country": "Malaysia",
                    "my_field": "ID12345",
                    "diagnosis": "VALID",
                    "match_no": -1,
                    "status": "NEW_FACILITY",
                    "os_id": "MY2022297H0MC6N",
                    "lon": 101.6451971,
                    "lat": 3.0866489,
                    "geocoded_address": "1, Jalan Dispensary (2/38), Seksyen 2 Petaling Jaya, 46000 Petaling Jaya, Selangor, Malaysia",
                    "item_id": 804461,
                    "cleansed": True
                }
            ])

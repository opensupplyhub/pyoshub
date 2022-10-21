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
class Test__flatten_facilities_json:
    def test__flatten_facilities_json(self):
        before = {
            "matches": [
                {
                "id": "DE2022278H70901",
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                    10.9134482,
                    48.3829797
                    ]
                },
                "properties": {
                    "name": "Somename",
                    "address": "Strasse 17, 12345 Beispiel",
                    "country_code": "DE",
                    "os_id": "DE2022278H70901",
                    "other_names": [
                    "Hempelhuse"
                    ],
                    "other_addresses": [
                    "Strasse 17, 12345 Beispiel"
                    ],
                    "contributors": [
                    {
                        "id": 2757,
                        "name": "Somebody",
                        "is_verified": False,
                        "contributor_name": "Somebody",
                        "list_name": None
                    }
                    ],
                    "country_name": "Germany",
                    "claim_info": None,
                    "other_locations": [
                    {
                        "lat": 48.3833527,
                        "lng": 10.913465,
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "notes": None
                    }
                    ],
                    "ppe_product_types": None,
                    "ppe_contact_phone": None,
                    "ppe_contact_email": None,
                    "ppe_website": None,
                    "is_closed": None,
                    "activity_reports": [],
                    "contributor_fields": [],
                    "new_os_id": None,
                    "has_inexact_coordinates": False,
                    "extended_fields": {
                    "name": [
                        {
                        "value": "Somename",
                        "field_name": "name",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "updated_at": "2022-10-05T12:43:37.488654Z"
                        },
                        {
                        "value": "Somename",
                        "field_name": "name",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "updated_at": "2022-10-05T14:24:22.681351Z"
                        },
                        {
                        "value": "Hempelhuse",
                        "field_name": "name",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "updated_at": "2022-10-05T14:25:36.697358Z"
                        },
                        {
                        "value": "Somename",
                        "field_name": "name",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "updated_at": "2022-10-21T13:40:59.485894Z"
                        }
                    ],
                    "address": [
                        {
                        "value": "Strasse 17, 12345 Beispiel",
                        "field_name": "address",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "updated_at": "2022-10-05T12:43:37.488654Z",
                        "is_from_claim": False
                        },
                        {
                        "value": "Strasse 17, 12345 Beispiel",
                        "field_name": "address",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "updated_at": "2022-10-05T14:24:22.681351Z",
                        "is_from_claim": False
                        },
                        {
                        "value": "Strasse 17, 12345 Beispiel",
                        "field_name": "address",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "updated_at": "2022-10-05T14:25:36.697358Z",
                        "is_from_claim": False
                        },
                        {
                        "value": "Strasse 17, 12345 Beispiel",
                        "field_name": "address",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "updated_at": "2022-10-21T13:40:59.485894Z",
                        "is_from_claim": False
                        }
                    ],
                    "number_of_workers": [],
                    "native_language_name": [],
                    "facility_type": [],
                    "processing_type": [],
                    "product_type": [],
                    "parent_company": []
                    },
                    "created_from": {
                    "created_at": "2022-10-05T12:43:36.872785Z",
                    "contributor": "Somebody"
                    },
                    "sector": [
                    {
                        "updated_at": "2022-10-21T13:40:59.485894Z",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "values": [
                        "Unspecified"
                        ],
                        "is_from_claim": False
                    }
                    ]
                }
                },
                {
                "id": "DE2022278H70901",
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                    10.9134482,
                    48.3829797
                    ]
                },
                "properties": {
                    "name": "Somename",
                    "address": "Strasse 17, 12345 Beispiel",
                    "country_code": "DE",
                    "os_id": "DE2022278H70901",
                    "other_names": [
                    "Hempelhuse"
                    ],
                    "other_addresses": [
                    "Strasse 17, 12345 Beispiel"
                    ],
                    "contributors": [
                    {
                        "id": 2757,
                        "name": "Somebody",
                        "is_verified": False,
                        "contributor_name": "Somebody",
                        "list_name": None
                    }
                    ],
                    "country_name": "Germany",
                    "claim_info": None,
                    "other_locations": [
                    {
                        "lat": 48.3833527,
                        "lng": 10.913465,
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "notes": None
                    }
                    ],
                    "ppe_product_types": None,
                    "ppe_contact_phone": None,
                    "ppe_contact_email": None,
                    "ppe_website": None,
                    "is_closed": None,
                    "activity_reports": [],
                    "contributor_fields": [],
                    "new_os_id": None,
                    "has_inexact_coordinates": False,
                    "extended_fields": {
                    "name": [
                        {
                        "value": "Somename",
                        "field_name": "name",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "updated_at": "2022-10-05T12:43:37.488654Z"
                        },
                        {
                        "value": "Somename",
                        "field_name": "name",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "updated_at": "2022-10-05T14:24:22.681351Z"
                        },
                        {
                        "value": "Hempelhuse",
                        "field_name": "name",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "updated_at": "2022-10-05T14:25:36.697358Z"
                        },
                        {
                        "value": "Somename",
                        "field_name": "name",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "updated_at": "2022-10-21T13:40:59.485894Z"
                        }
                    ],
                    "address": [
                        {
                        "value": "Strasse 17, 12345 Beispiel",
                        "field_name": "address",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "updated_at": "2022-10-05T12:43:37.488654Z",
                        "is_from_claim": False
                        },
                        {
                        "value": "Strasse 17, 12345 Beispiel",
                        "field_name": "address",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "updated_at": "2022-10-05T14:24:22.681351Z",
                        "is_from_claim": False
                        },
                        {
                        "value": "Strasse 17, 12345 Beispiel",
                        "field_name": "address",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "updated_at": "2022-10-05T14:25:36.697358Z",
                        "is_from_claim": False
                        },
                        {
                        "value": "Strasse 17, 12345 Beispiel",
                        "field_name": "address",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "updated_at": "2022-10-21T13:40:59.485894Z",
                        "is_from_claim": False
                        }
                    ],
                    "number_of_workers": [],
                    "native_language_name": [],
                    "facility_type": [],
                    "processing_type": [],
                    "product_type": [],
                    "parent_company": []
                    },
                    "created_from": {
                    "created_at": "2022-10-05T12:43:36.872785Z",
                    "contributor": "Somebody"
                    },
                    "sector": [
                    {
                        "updated_at": "2022-10-21T13:40:59.485894Z",
                        "contributor_id": 2757,
                        "contributor_name": "Somebody",
                        "values": [
                        "Unspecified"
                        ],
                        "is_from_claim": False
                    }
                    ]
                }
                }
            ],
            "item_id": 804343,
            "geocoded_geometry": {
                "type": "Point",
                "coordinates": [
                10.9134482,
                48.3829797
                ]
            },
            "geocoded_address": "Soldnerstra\u00dfe 17, 86167 Augsburg, Germany",
            "status": "MATCHED",
            "os_id": "DE2022278H70901"
            }

        after = [
            {
                "match_no": 1,
                "item_id": 804343,
                "lon": 10.9134482,
                "lat": 48.3829797,
                "geocoded_address": "Soldnerstra\u00dfe 17, 86167 Augsburg, Germany",
                "status": "MATCHED",
                "os_id": "DE2022278H70901",
                "match_id": "DE2022278H70901",
                "match_lon": 10.9134482,
                "match_lat": 48.3829797,
                "match_name": "Somename",
                "match_address": "Strasse 17, 12345 Beispiel",
                "match_country_code": "DE",
                "match_os_id": "DE2022278H70901",
                "match_other_names": "Hempelhuse",
                "match_other_addresses": "Strasse 17, 12345 Beispiel",
                "match_contributors": "id:2757|name:Somebody|is_verified:False|contributor_name:Somebody|list_name:None",
                "match_country_name": "Germany",
                "match_claim_info": "",
                "match_other_locations": "lat:48.3833527|lon:10.913465|contributor_id:2757|contributor_name:Somebody|notes:None",
                "match_is_closed": "",
                "match_activity_reports": "",
                "match_contributor_fields": "",
                "match_new_os_id": "",
                "match_has_inexact_coordinates": False,
                "match_ef_name": "value:Somename|field_name:name|contributor_id:2757|contributor_name:Somebody|updated_at:2022-10-05T12:43:37.488654Z\nvalue:Somename|field_name:name|contributor_id:2757|contributor_name:Somebody|updated_at:2022-10-05T14:24:22.681351Z\nvalue:Hempelhuse|field_name:name|contributor_id:2757|contributor_name:Somebody|updated_at:2022-10-05T14:25:36.697358Z\nvalue:Somename|field_name:name|contributor_id:2757|contributor_name:Somebody|updated_at:2022-10-21T13:40:59.485894Z",
                "match_ef_address": "value:Strasse 17, 12345 Beispiel|field_name:address|contributor_id:2757|contributor_name:Somebody|updated_at:2022-10-05T12:43:37.488654Z|is_from_claim:False\nvalue:Strasse 17, 12345 Beispiel|field_name:address|contributor_id:2757|contributor_name:Somebody|updated_at:2022-10-05T14:24:22.681351Z|is_from_claim:False\nvalue:Strasse 17, 12345 Beispiel|field_name:address|contributor_id:2757|contributor_name:Somebody|updated_at:2022-10-05T14:25:36.697358Z|is_from_claim:False\nvalue:Strasse 17, 12345 Beispiel|field_name:address|contributor_id:2757|contributor_name:Somebody|updated_at:2022-10-21T13:40:59.485894Z|is_from_claim:False",
                "match_ef_number_of_workers": "",
                "match_ef_native_language_name": "",
                "match_ef_facility_type": "",
                "match_ef_processing_type": "",
                "match_ef_product_type": "",
                "match_ef_parent_company": "",
                "match_created_from_created_at": "2022-10-05T12:43:36.872785Z",
                "match_created_from_contributor": "Somebody",
                "match_sector": "updated_at:2022-10-21T13:40:59.485894Z|contributor_id:2757|contributor_name:Somebody|values:['Unspecified']|is_from_claim:False"
            },
            {
                "match_no": 2,
                "item_id": 804343,
                "lon": 10.9134482,
                "lat": 48.3829797,
                "geocoded_address": "Soldnerstra\u00dfe 17, 86167 Augsburg, Germany",
                "status": "MATCHED",
                "os_id": "DE2022278H70901",
                "match_id": "DE2022278H70901",
                "match_lon": 10.9134482,
                "match_lat": 48.3829797,
                "match_name": "Somename",
                "match_address": "Strasse 17, 12345 Beispiel",
                "match_country_code": "DE",
                "match_os_id": "DE2022278H70901",
                "match_other_names": "Hempelhuse",
                "match_other_addresses": "Strasse 17, 12345 Beispiel",
                "match_contributors": "id:2757|name:Somebody|is_verified:False|contributor_name:Somebody|list_name:None",
                "match_country_name": "Germany",
                "match_claim_info": "",
                "match_other_locations": "lat:48.3833527|lon:10.913465|contributor_id:2757|contributor_name:Somebody|notes:None",
                "match_is_closed": "",
                "match_activity_reports": "",
                "match_contributor_fields": "",
                "match_new_os_id": "",
                "match_has_inexact_coordinates": False,
                "match_ef_name": "value:Somename|field_name:name|contributor_id:2757|contributor_name:Somebody|updated_at:2022-10-05T12:43:37.488654Z\nvalue:Somename|field_name:name|contributor_id:2757|contributor_name:Somebody|updated_at:2022-10-05T14:24:22.681351Z\nvalue:Hempelhuse|field_name:name|contributor_id:2757|contributor_name:Somebody|updated_at:2022-10-05T14:25:36.697358Z\nvalue:Somename|field_name:name|contributor_id:2757|contributor_name:Somebody|updated_at:2022-10-21T13:40:59.485894Z",
                "match_ef_address": "value:Strasse 17, 12345 Beispiel|field_name:address|contributor_id:2757|contributor_name:Somebody|updated_at:2022-10-05T12:43:37.488654Z|is_from_claim:False\nvalue:Strasse 17, 12345 Beispiel|field_name:address|contributor_id:2757|contributor_name:Somebody|updated_at:2022-10-05T14:24:22.681351Z|is_from_claim:False\nvalue:Strasse 17, 12345 Beispiel|field_name:address|contributor_id:2757|contributor_name:Somebody|updated_at:2022-10-05T14:25:36.697358Z|is_from_claim:False\nvalue:Strasse 17, 12345 Beispiel|field_name:address|contributor_id:2757|contributor_name:Somebody|updated_at:2022-10-21T13:40:59.485894Z|is_from_claim:False",
                "match_ef_number_of_workers": "",
                "match_ef_native_language_name": "",
                "match_ef_facility_type": "",
                "match_ef_processing_type": "",
                "match_ef_product_type": "",
                "match_ef_parent_company": "",
                "match_created_from_created_at": "2022-10-05T12:43:36.872785Z",
                "match_created_from_contributor": "Somebody",
                "match_sector": "updated_at:2022-10-21T13:40:59.485894Z|contributor_id:2757|contributor_name:Somebody|values:['Unspecified']|is_from_claim:False"
            }
        ]

        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=False)
        result = osh_api._flatten_facilities_json(before)
        assert(result == after)
        assert(len(result) == 2)
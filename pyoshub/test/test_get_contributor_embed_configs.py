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
class Test_get_contributor_embed_configs():
    def test_get_contributor_embed_configs_valid_id(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_contributor_embed_configs(25)
        assert(result == {'embedded_map_id': 8,
                'width': '1200',
                'height': '800',
                'color': '#47b60c',
                'font': 'Arial,Helvetica,sans-serif',
                'contributor_id': 25,
                'number_of_workers_display_name': 'Number of Workers',
                'number_of_workers_visible': True,
                'number_of_workers_order': 0,
                'number_of_workers_searchable': False,
                'percent_female_workers_display_name': 'percent_female_workers',
                'percent_female_workers_visible': True,
                'percent_female_workers_order': 1,
                'percent_female_workers_searchable': False,
                'type_of_facility_display_name': 'Type of Facility',
                'type_of_facility_visible': True,
                'type_of_facility_order': 2,
                'type_of_facility_searchable': False,
                'type_of_product_display_name': 'Type of Product',
                'type_of_product_visible': True,
                'type_of_product_order': 3,
                'type_of_product_searchable': False,
                'percent_migrant_workers_display_name': 'percent_migrant_workers',
                'percent_migrant_workers_visible': True,
                'percent_migrant_workers_order': 4,
                'percent_migrant_workers_searchable': False,
                'parent_company_display_name': 'Parent Company',
                'parent_company_visible': True,
                'parent_company_order': 5,
                'parent_company_searchable': False,
                'tier_display_name': 'tier',
                'tier_visible': True,
                'tier_order': 6,
                'tier_searchable': False,
                'undefined_1_display_name': '',
                'undefined_1_visible': False,
                'undefined_1_order': 7,
                'undefined_1_searchable': False,
                'product_type_display_name': 'Product Type',
                'product_type_visible': False,
                'product_type_order': 8,
                'product_type_searchable': False,
                'facility_type_display_name': 'Facility Type',
                'facility_type_visible': False,
                'facility_type_order': 9,
                'facility_type_searchable': False,
                'processing_type_display_name': 'Processing Type',
                'processing_type_visible': False,
                'processing_type_order': 10,
                'processing_type_searchable': False,
                'prefer_contributor_name': True,
                'contributor_name': 'Levi Strauss & Co.',
                'text_search_label': 'Search a Facility Name or OAR ID',
                'map_style': 'default',
                'extended_fields_0': 'number_of_workers',
                'extended_fields_1': 'parent_company',
                'hide_sector_data': None
            }
        )
        assert(osh_api.ok)
        assert(not osh_api.error)
        assert(osh_api.reason == '200')


    def test_get_contributor_embed_configs_invalid_id(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_contributor_embed_configs(24)
        assert(result == [])
        assert(not osh_api.ok)
        assert(osh_api.error)
        assert(osh_api.reason == '403')
        assert(osh_api.result == {'code': -1, 'message': '403'})
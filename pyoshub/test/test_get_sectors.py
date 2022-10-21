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
class Test_get_sectors:
    def test_get_sectors(self):
        osh_api = pyoshub.OSH_API(url=os.environ["TEST_OSH_URL"],token=os.environ["TEST_OSH_TOKEN"],check_token=True)
        result = osh_api.get_sectors()
        assert(len(result) == 69)
        assert(result == [
            {'sector': '"Bed ""'}, 
            {'sector': '"Bed"'}, 
            {'sector': '"Knit Bottoms"'}, 
            {'sector': '"Knit Tops"'}, 
            {'sector': '"Sleepwear""'}, 
            {'sector': '#N/A'}, 
            {'sector': 'Accessori'}, 
            {'sector': 'Accessories'}, 
            {'sector': 'Advisory'}, 
            {'sector': 'Agriculture'}, 
            {'sector': 'Agriculture & Farming'}, 
            {'sector': 'Agriculture And Farming'}, 
            {'sector': 'Apparel'}, 
            {'sector': 'Appliances'}, 
            {'sector': 'Automobiles & Other Transport Vehicles'}, 
            {'sector': 'Automotive'}, 
            {'sector': 'Banking'}, 
            {'sector': 'Bath"'}, 
            {'sector': 'Bike'}, 
            {'sector': 'Chemicals'}, 
            {'sector': 'Civics'}, 
            {'sector': 'Construction'}, 
            {'sector': 'Consumer Electronics'}, 
            {'sector': 'Consumer Product'}, 
            {'sector': 'Consumer Products'}, 
            {'sector': 'Denim""'}, 
            {'sector': 'Electrical Equipment'}, 
            {'sector': 'Electricity'}, 
            {'sector': 'Electronics'}, 
            {'sector': 'Electronics/Technology'}, 
            {'sector': 'Energy'}, 
            {'sector': 'Energy & Resources'}, 
            {'sector': 'Equipment'}, 
            {'sector': 'Esg & Sustainability'}, 
            {'sector': 'Essentials'}, 
            {'sector': 'Fashion'}, 
            {'sector': 'Financial Services'}, 
            {'sector': 'Food'}, 
            {'sector': 'Food And Beverage'}, 
            {'sector': 'Food And Beverages'}, 
            {'sector': 'Footwear'}, 
            {'sector': 'Furniture'}, 
            {'sector': 'Gear'}, 
            {'sector': 'Hardlines'},
            {'sector': 'Healthcare'}, 
            {'sector': 'Home'}, 
            {'sector': 'Home Goods'}, 
            {'sector': 'Housewares'}, 
            {'sector': 'Jewelry'}, 
            {'sector': 'Knit Activewear"'}, 
            {'sector': 'Materials Manufacturing'}, 
            {'sector': 'Multi-Category'}, 
            {'sector': 'Non-Retail'}, 
            {'sector': 'Outdoor Equipment'}, 
            {'sector': 'Outerwear""'}, 
            {'sector': 'Paper'}, 
            {'sector': 'Pharmaceuticals'}, 
            {'sector': 'Renewable Energy'}, 
            {'sector': 'Repair'}, 
            {'sector': 'Shoes'}, 
            {'sector': 'Sleeping Bags'}, 
            {'sector': 'Solar Electric'}, 
            {'sector': 'Solar Energy'}, 
            {'sector': 'Sporting Goods'}, 
            {'sector': 'Technology'}, 
            {'sector': 'Tents'}, 
            {'sector': 'Textiles'}, 
            {'sector': 'Tier 2'}, 
            {'sector': 'Toys'}])
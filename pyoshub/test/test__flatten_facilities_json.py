import pytest
import pyoshub.pyoshub as pyoshub 

osh_api = pyoshub.OSH_API()


#@pytest.mark.vcr()
#def test__flatten_facilities_json():
#    global osh_api
#    result = osh_api._flatten_facilities_json()
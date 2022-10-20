"""pyosh is a Package for accessing the `Open Supply Hub API <https://opensupplyhub.org/api/docs>`_ using python."""

__version__ = "0.2.0"

import os
import yaml
import requests
import json
import urllib
import time
from typing import Union
import io
import logging


class OSH_API():
    """This is a class that wraps API access to https://opensupplyhub.org.
     
        Attributes
        ----------
        url: string
           The URL used to connect to the API
        token: string
           The autentication token used to connect to the API
        header: dict
           The header used to connect, and authenticate to the API
        api_call_count: int
           The accumulated number of API calls made during the lifetime of the object. This value is not
           persisted and gets initialised to 0 each time an object is instantiated.
        result: dict
           A distionary containing the result of the last call made. Key ``code`` is an int with an error
           code (0 being no errors, nonzero indicating an error), and ``message`` a str containing an error message.
           
       
        Example
        -------
        This is an example of a yaml configuration file which supplies a valid API endpoint URL, and an API token.
                
        .. code-block:: 
            
            OSH_URL: https://opensupplyhub.org
            OSH_TOKEN: 12345abcdef12345abcdef12345abcdef
       
    """
        
    def __init__(self, url : str = "http://opensupplyhub.org", token : str = "", 
                 path_to_env_yml : str = "", url_to_env_yml : str = "", 
                 check_token = False):
        """object generation method
        
        Parameters
        ----------
        url: str, optional, default = "http://opensupplyhub.org"
            URL of endpoint to use, defaults to https://opensupplyhub.org
        token: str, optional, default = ""
            Access token to authenticate to the API if not using any other method described in the `Authentication section <authentication.html>`_
        path_to_env_yml: str, optional, default = ""
            Path to yaml file containing access token and/or endpoint URL
        url_to_env_yml: str, optional, default = ""
            URL from where a text yaml file containing access token and/or endpoint URL can be downloaded
        check_token: bool, optional, default = False
            Whether to check API token validity during initialisation. Note this will cost one API call count.

        """
        result = {}
        self.header = {}
        credentials = {}
        self.error = False
        
        if len(path_to_env_yml) > 0:
            try:
                with open(path_to_env_yml,"rt") as f:
                    credentials = yaml.load(f,yaml.Loader)
                    self.url = credentials["OSH_URL"]
                    self.token = credentials["OSH_TOKEN"]
                    logging.info(f"using specified env file")
            except Exception as e:
                self.result = {"code":-1,"message":str(e)}
                self.error = True
                logging.error(str(e))
                return
        elif len(url_to_env_yml) > 0:
            try:
                r = requests.get(url_to_env_yml)
                credentials = yaml.load(io.StringIO(r.text),yaml.Loader)
                self.url = credentials["OSH_URL"]
                self.token = credentials["OSH_TOKEN"]
            except:
                pass
        elif os.path.exists("./.env.yml"):
            try:
                with open("./.env.yml","rt") as f:
                    credentials = yaml.load(f,yaml.Loader)
                self.url = credentials["OSH_URL"]
                self.token = credentials["OSH_TOKEN"]
            except:
                pass
        else:
            self.url = url
            if len(token)>0:
                self.token = token
        
        if "OSH_URL" in os.environ.keys():
            self.url = os.environ["OSH_URL"]
        elif "OSH_URL" in credentials.keys():
            self.url = credentials["OSH_URL"]
        else:
            self.url = url
            
        if "OSH_TOKEN" in os.environ.keys():
            self.token = os.environ["OSH_TOKEN"]
        elif "OSH_TOKEN" in credentials.keys():
            self.token = credentials["OSH_TOKEN"]
        else:
            self.token = token
         
        self.url = self.url.strip("/") # remove trailing slash as we add it
        
        self.header = {
            "accept": "application/json",
            "Authorization": f"Token {self.token}"
        }
        
        self.last_api_call_epoch = -1
        self.last_api_call_duration = -1
        self.api_call_count = 0
        self.countries = []
        self.countries_active_count = -1
        self.contributors = []
        self.post_facility_results = {
            "NEW_FACILITY":1,
            "MATCHED":2,
            "POTENTIAL_MATCH":0,
            "ERROR_MATCHING":-1
        }
        self.raw_data = {}
           
        # Check valid URL
        try:
            r = requests.get(f"{self.url}/health-check/",timeout=5)
            if r.ok:
                self.result = {"code":0,"message":"ok"}
                self.error = False
            else:
                self.result = {"code":r.status_code,"message":r.reason}
                self.error = False
        except Exception as e:
            self.result = {"code":-1,"message":str(e)}
            self.error = True
            return
        
        # Check header/token validity
        if check_token and len(self.token.strip()) == 0:
            self.result = {"code":-1,"message":"No/empty token"}
            self.error = True
        elif check_token:
            try:
                self.last_api_call_epoch = time.time()
                r = requests.get(f"{self.url}/api/facilities/count/",headers=self.header)
                self.last_api_call_duration = time.time()-self.last_api_call_epoch
                self.api_call_count += 1
                if not r.ok:
                    self.result = {"code":r.status_code,"message":str(r)}
                    self.error = True
                else:
                    # Check everything is working
                    try:
                        facilites_count_json = json.loads(r.text)
                        facilites_count = facilites_count_json["count"]
                        self.result = {"code":0,"message":"ok"}
                        self.error = False
                    except Exception as e:
                        self.result = {"code":-1,"message":"JSON error: "+str(e)}
                        self.error = True
                        return
            except Exception as e:
                self.result = {"code":-1,"message":str(e)}
                self.error = True
                return
        
        return 
    


    def get_facilities(self, q : str = "", 
                       contributors : Union[int,list] = -1,
                       lists : int = -1, contributor_types : str = "", countries : str = "",
                       boundary : dict = {}, parent_company : str = "", facility_type : str = "",
                       processing_type : str = "", product_type : str = "", number_of_workers : str = "",
                       native_language_name : str = "", detail : bool =False, sectors : str = "",
                       page : int = -1, pageSize : int = -1,) -> list:
        """Returns a list of facilities in GeoJSON format for a given query. (Maximum of 50 facilities per page if the detail parameter is fale or not specified, 10 if the detail parameter is true.)
        
        .. attention::
          Rate limits and possibly list size limitations may effect the returned values. This call
          is intended to be used in conjunction with a search filter.
         
        
        Parameters
        ----------
        q : str, optional
           Facility Name or OS ID
        contributors : int or list, optional
           Contributor ID
        lists : integer, optional
           List ID
        contributor_types : string, optional
           Contributor Type
        countries : string, optional
           Country Code
        boundary : string, optional
           Pass a GeoJSON geometry to filter by facilities within the boundaries of that geometry.
        parent_company : string, optional
           Pass a Contributor ID or Contributor name to filter by facilities with that Parent Company.
        facility_type : string, optional
           Facility type
        processing_type : string, optional
           Processing type
        product_type : string, optional
           Product type
        number_of_workers : string, optional
           Submit one of several standardized ranges to filter by facilities with a number_of_workers matching those values. Options are: "Less than 1000", "1001-5000", "5001-10000", or "More than 10000".
        native_language_name : string, optional
           The native language name of the facility
        detail : boolean, optional
           Set this to true to return additional detail about contributors and extended fields with each result. setting this to true will make the response significantly slower to return.
        sectors : string, optional
           The sectors that this facility belongs to. Values must match those returned from the `GET /api/sectors` endpoint
        page : integer, optional
           A page number within the paginated result set.
        pageSize : integer, optional
           Number of results to return per page.
           
        Returns
        -------
        list(dict)
            An array of dictionaries (key,value pairs). See table below for 
            return data structures.
            

            +-------------------------------+-----------------------------------------------+-------+
            |column                         | description                                   | type  |
            +===============================+===============================================+=======+
            |os_id                          | The OS ID                                     | str   |
            +-------------------------------+-----------------------------------------------+-------+
            |lon                            | Geographics longitude in degrees              | float |
            +-------------------------------+-----------------------------------------------+-------+
            |lat                            | Geographics latitude in degrees               | float |
            +-------------------------------+-----------------------------------------------+-------+
            |name                           | Facility name                                 | str   |
            +-------------------------------+-----------------------------------------------+-------+
            |address                        | Facility address                              | str   |
            +-------------------------------+-----------------------------------------------+-------+
            |country_code                   |`ISO 3166-2 Alpha country code                 | str   |
            |                               |<https://iso.org/obp/ui/#search/code/>`_       |       |
            +-------------------------------+-----------------------------------------------+-------+
            |country_name                   |`ISO 3166 country name                         | str   |
            |                               |<https://iso.org/obp/ui/#search/code/>`_       |       |
            +-------------------------------+-----------------------------------------------+-------+
            |address                        | Facility address                              | str   |
            +-------------------------------+-----------------------------------------------+-------+
            |has_approved_claim             | Flag indicating if facility has been claimed  | bool  |
            |                               |                                               |       |
            |                               | by owner, manager, or other authorised person |       |
            +-------------------------------+-----------------------------------------------+-------+
            |is_closed                      | Flag indicating if facility has been closed   | bool  |
            |                               |                                               |       |
            |                               | (*True*), or is currently open (*False*)      |       |
            +-------------------------------+-----------------------------------------------+-------+
            | Additional fields returned when *detail=True*                                         |
            +-------------------------------+-----------------------------------------------+-------+
            | other_names                   | Other names provided, joined with ``|``       | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | other_addresses               | Other facility addresses, joined with ``|``   | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | contributors                  | ``|`` joined contributors who provided data   | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | claim_info                    | Who claimed the facility                      | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | other_locations               |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | is_closed                     | Flag indicating facility no longer active     | bool  |
            +-------------------------------+-----------------------------------------------+-------+
            | activity_reports              |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | contributor_fields            |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | has_inexact_coordinates       | Misnomer: Geocoordinates manually entered     | bool  |
            +-------------------------------+-----------------------------------------------+-------+
            | name_extended                 |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | address_extended              |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | number_of_workers_extended    | Text indicating size of facility              | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | native_language_name_extended | Name of native facility language              | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | facility_type_extended        | Type of facility, e.g. *"Office / HQ*         | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | processing_type_extended      | Type of processing, e.g. *Packaging*          | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | product_type_extended         | Product type, e.g. *Radios*                   | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | parent_company_extended       | Name of Parent Company                        | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | created_from                  | Information about first recored creating entry| str   |
            +-------------------------------+-----------------------------------------------+-------+
            | sector                        | Business sector                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
        """
        
        parameters = []
         
        if page != -1:
            parameters.append(f"page={page}")
        if pageSize != -1:
            parameters.append(f"pageSize={pageSize}")
        if len(q) > 0:
            q = urllib.parse.quote_plus(q)
            parameters.append(f"q={q}")
        if contributors != -1:
            if isinstance(contributors,list):
                for contributor in contributors:
                    c = urllib.parse.quote_plus(str(contributor))
                    parameters.append(f"contributors={c}")
            else:
                contributors = urllib.parse.quote_plus(str(contributors))
                parameters.append(f"contributors={contributors}")
        if lists != -1:
            parameters.append(f"lists={lists}")
        if len(contributor_types) > 0:
            if isinstance(contributor_types,list):
                for contributor_type in contributor_types:
                    ct = urllib.parse.quote_plus(contributor_type)
                    parameters.append(f"contributor_types={ct}")
            else:
                contributor_types = urllib.parse.quote_plus(contributor_types)
                parameters.append(f"contributor_types={contributor_types}")
        if len(countries) > 0:
            countries = urllib.parse.quote_plus(countries)
            parameters.append(f"countries={countries}")
        if len(boundary.keys()) > 0:
            boundary = urllib.parse.quote_plus(str(boundary).replace(" ",""))
            parameters.append(f"boundary={boundary}")
        if len(parent_company) > 0:
            parent_company = urllib.parse.quote_plus(parent_company)
            parameters.append(f"parent_company={parent_company}")
        if len(facility_type) > 0:
            facility_type = urllib.parse.quote_plus(facility_type)
            parameters.append(f"facility_type={facility_type}")
        if len(processing_type) > 0:
            processing_type = urllib.parse.quote_plus(processing_type)
            parameters.append(f"processing_type={processing_type}")
        if len(product_type) > 0:
            product_type = urllib.parse.quote_plus(product_type)
            parameters.append(f"product_type={product_type}")
        if len(number_of_workers) > 0:
            number_of_workers = urllib.parse.quote_plus(number_of_workers)
            parameters.append(f"number_of_workers={number_of_workers}")
        if len(native_language_name) > 0:
            native_language_name = urllib.parse.quote_plus(native_language_name)
            parameters.append(f"native_language_name={native_language_name}")
        if detail:
            parameters.append(f"detail=true")
        else:
            parameters.append(f"detail=false")
        if len(sectors) > 0:
            sectors = urllib.parse.quote_plus(sectors)
            parameters.append(f"sectors={sectors}")
        
        parameters = "&".join(parameters)
        have_next = True
        request_url = f"{self.url}/api/facilities/?{parameters}"
        
        alldata = []
        
        while have_next:
            try:
                self.last_api_call_epoch = time.time()
                r = requests.get(request_url,headers=self.header)
                self.last_api_call_duration = time.time()-self.last_api_call_epoch
                self.api_call_count += 1
                if r.ok:
                    data = json.loads(r.text)
                    
                    for entry in data["features"]:
                        new_entry = {
                            "os_id":entry["id"],
                            "lon":entry["geometry"]["coordinates"][0],
                            "lat":entry["geometry"]["coordinates"][1],
                        }
                        for k,v in entry["properties"].items():
                            if not k.startswith("ppe_") and not k == "new_os_id":
                                new_entry[k] = v
                        alldata.append(new_entry)
                        
                    self.result = {"code":0,"message":f"{r.status_code}"}
                    if 'next' in data.keys() and data["next"] is not None:
                        request_url = data["next"]
                    else:
                        have_next = False
                    self.error = False
                else:
                    #alldata = []
                    self.result = {"code":-1,"message":f"{r.status_code}"}
                    have_next = False
                    self.error = True
            except Exception as e:
                self.result = {"code":-1,"message":str(e)}
                self.error = True
                return alldata
        
        return alldata
        #return pd.DataFrame(alldata)
  
    
    def post_facilities(self, name : str = "", address : str = "", country : str = "", sector : str ="",
                        data : dict = {}, 
                        number_of_workers : str = "",facility_type : str = "",
                        processing_type : str = "", product_type : str = "",
                        parent_company_name : str = "", native_language_name : str = "",
                        create : bool = False, public : bool = True, textonlyfallback : bool = False) -> list:
        """Add a single facility record.

        There are two ways supplying data, either via the ``name``, ``address``, ``country`` etc parameters,
        or as a dict via the ``data`` parameters, in which case the optional parameters would need
        to be the keys of the dictionary.

        Uploading a record may create a new entry, return a previously matched entry, or require you to make
        a confirm/reject selection by calling one of two corresponding API endpoints.
         
        .. uml::
        
          @startuml

          (*) --> "ingest data"
          "ingest data"  --> "sector/product types"
          "sector/product types" --> "dedupe entry"

          "dedupe entry" --> "MATCHED"
          "dedupe entry" --> "NEW_FACILITY"
          "dedupe entry" --> "POTENTIAL_MATCH"
          "dedupe entry" --> "ERROR_MATCHING"

          "POTENTIAL_MATCH" --> "confirm/reject endpoints"

          "MATCHED" -->[existing os_id] (*)
          "NEW_FACILITY" -->[new os_id] (*)
          "confirm/reject endpoints" -->[second call required] (*)
          "ERROR_MATCHING" -->[record invalid] (*)
          
          @enduml


        Parameters
        ----------
        name : str
            Name of the facility
        address : str
            Complete address of the facility
        country : str, optional
            _description_, by default ""
        sector : str, optional
            _description_, by default ""
        data : dict, optional
            _description_, by default {}
        number_of_workers : str, optional
            _description_, by default ""
        facility_type : str, optional
            _description_, by default ""
        processing_type : str, optional
            _description_, by default ""
        product_type : str, optional
            _description_, by default ""
        parent_company_name : str, optional
            _description_, by default ""
        native_language_name : str, optional
            _description_, by default ""
        create : bool, optional
            _description_, by default False
        public : bool, optional
            _description_, by default True
        textonlyfallback : bool, optional
            _description_, by default False

        Returns
        -------
        list(dict)
            An array of dictionaries (key,value pairs). See tables below for example
            return data structures, which depend on the value of the ``status`` field.


        For status == ``MATCHED``

        +--------------------------------+------------------------------------------+-------+
        | fieldname                      | description                              | type  |
        +================================+==========================================+=======+
        | match_no                       | Running number of match found            | int   |
        +--------------------------------+------------------------------------------+-------+
        | item_id                        | Internal reference                       | int   |
        +--------------------------------+------------------------------------------+-------+
        | lon                            | Geographic longitude in degrees          | float |
        +--------------------------------+------------------------------------------+-------+
        | lat                            | Geographic latitude in degrees           | float |
        +--------------------------------+------------------------------------------+-------+
        | geocoded_address               | Address returned from geocoder           | str   |
        +--------------------------------+------------------------------------------+-------+
        | status                         | Will be set to ``MATCHED``               | str   |
        +--------------------------------+------------------------------------------+-------+
        | os_id                          | The OS ID                                | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_id                       | The OS ID of the match                   | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_lon                      | Geographic longitude of match            | float |
        +--------------------------------+------------------------------------------+-------+
        | match_lat                      | Geographic latitude of match             | float |
        +--------------------------------+------------------------------------------+-------+
        | match_name                     | Facility name of match                   | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_address                  | Address of match                         | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_country_code             |Match `ISO 3166-2 ountry code             | str   |
        |                                |<https://iso.org/obp/ui/#search/code/>`_  |       |
        +--------------------------------+------------------------------------------+-------+
        | match_os_id                    | The OS ID of the match                   | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_other_names              | Other names found for match              | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_other_addresses          | Other addresses found for match          | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_contributors             | Contributors providing match             | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_country_name             |Match `ISO 3166 country name              | str   |
        |                                |<https://iso.org/obp/ui/#search/code/>`_  |       |
        +--------------------------------+------------------------------------------+-------+
        | match_claim_info               | Claim information of match               | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_other_locations          |                                          | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_is_closed                | Flag indicating if match was closed      | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_activity_reports         |                                          | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_contributor_fields       |                                          | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_new_os_id                |                                          | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_has_inexact_coordinates  | Misnomer: Geocoordinates manually        | bool  |
        |                                |                                          |       |
        |                                | entered for match                        |       |
        +--------------------------------+------------------------------------------+-------+
        | match_ef_name                  | Match extended field name                | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_ef_address               | Extended field address of match          | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_ef_number_of_workers     | Extended field number of workers of      | str   |
        |                                |                                          |       |
        |                                | match                                    |       |
        +--------------------------------+------------------------------------------+-------+
        | match_ef_native_language_name  | Native facility language of match        | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_ef_facility_type         | Facility type of match                   | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_ef_processing_type       | Processing type of match                 | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_ef_product_type          | Product type of match                    | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_ef_parent_company        | Parent company of match                  | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_created_from_created_at  | Timestamp match was created              | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_created_from_contributor | Contributor name who created match       | str   |
        +--------------------------------+------------------------------------------+-------+
        | match_sector                   | Sector assignment of match               | str   |
        +--------------------------------+------------------------------------------+-------+

        
        For status == ``NEW_FACILITY``

        +--------------------------------+------------------------------------------+-------+
        | fieldname                      | description                              | type  |
        +================================+==========================================+=======+
        | item_id                        | Internal reference                       | int   |
        +--------------------------------+------------------------------------------+-------+
        | lon                            | Geographic longitude in degrees          | float |
        +--------------------------------+------------------------------------------+-------+
        | lat                            | Geographic latitude in degrees           | float |
        +--------------------------------+------------------------------------------+-------+
        | geocoded_address               | Address returned from geocoder           | str   |
        +--------------------------------+------------------------------------------+-------+
        | status                         | Well be set to ``NEW_FACILITY``          | str   |
        +--------------------------------+------------------------------------------+-------+
        | os_id                          | The OS ID                                | str   |
        +--------------------------------+------------------------------------------+-------+
        
        For status == ``POTENTIAL_MATCH``
          In addition to the fields in ``MATCHED``
          
        +-------------------------+------------------------------------------+-------+
        | fieldname               | description                              | type  |
        +=========================+==========================================+=======+
        | match_confidence        | Numerical value between 0.0 and 1.0      | int   |
        +-------------------------+------------------------------------------+-------+
        | match_confirm_match_url | Path part of the endpoint to call        | float |
        |                         | indicating confirming this match         |       |       
        +-------------------------+------------------------------------------+-------+
        | match_confirm_match_url | Path part of the endpoint to call        | float |
        |                         | indicating rejecting this match          |       |
        +-------------------------+------------------------------------------+-------+  
        
        
        For status == ``ERROR``
        
        """
        if len(data) == 0:
            payload = {}
            
            if len(name)>0:
                payload["name"] = name.strip()
            else:
                self.result = {"code":-100,"message":"Error: Empty facility name given, we need a name."}
                return []
            
            if len(address)>0:
                payload["address"] = address.strip()
            else:
                self.result = {"code":-101,"message":"Error: Empty address given, we need an address."}
                return []
            
            if len(country)>0:
                payload["country"] = country.strip()
            else:
                self.result = {"code":-102,"message":"Error: Empty country name given, we need a country."}
                return []
            
            if len(sector)>0:
                payload["sector"] = sector.strip()
            else:
                payload["sector"] = "Unspecified"

            if len(number_of_workers)>0:
                payload["number_of_workers"] = number_of_workers.strip()
                
            if len(facility_type)>0:
                payload["facility_type"] = facility_type.strip()
                
            if len(processing_type)>0:
                payload["processing_type"] = processing_type.strip()
                
            if len(product_type)>0:
                payload["product_type"] = product_type.strip()
                
            if len(parent_company_name)>0:
                payload["parent_company_name"] = parent_company_name.strip()
                
            if len(native_language_name)>0:
                payload["native_language_name"] = native_language_name.strip()
                
        else:
            payload = data
        
        parameters = "?"
        if create:
            parameters += "create=true"
        else:
            parameters += "create=false"
            
        if public:
            parameters += "&public=true"
        else:
            parameters += "&public=false"
            
        if textonlyfallback:
            parameters += "&textonlyfallback=true"
        else:
            parameters += "&textonlyfallback=false"
                  
        try:
            self.last_api_call_epoch = time.time()
            r = requests.post(f"{self.url}/api/facilities/?{parameters}",headers=self.header,data=payload)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self.api_call_count += 1
            if r.ok:
                self.raw_data = json.loads(r.text)
                data = self._flatten_facilities_json(self.raw_data)
                self.result = {"code":0,"message":f"{r.status_code}"}
                self.error = False
            else:
                data = {"status":"HTTP_ERROR"}
                self.result = {"code":-1,"message":f"{r.status_code}"}    
                self.error = True
        except Exception as e:
            self.result = {"code":-1,"message":str(e)}
            self.error = True
            return
                
        return data
        #return pd.DataFrame(data)
    
    
    
    def post_facilities_bulk(self, records : list = [], ) -> list:
        """Add multiple records at once.
        
        .. attention::
          This function will become available at a later stage
        
        """
        return
    

    def get_facilities_match_record(self, match_id: int = -1, match_url: str = "") -> list:
        """This call is a utility call for retrieving a more detailed the match status result after a factory
        was uploaded.

        Parameters
        ----------
        match_id : int, optional
            numeric match id, this is the ``id`` part of the voting URL ``/facility-matches/{id}/confirm/``
            or reject, as returned from the post_facility call.
        match_url : str, optional
            This is the voting URL ``/facility-matches/{id}/confirm/`` or ``/facility-matches/{id}/reject/``
            or reject, as returned from the post_facility call, which will be used to retrieve the numeric 
            ``match_id``


        Returns
        -------
        list(dict)
            An array of dictionaries (key,value pairs). See table below for 
            return data structures.

            +------------------------------+---------------------------------------------------------+-------+
            | column                       | description                                             | type  |
            +==============================+=========================================================+=======+
            | id                           | match_id                                                | int   |
            +------------------------------+---------------------------------------------------------+-------+
            | status                       | one of ``PENDING``, ``REJECTED``, ``CONFIRMED``         | str   |
            +------------------------------+---------------------------------------------------------+-------+
            | confidence                   | return value of the matching algorithm, formatted float | str   |
            +------------------------------+---------------------------------------------------------+-------+
            | results_code_version         | matching code revision, if set                          | str   |
            +------------------------------+---------------------------------------------------------+-------+
            | results_recall_weight        | matching algorithm metric                               | int   |
            +------------------------------+---------------------------------------------------------+-------+
            | results_no_geocoded_items    | geocoding result flag                                   | bool  |
            +------------------------------+---------------------------------------------------------+-------+
            | results_automatic_threshold  | matching algorithm setting                              | float |
            +------------------------------+---------------------------------------------------------+-------+
            | results_gazetteer_threshold  | matching algorithm setting                              | float |
            +------------------------------+---------------------------------------------------------+-------+
            | results_no_gazetteer_matches | matching algorithm setting                              | bool  |
            +------------------------------+---------------------------------------------------------+-------+
            | os_id                        | OS ID match record pertains to                          | str   |
            +------------------------------+---------------------------------------------------------+-------+
            | name                         | facility name                                           | str   |
            +------------------------------+---------------------------------------------------------+-------+
            | address                      | facility address                                        | str   |
            +------------------------------+---------------------------------------------------------+-------+
            | location_lat                 | geographic latitude                                     | float |
            +------------------------------+---------------------------------------------------------+-------+
            | location_lng                 | geographic longitude                                    | float |
            +------------------------------+---------------------------------------------------------+-------+
            | is_active                    | flag indicating matched record is active                | bool  |
            +------------------------------+---------------------------------------------------------+-------+

        """

        #alldata = []
        #for k,v in api_facility_matches.items():
        #    if isinstance(v,dict):
        #        for kk,vv in v.items():
        #            alldata.append({
        #                "column":f"{k}_{kk}",
        #                "description": "",
        #                "type":str(type(vv)).split("'")[1]
        #            })
        #    else:
        #        alldata.append({
        #            "column":f"{k}",
        #            "description": "",
        #            "type":str(type(v)).split("'")[1]
        #        })

        return []


    def post_facility_match_confirm(self, match_id: int = -1, match_url: str = "") -> list:
        """_summary_

        Parameters
        ----------
        match_id : int, optional
            numeric match id, this is the ``id`` part of the voting URL ``/facility-matches/{id}/confirm/``
            or reject, as returned from the post_facility call.
        match_url : str, optional
            This is the voting URL ``/facility-matches/{id}/confirm/`` or ``/facility-matches/{id}/reject/``
            or reject, as returned from the post_facility call, which will be used to retrieve the numeric 
            ``match_id``

        Returns
        -------
        list
            An array of dictionaries (key,value pairs). See table below for 
            return data structures.
        
            +-----------------+-----------------------------------+------+
            |column           | description                       | type |
            +=================+===================================+======+
            |                 |                                   |      |
            +-----------------+-----------------------------------+------+
        """

        return []


    def post_facility_match_reject(self, match_id: int = -1, match_url: str = "") -> list:
        """_summary_

        Parameters
        ----------
        match_id : int, optional
            numeric match id, this is the ``id`` part of the voting URL ``/facility-matches/{id}/confirm/``
            or reject, as returned from the post_facility call.
        match_url : str, optional
            This is the voting URL ``/facility-matches/{id}/confirm/`` or ``/facility-matches/{id}/reject/``
            or reject, as returned from the post_facility call, which will be used to retrieve the numeric 
            ``match_id``

        Returns
        -------
        list
            An array of dictionaries (key,value pairs). See table below for 
            return data structures.
        
            +-----------------+-----------------------------------+------+
            |column           | description                       | type |
            +=================+===================================+======+
            |                 |                                   |      |
            +-----------------+-----------------------------------+------+
        """

        return []


    def get_contributor_types(self) -> list:
        """Get a list of contributor type choices. The original REST API returns a list of pairs of values and display names.
        As all display names and values are identical, we only return the values used in the database.
        
        Returns
        -------
        list(dict)
           An array of dictionaries (key,value pairs). See table below for 
           return data structures.
               
           +-----------------+---------------------------------+------+
           |column           | description                     | type |
           +=================++================================+======+
           |contributor_type | The values of contributor types | str  |
           +-----------------+---------------------------------+------+
        """
        
        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self.url}/api/contributor-types",headers=self.header)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self.api_call_count += 1
            
            if r.ok:
                data = [{"contributor_type":value} for value,display in json.loads(r.text)]
                self.result = {"code":0,"message":f"{r.status_code}"}
            else:
                data = []
                self.result = {"code":-1,"message":f"{r.status_code}"}
            self.contributors = data
            self.error = False
        except Exception as e:
            self.result = {"code":-1,"message":str(e)}
            self.error = True
            return []
        
        return data
        #return pd.DataFrame(self.contributors,columns=["contributor_type"])
    

    def get_countries(self) -> list:
        """Get a list of `ISO 3166-2 Alpha 2 country codes and English short names <https://www.iso.org/obp/ui/#search>` used. 
        
        Returns
        -------
        list(dict)
           An array of dictionaries (key,value pairs). See table below for 
           return data structures.
            
           +-----------+---------------------------------+------+
           |column     | description                     | type |
           +===========+=================================+======+
           |iso_3166_2 | ISO 3166-2 Alpha-2 Country Code | str  |
           +-----------+---------------------------------+------+
           |country    | ISO 3166 Country Name           | str  |
           +-----------+---------------------------------+------+
        """
        
        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self.url}/api/countries",headers=self.header)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self.api_call_count += 1
            if r.ok:
                self.raw_data = json.loads(r.text)
                data = [{"iso_3166_2":cid,"country":con} for cid,con in self.raw_data]
                self.result = {"code":0,"message":f"{r.status_code}"}
            else:
                data = []
                self.result = {"code":-1,"message":f"{r.status_code}"}
            self.countries = data
            self.error = False
        except Exception as e:
            self.result = {"code":-1,"message":str(e)}
            self.error = True
            return

        return data
        #return pd.DataFrame(self.countries,columns=["iso_3166_2","country"])
    
        
    def get_countries_active_count(self) -> int:
        """Get a count of disctinct country codes used by active facilities.
        
        Returns
        -------
        int
           disctinct country codes used by active facilities
        """
        
        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self.url}/api/countries/active_count",headers=self.header)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self.api_call_count += 1
            if r.ok:
                data = int(json.loads(r.text)["count"])
                self.result = {"code":0,"message":f"{r.status_code}"}
            else:
                data = -1
                self.result = {"code":-1,"message":f"{r.status_code}"}
            self.countries_active_count = data
            self.error = False
        except Exception as e:
            self.result = {"code":-1,"message":str(e)}
            self.error = True
            return
        
        return data


    
    def get_facility_processing_types(self) -> list:
        """Return a list of defined facility and associated processing types
        
        Returns
        -------
        list(dict)
           An array of dictionaries (key,value pairs). See table below for 
           return data structures.
            
           +-----------------+-----------------------------------------------------+------+
           |column           | description                                         | type |
           +=================+=====================================================+======+
           |facility_type    | A defined facility type, *"Office / HQ*             | str  |
           +-----------------+-----------------------------------------------------+------+
           |processing_type  | Processing, e.g. *Packaging*, for the facility type | str  |
           +-----------------+-----------------------------------------------------+------+
        """
        
        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self.url}/api/facility-processing-types/",headers=self.header)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self.api_call_count += 1
            if r.ok:
                facility_processing_types = json.loads(r.text)
                self.result = {"code":0,"message":f"{r.status_code}"}
                alldata = []
                for facility_processing_type in facility_processing_types:
                    for processingType in facility_processing_type["processingTypes"]:
                        alldata.append({
                            "facility_type":facility_processing_type["facilityType"],
                            "processing_type":processingType
                        })
                data = alldata
                self.error = False
            else:
                data = []
                self.result = {"code":-1,"message":f"{r.status_code}"}
                self.error = True
        except Exception as e:
            self.result = {"code":-1,"message":str(e)}
            self.error = True
            return

            
        self.facility_processing_types = data
        return data    
    
  
    def get_product_types(self) -> list:
        """Returns a list of product types specified in the database
        
        Returns
        -------
        list(dict)
           An array of dictionaries (key,value pairs). See table below for 
           return data structures.
            
           +-----------------+-----------------------------------------------------+------+
           |column           | description                                         | type |
           +=================+=====================================================+======+
           |product_type     | Name of product type as uploaded to the database    | str  |
           +-----------------+-----------------------------------------------------+------+
        """
        
        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self.url}/api/product-types/",headers=self.header)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self.api_call_count += 1
            if r.ok:
                self.raw_data = json.loads(r.text)
                data = [{"product_type":sector} for sector in self.raw_data]
                self.result = {"code":0,"message":f"{r.status_code}"}
                self.error = False
            else:
                data = []
                self.result = {"code":-1,"message":f"{r.status_code}"}
                self.error = True
            self.product_types = data
        except Exception as e:
            self.result = {"code":-1,"message":str(e)}
            self.error = True
            return

        return data
        #return pd.DataFrame(self.product_types,columns=["product_type"])
        
    
       
    def get_sectors(self) -> int:
        """Returns a list of sectors defined at the time of import.
        
        The sectors list is assumed to evolve over time as we better understand how to structure our data and
        how our database is being used. Upon ingestion of data, the logic tries to match an entry specified 
        in the sector field to the sector list values. If a match is found, the sector value will be
        used. If no match is found, the sector value will be set to ``Unspecified``.
        
        Returns
        -------
        list(dict)
           An array of dictionaries (key,value pairs). See table below for 
           return data structures.
            
           +-----------------+-----------------------------------------------------+------+
           |column           | description                                         | type |
           +=================+=====================================================+======+
           |sector           | Name of sector defined in the database              | str  |
           +-----------------+-----------------------------------------------------+------+
        """
        
        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self.url}/api/sectors/",headers=self.header)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self.api_call_count += 1
            if r.ok:
                self.raw_data = json.loads(r.text)
                data = [{"sector":sector} for sector in self.raw_data]
                self.result = {"code":0,"message":f"{r.status_code}"}
                self.error = False
            else:
                data = []
                self.result = {"code":-1,"message":f"{r.status_code}"}
                self.error = True
            self.sectors = data
        except Exception as e:
            self.result = {"code":-1,"message":str(e)}
            self.error = True
            return


        return data
        #return pd.DataFrame(self.sectors,columns=["sectors"])
    


    def get_workers_ranges(self) -> list:
        """Retrieve allowed texts for workes range specification, and their range:
        
        The returned numeric ranges can be used to map a numeric value onto a valid workers range
        text used across the database.
        
        Returns
        -------
        list(dict)
           An array of dictionaries (key,value pairs). See table below for 
           return data structures.
            
           +-----------------+-----------------------------------------------------+------+
           |column           | description                                         | type |
           +=================+=====================================================+======+
           |workers_range    | Text to be used, e.g. ``Less than 1000``            | str  |
           +-----------------+-----------------------------------------------------+------+
           |lower            | Numeric lower limit to select text ``n >= lower``   | int  |
           +-----------------+-----------------------------------------------------+------+
           |upper            | Numeric upper limit to select text ``n >= lower``   | int  |
           +-----------------+-----------------------------------------------------+------+
        """
        
        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self.url}/api/workers-ranges/",headers=self.header)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self.api_call_count += 1
            if r.ok:
                workers_ranges = json.loads(r.text)
                alldata = []
                for workers_range in workers_ranges:
                    if "-" in workers_range:
                        lower,upper = workers_range.split("-")
                    elif "Less" in workers_range:
                        upper = workers_range.split(" ")[-1]
                        lower = 1
                    elif "More" in workers_range:
                        lower = workers_range.split(" ")[-1]
                        upper = 999999
                    else:
                        lower = -1
                        upper = -1
                    alldata.append({
                        "workers_range":workers_range,
                        "lower":lower,
                        "upper":upper,
                    })
                self.result = {"code":0,"message":f"{r.status_code}"}
                #data = pd.DataFrame(alldata)
                data = alldata
                self.error = False
            else:
                data = {
                        "workers_range":[],
                        "lower":[],
                        "upper":[],
                }
                data = []
                self.result = {"code":-1,"message":f"{r.status_code}"}
                self.error = True
            self.workers_ranges = data
        except Exception as e:
            self.result = {"code":-1,"message":str(e)}
            self.error = True
            return

        return data



    def post_disassociate_facility(self, osh_id: str) -> list:
        """Deactivate any matches to the facility submitted by the authenticated contributor making this call.
        
        This call removes/disassociates a facility from the content provided by the contributor
        associated with the authentication token. 
        
        Parameters
        ----------
        osh_id: str
           sixteen character OS ID
           
        Returns
        -------
        list(dict)
            An array of dictionaries (key,value pairs). See table below for 
            return data structures.

            +-------------------------------+-----------------------------------------------+-------+
            |column                         | description                                   | type  |
            +===============================+===============================================+=======+
            |os_id                          | The OS ID                                     | str   |
            +-------------------------------+-----------------------------------------------+-------+
            |lon                            | Geographics longitude in degrees              | float |
            +-------------------------------+-----------------------------------------------+-------+
            |lat                            | Geographics latitude in degrees               | float |
            +-------------------------------+-----------------------------------------------+-------+
            |name                           | Facility name                                 | str   |
            +-------------------------------+-----------------------------------------------+-------+
            |address                        | Facility address                              | str   |
            +-------------------------------+-----------------------------------------------+-------+
            |country_code                   |`ISO 3166-2 Alpha country code                 | str   |
            |                               |<https://iso.org/obp/ui/#search/code/>`_       |       |
            +-------------------------------+-----------------------------------------------+-------+
            |country_name                   |`ISO 3166 country name                         | str   |
            |                               |<https://iso.org/obp/ui/#search/code/>`_       |       |
            +-------------------------------+-----------------------------------------------+-------+
            |address                        | Facility address                              | str   |
            +-------------------------------+-----------------------------------------------+-------+
            |has_approved_claim             | Flag indicating if facility has been claimed  | bool  |
            |                               |                                               |       |
            |                               | by owner, manager, or other authorised person |       |
            +-------------------------------+-----------------------------------------------+-------+
            |is_closed                      | Flag indicating if facility has been closed   | bool  |
            |                               |                                               |       |
            |                               | (*True*), or is currently open (*False*)      |       |
            +-------------------------------+-----------------------------------------------+-------+
            | Additional fields returned when *return_extended_fields=True*                         |
            +-------------------------------+-----------------------------------------------+-------+
            | other_names                   | Other names provided, joined with ``|``       | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | other_addresses               | Other facility addresses, joined with ``|``   | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | contributors                  | ``|`` joined contributors who provided data   | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | claim_info                    | Who claimed the facility                      | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | other_locations               | The unique set of geographic coordinates      | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | is_closed                     | Flag indicating facility no longer active     | bool  |
            +-------------------------------+-----------------------------------------------+-------+
            | activity_reports              | An audit trail record of changes made         | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | contributor_fields            |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | has_inexact_coordinates       | Misnomer: Geocoordinates manually entered     | bool  |
            +-------------------------------+-----------------------------------------------+-------+
            | name_extended                 | The timestamped record of names provided      | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | address_extended              | The timestamped record of                     | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | number_of_workers_extended    | Text indicating size of facility              | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | native_language_name_extended | Name of native facility language              | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | facility_type_extended        | Type of facility, e.g. *"Office / HQ*         | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | processing_type_extended      | Type of processing, e.g. *Packaging*          | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | product_type_extended         | Product type, e.g. *Radios*                   | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | parent_company_extended       | Name of Parent Company                        | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | created_from                  | Information about first recored creating entry| str   |
            +-------------------------------+-----------------------------------------------+-------+
            | sector                        | Business sector                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
        """

        return
    
    
    def get_facility_history(self, osh_id: str) -> list:
        """Returns the history of changes, or audit trail, for a facility as a list of dictionaries describing the changes.
        
        Parameters
        ----------
        osh_id: str
           sixteen character OS ID
           
        Returns
        -------
        list(dict)
            An array of dictionaries (key,value pairs). See table below for 
            return data structures.

            +-------------------------------+-----------------------------------------------+-------+
            |column                         | description                                   | type  |
            +===============================+===============================================+=======+
            | updated_at                    | Timestamp of change record                    | str   |
            |                               | ``YYYY-MM-DD HH:MM:SS.ffffff +zz:zz``         |       |        
            +-------------------------------+-----------------------------------------------+-------+
            | action                        | One of ``ASSOCIATE``, ``DISASSOCIATE``, or    | str   |
            |                               | ``CREATE``                                    |       |        
            +-------------------------------+-----------------------------------------------+-------+
            | detail                        | Change detail string                          | str   |
            +-------------------------------+-----------------------------------------------+-------+
        """
        
        #https://9f692df0338dcbc9848646c6.openapparel.org/api/facilities/DE2020080D37VCK/history/

        return
    
    
    def post_facility_open_or_closed(self, osh_id: str, closure_state: str, reason_for_report: str) -> list:
        """Report that a facility has been closed or opened.
        
        Parameters
        ----------
        osh_id: str
           sixteen character OS ID
        closure_state: str
           desired state, must be one of ``OPEN`` or ``CLOSED``
        reason_for_report: str
           Justification or explanation of state change for audit trail
           
        Returns
        -------
        list(dict)
            An array of dictionaries (key,value pairs). See table below for 
            return data structures.

            +-------------------------------+-----------------------------------------------+-------+
            |column                         | description                                   | type  |
            +===============================+===============================================+=======+
            | facility                      | The OS ID                                     | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | reported_by_user              | Userid  reporting open or closed              | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | reported_by_contributor       | Name of contributor reporting open or closed  | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | closure_state                 | one of ``CLOSED`` or ``OPEN``                 | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | approved_at                   |                                               |       |
            +-------------------------------+-----------------------------------------------+-------+
            | status_change_reason          | text giving rationale for status change       | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | status                        | one of ``PENDING``                            | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | status_change_by              | user name changing the status                 | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | status_change_date            | Timestamp of status change record             | str   |
            |                               | ``YYYY-MM-DD HH:MM:SS.ffffff +zz:zz``         |       |
            +-------------------------------+-----------------------------------------------+-------+
            | created_at                    | Timestamp of change record                    | str   |
            |                               | ``YYYY-MM-DD HH:MM:SS.ffffff +zz:zz``         |       |
            +-------------------------------+-----------------------------------------------+-------+
            | updated_at                    | Timestamp of change record                    | str   |
            |                               | ``YYYY-MM-DD HH:MM:SS.ffffff +zz:zz``         |       |
            +-------------------------------+-----------------------------------------------+-------+
            | id                            | status numeric id                             | int   |
            +-------------------------------+-----------------------------------------------+-------+
            | reason_for_report             | rationale for adding this record              | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | facility_name                 | facility name                                 | str   |
            +-------------------------------+-----------------------------------------------+-------+
        """
        
        return 
    
    
    def post_facility_open(self, osh_id: str, reason_for_report: str) -> list:
        """Report that a facility has been opened. 
        
        This is a short form of calling ``post_facility_open_or_closed`` with the named parameter
        ``closure_state="OPEN"``, helping to avoid possible errors due to typos.
        """
        
        return self.post_facility_open_or_closed(osh_id, "OPEN", reason_for_report)
    
    
    def post_facility_closed(self, osh_id: str, reason_for_report: str) -> list:
        """Report that a facility has been opened. 
        
        This is a short form of calling ``post_facility_open_or_closed`` with the named parameter
        ``closure_state="CLOSED"``, helping to avoid possible errors due to typos.
        """
        
        return self.post_facility_open_or_closed(osh_id, "CLOSED", reason_for_report)
    
    
    
  
    def get_contributor_lists(self,contributor_id : Union[int,str]) -> list:
        """Get lists for specific contributor.
        
        For interactive uploads, data are organised along the notion of lists. Suppliers often publish
        their supplier's lists on their websites, together with a name or identification relating to
        the point in time the list relates to.
        
        As an example, a list may be called '*brand* Public Supplier List 2021' .
        
        Parameters
        ----------
        contributor_id: int or str
           numeric contributor id
           
        Returns
        -------
        list(dict)
           An array of dictionaries (key,value pairs). See table below for 
           return data structures.
            
           +-----------+---------------------------------+------+
           |column     | description                     | type |
           +===========+=================================+======+
           |list_id    | The numeric ID of the list      | int  |
           +-----------+---------------------------------+------+
           |list_name  | The name of the list            | str  |
           +-----------+---------------------------------+------+
        """
        
        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self.url}/api/contributor-lists/?contributors={contributor_id}",headers=self.header)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self.api_call_count += 1

            if r.ok:
                self.raw_data = json.loads(r.text)
                data = [{"list_id":cid,"list_name":con} for cid,con in self.raw_data]
                self.result = {"code":0,"message":f"{r.status_code}"}
                self.error = False
            else:
                data = []
                self.result = {"code":-1,"message":f"{r.status_code}"}
                self.error = True
            self.contributors = data
        except Exception as e:
            self.result = {"code":-1,"message":str(e)}
            self.error = True
            return
        
        return data
        #return pd.DataFrame(self.contributors,columns=["list_id","list_name"])



    def get_contributors(self) -> list:
        """Get a list of contributors and their ID.
        
        Returns
        -------
        list(dict)
            An array of dictionaries (key,value pairs). See table below for 
            return data structures.
        
            +-----------------+-----------------------------------+------+
            |column           | description                       | type |
            +=================+===================================+======+
            |contributor_id   | The numeric ID of the contributor | int  |
            +-----------------+-----------------------------------+------+
            |contributor_name | The name of the contributor       | str  |
            +-----------------+-----------------------------------+------+
        """
        
        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self.url}/api/contributors",headers=self.header)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self.api_call_count += 1

            if r.ok:
                self.raw_data = json.loads(r.text)
                data = [{"contributor_id":cid,"contributor_name":con} for cid,con in self.raw_data]
                self.result = {"code":0,"message":f"{r.status_code}"}
                self.error = False
            else:
                data = []
                self.result = {"code":-1,"message":f"{r.status_code}"}
                self.error = True
            self.contributors = data
        except Exception as e:
            self.result = {"code":-1,"message":str(e)}
            self.error = True
            return
        
        return data
        #return pd.DataFrame(self.contributors,columns=["contributor_id","contributor_name"])
    
  
    def get_contributors_active_count(self) -> int:
        """Returns the number of active contributors.

        Returns
        -------
        active_count: int
           Number of active contributors
        """
        
        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self.url}/api/contributors/active_count",headers=self.header)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self.api_call_count += 1
            if r.ok:
                data = int(json.loads(r.text)["count"])
                self.result = {"code":0,"message":f"{r.status_code}"}
                self.error = False
            else:
                data = -1
                self.result = {"code":-1,"message":f"{r.status_code}"}
                self.error = True
            self.countries_active_count = data
        except Exception as e:
            self.result = {"code":-1,"message":str(e)}
            self.error = True
            return

   

        return data
     


    def get_facility(self,osh_id : str, return_extended_fields : bool = False ) -> dict:
        """Return detail on one facility
        
        Parameters
        ----------
        osh_id: str
           sixteen character OS ID
           
        Returns
        -------
        list(dict)
            An array of dictionaries (key,value pairs). See table below for 
            return data structures.

            +-------------------------------+-----------------------------------------------+-------+
            |column                         | description                                   | type  |
            +===============================+===============================================+=======+
            |os_id                          | The OS ID                                     | str   |
            +-------------------------------+-----------------------------------------------+-------+
            |lon                            | Geographics longitude in degrees              | float |
            +-------------------------------+-----------------------------------------------+-------+
            |lat                            | Geographics latitude in degrees               | float |
            +-------------------------------+-----------------------------------------------+-------+
            |name                           | Facility name                                 | str   |
            +-------------------------------+-----------------------------------------------+-------+
            |address                        | Facility address                              | str   |
            +-------------------------------+-----------------------------------------------+-------+
            |country_code                   |`ISO 3166-2 Alpha country code                 | str   |
            |                               |<https://iso.org/obp/ui/#search/code/>`_       |       |
            +-------------------------------+-----------------------------------------------+-------+
            |country_name                   |`ISO 3166 country name                         | str   |
            |                               |<https://iso.org/obp/ui/#search/code/>`_       |       |
            +-------------------------------+-----------------------------------------------+-------+
            |address                        | Facility address                              | str   |
            +-------------------------------+-----------------------------------------------+-------+
            |has_approved_claim             | Flag indicating if facility has been claimed  | bool  |
            |                               |                                               |       |
            |                               | by owner, manager, or other authorised person |       |
            +-------------------------------+-----------------------------------------------+-------+
            |is_closed                      | Flag indicating if facility has been closed   | bool  |
            |                               |                                               |       |
            |                               | (*True*), or is currently open (*False*)      |       |
            +-------------------------------+-----------------------------------------------+-------+
            | Additional fields returned when *return_extended_fields=True*                         |
            +-------------------------------+-----------------------------------------------+-------+
            | other_names                   | Other names provided, joined with ``|``       | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | other_addresses               | Other facility addresses, joined with ``|``   | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | contributors                  | ``|`` joined contributors who provided data   | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | claim_info                    | Who claimed the facility                      | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | other_locations               |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | is_closed                     | Flag indicating facility no longer active     | bool  |
            +-------------------------------+-----------------------------------------------+-------+
            | activity_reports              |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | contributor_fields            |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | has_inexact_coordinates       | Misnomer: Geocoordinates manually entered     | bool  |
            +-------------------------------+-----------------------------------------------+-------+
            | name_extended                 |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | address_extended              |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | number_of_workers_extended    | Text indicating size of facility              | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | native_language_name_extended | Name of native facility language              | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | facility_type_extended        | Type of facility, e.g. *"Office / HQ*         | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | processing_type_extended      | Type of processing, e.g. *Packaging*          | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | product_type_extended         | Product type, e.g. *Radios*                   | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | parent_company_extended       | Name of Parent Company                        | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | created_from                  | Information about first recored creating entry| str   |
            +-------------------------------+-----------------------------------------------+-------+
            | sector                        | Business sector                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
        """
        
        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self.url}/api/facilities/{osh_id}/",headers=self.header)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self.api_call_count += 1
            if r.ok:
                data = json.loads(r.text)
                self.raw_result = data.copy()
                self.result = {"code":0,"message":f"{r.status_code}"}
                
                entry = {
                    "id": data["id"],
                    "lon": data["geometry"]["coordinates"][0],
                    "lat": data["geometry"]["coordinates"][1]
                }
                for k,v in data["properties"].items():
                    if k.startswith("ppe_") or k == "new_os_id":
                        continue
                    elif isinstance(v,list):
                        if len(v) > 0 and isinstance(v[0],dict):
                            lines = []
                            for vv in v:
                                lines.append("|".join([f"{kkk}:{vvv}" for kkk,vvv in vv.items()]))
                            entry[k] = "\n".join(lines).replace("lng:","lon:")
                        else:
                            entry[k] = "\n".join(v)
                    elif k == "extended_fields" and return_extended_fields:
                        for kk in v.keys():
                            lines = []
                            for vv in v[kk]:
                                lines.append("|".join([f"{kkk}:{vvv}" for kkk,vvv in vv.items()]))
                            entry[f"{kk}_extended"] = "\n".join(lines).replace("lng:","lon:")
                        #self.v = v.copy()
                    elif k == "created_from":
                        self.v = v.copy()
                        entry[k] = "|".join([f"{kkk}:{vvv}" for kkk,vvv in v.items()]) 
                    elif k == "extended_fields" and not return_extended_fields:
                        pass
                    else:
                        if v is not None:
                            entry[k] = v
                        else:
                            entry[k] = ""
                #data = pd.DataFrame(entry,index=[0])
                data = entry.copy()
                self.error = False
            else:
                #data = pd.DataFrame()
                data = {}
                self.result = {"code":-1,"message":f"{r.status_code}"}
                self.error = True
        except Exception as e:
            self.result = {"code":-1,"message":str(e)}
            self.error = True
            return {}
        
        return data


    
    def get_facilities_count(self) -> int:
        """Return the number of facilities in the database.
        
        There will be more than one record per facility in general, so this is not the amount of data
        in the Open Supply Hub database, but the number of facilities with associated records.
        
        Returns
        -------
        active_count: int
           disctinct country codes used by active facilities
        """
        
        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self.url}/api/facilities/count",headers=self.header)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self.api_call_count += 1
            if r.ok:
                data = int(json.loads(r.text)["count"])
                self.result = {"code":0,"message":f"{r.status_code}"}
                self.error = False
            else:
                data = -1
                self.result = {"code":-1,"message":f"{r.status_code}"}
                self.error = True
            self.countries_active_count = data
        except Exception as e:
            self.result = {"code":-1,"message":str(e)}
            self.error = True
            return
        
        return data
    


    def get_parent_companies(self) -> list:
        """Returns a list of parent companies and either contributor ID of contributor name.
        
        .. note::
          This API call is likely to be retired and possibly replaced with a more user friendly
          version.
        
        Returns
        -------
        list(dict)
           An array of dictionaries (key,value pairs). See table below for 
           return data structures.
            
           +------------------+----------------------------------------------------+-------------+
           |column            | description                                        | type        |
           +==================+====================================================+=============+
           |key_or_contributor| Numeric key, or name of contributor                | str or int  |
           +------------------+----------------------------------------------------+-------------+
           |parent_company    | Name of parent company as uploaded to the database | str         |
           +------------------+----------------------------------------------------+-------------+
        """
        
        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self.url}/api/parent-companies/",headers=self.header)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self.api_call_count += 1
            if r.ok:
                self.raw_data = json.loads(r.text)
                data = [{"key_or_contributor":k,"parent_company":p} for k,p in self.raw_data]
                self.result = {"code":0,"message":f"{r.status_code}"}
                self.error = False
            else:
                data = []
                self.result = {"code":-1,"message":f"{r.status_code}"}
                self.error = True
            self.parent_companies = data
        except Exception as e:
            self.result = {"code":-1,"message":str(e)}
            self.error = True
            return []

        return data
        #return pd.DataFrame(self.parent_companies,columns=["key_or_something","parent_company"])
    
     


    
    def get_facilities_downloads(self) -> list:
        """Returns a list of facilities. 
                   
        Returns
        -------
        list(dict)
            An array of dictionaries (key,value pairs). See table below for 
            return data structures.
            

            +-----------------------------------+-----------------------------------------------+-------+
            | column                            | description                                   | type  |
            +===================================+===============================================+=======+
            | os_id                             | The OS ID                                     | str   |
            +-----------------------------------+-----------------------------------------------+-------+
            | contribution_date                 |                                               | str   |
            +-----------------------------------+-----------------------------------------------+-------+
            | name                              |                                               | str   |
            +-----------------------------------+-----------------------------------------------+-------+
            | address                           |                                               | str   |
            +-----------------------------------+-----------------------------------------------+-------+
            | country_code                      |                                               | str   |
            +-----------------------------------+-----------------------------------------------+-------+
            | country_name                      |                                               | str   |
            +-----------------------------------+-----------------------------------------------+-------+
            | lat                               |                                               | str   |
            +-----------------------------------+-----------------------------------------------+-------+
            | lng                               |                                               | str   |
            +-----------------------------------+-----------------------------------------------+-------+
            | sector                            |                                               | str   |
            +-----------------------------------+-----------------------------------------------+-------+
            | contributor (list)                |                                               | str   |
            +-----------------------------------+-----------------------------------------------+-------+
            | number_of_workers                 |                                               | str   |
            +-----------------------------------+-----------------------------------------------+-------+
            | parent_company                    |                                               | str   |
            +-----------------------------------+-----------------------------------------------+-------+
            | processing_type_facility_type_raw |                                               | str   |
            +-----------------------------------+-----------------------------------------------+-------+
            | facility_type                     |                                               | str   |
            +-----------------------------------+-----------------------------------------------+-------+
            | processing_type                   |                                               | str   |
            +-----------------------------------+-----------------------------------------------+-------+
            | product_type                      |                                               | str   |
            +-----------------------------------+-----------------------------------------------+-------+
            | is_closed                         |                                               | str   |
            +-----------------------------------+-----------------------------------------------+-------+
        """        
        have_next = True
        request_url = f"{self.url}/api/facilities-downloads/"
        alldata = []
        
        while have_next:
            try:
                self.last_api_call_epoch = time.time()
                r = requests.get(request_url,headers=self.header)
                self.last_api_call_duration = time.time()-self.last_api_call_epoch
                self.api_call_count += 1
                #return json.loads(r.text) #@@@@@@@@@@@@@@
                if r.ok:
                    self.raw_data = json.loads(r.text)
                    
                    for row in self.raw_data["results"]["rows"]:
                        alldata.append(dict(zip(self.raw_data["results"]["headers"],row)))
                    
                    _ = """
                    for entry in data["features"]:
                        new_entry = {
                            "os_id":entry["id"],
                            "lon":entry["geometry"]["coordinates"][0],
                            "lat":entry["geometry"]["coordinates"][1],
                        }
                        for k,v in entry["properties"].items():
                            if not k.startswith("ppe_") and not k == "new_os_id":
                                new_entry[k] = v
                        alldata.append(new_entry)
                        """
                    self.result = {"code":0,"message":f"{r.status_code}"}
                    if 'next' in self.raw_data.keys() and self.raw_data["next"] is not None:
                        request_url = self.raw_data["next"]
                    else:
                        have_next = False
                    #have_next = False
                    self.error = False
                else:
                    #alldata = []
                    self.result = {"code":-1,"message":f"{r.status_code}"}
                    have_next = False
                    self.error = True
                    return alldata
            except Exception as e:
                self.result = {"code":-1,"message":str(e)}
                self.error = True
                return alldata
        
        return alldata
        #return pd.DataFrame(alldata)
        
     
    
    def get_contributor_embed_configs(self,contributor_id : Union[int,str]) -> list:
        """Get embedded maps configuration for specific contributor.
        
        Embedded maps are a premium feature of Open Supply Hub which can be used to display a vendor/brand specific
        map on any website via ``iframes``. This call returns a wealth of data, this documentation focuses on the key
        aspects of the parameters.
        
        Parameters
        ----------
        contributor_id: str or int
           numeric contributor id
           
        Returns
        -------
        list(dict)
           An array of dictionaries (key,value pairs). See table below for 
           return data structures.
            
           +-------------------------+---------------------------------------+--------+
           |column                   | description                           | type   |
           +=========================+=======================================+========+
           |embedded_map_id          | The numeric ID of the embedded map    | int    |
           +-------------------------+---------------------------------------+--------+
           | width                   | The width of the map's iframe         | int    |
           +-------------------------+---------------------------------------+--------+
           | height                  | The height of the map's iframe        | int    |
           +-------------------------+---------------------------------------+--------+
           | color                   | The hex #RRGGBB color of the theme    | str    |
           +-------------------------+---------------------------------------+--------+
           | font                    | The font name used by the map         | int    |
           +-------------------------+---------------------------------------+--------+
           | contributor_name        | The contributor name                  | str    |
           +-------------------------+---------------------------------------+--------+
           | text_search_label       | The search label to be displayed      | str    |
           +-------------------------+---------------------------------------+--------+
           | map_style               | The map style                         | str    |
           +-------------------------+---------------------------------------+--------+
           | There will be a series of options specifying field visibility            |
           | of extended fields                                                       |
           +-------------------------+---------------------------------------+--------+
           | *field* display_name    | The text to be displayed for *param*  | str    |
           +-------------------------+---------------------------------------+--------+
           | *field* tier_visible    | Flag indicating visibility            | bool   |
           +-------------------------+---------------------------------------+--------+
           | *field* tier_order      | Sequence number for *field*           | int    |
           +-------------------------+---------------------------------------+--------+
           | *field* tier_searchable | Flag indicating *field* is searchable | bool   |
           +-------------------------+---------------------------------------+--------+
        """
        
        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self.url}/api/contributor-embed-configs/{contributor_id}/",headers=self.header)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self.api_call_count += 1
            
            if r.ok:
                data = json.loads(r.text)
                alldata = {}
                num_undefined = 1
                have_undefined = False
                for k,v in data.items():
                    if k == 'embed_fields':
                        for embedded_field in v:
                            for column in ['display_name','visible','order','searchable']:
                                if len(embedded_field["column_name"]) ==  0: # ref  https://github.com/open-apparel-registry/open-apparel-registry/issues/2200
                                    have_undefined = True
                                    alldata[f'undefined_{num_undefined}_{column}'] = embedded_field[column]
                                else:
                                    have_undefined = False
                                    alldata[f'{embedded_field["column_name"]}_{column}'] = embedded_field[column]
                            if have_undefined:
                                num_undefined += 1
                                have_undefined = False
                    elif k == 'extended_fields':
                        for i in range(len(v)):
                            alldata[f'{k}_{i}'] = v[i]
                    else:
                        if k == "id":
                            alldata["embedded_map_id"] = v
                        elif k == "contributor":
                            alldata["contributor_id"] = v
                        else:
                            alldata[k] = v
                data = alldata
                self.result = {"code":0,"message":f"{r.status_code}"}
                self.error = False
            else:
                data = []
                self.result = {"code":-1,"message":f"{r.status_code}"}
                self.error = True
        except Exception as e:
            self.result = {"code":-1,"message":str(e)}
            self.error = True
            return
        
        return data
        #return pd.DataFrame(data)
        

    
    def _flatten_facilities_json(self,json_data):
        """Convert deep facility data to a flat key,value dict.
        
        Internal use only.
        """
        base_entry = {}
        for k,v in json_data.items():
            if k == "matches":
                continue
            elif k == "geocoded_geometry":
                try:
                    base_entry["lon"] = v["coordinates"][0]
                    base_entry["lat"] = v["coordinates"][1]
                except:
                    base_entry["lon"] = -1
                    base_entry["lat"] = -1
            else:
                if v is not None:
                    base_entry[k] = v
                else:
                    base_entry[k] = ""

        alldata = []
        if len(json_data["matches"])>0:
            match_no = 1
            for match in json_data["matches"]:
                new_data = {"match_no":match_no}
                new_data.update(base_entry)#.copy()
                for k,v in match.items():
                    if isinstance(v,list):
                        raise NotImplementedError("Internal _flatten_facilities_json. Facilities data structure must have changed. "
                                                  "Instance 1/2. "
                                                  "Please report on github and/or check for an updated library.")
                        pass
                    elif k in ["Feature","type"]:
                        pass
                    elif k == "geometry":
                        new_data["match_lon"] = v["coordinates"][0]
                        new_data["match_lat"] = v["coordinates"][1]
                    elif isinstance(v,dict):
                        for kk,vv in v.items():
                            if isinstance(vv,list):
                                if len(vv) == 0:
                                    new_data[f"match_{kk}"] = ""
                                else:
                                    lines = []
                                    for vvv in vv:
                                        if isinstance(vvv,dict):
                                            lines.append("|".join([f"{kkkk}:{vvvv}" for kkkk,vvvv in vvv.items()]))
                                        elif isinstance(vvv,str):
                                            lines.append(vvv)
                                    new_data[f"match_{kk}"] = "\n".join(lines).replace("lng:","lon:")
                            elif isinstance(vv,dict):
                                for kkk,vvv in vv.items():
                                    lines = []
                                    for entry in vvv:
                                        if isinstance(entry,dict):
                                            lines.append("|".join([f"{kkkk}:{vvvv}" for kkkk,vvvv in entry.items()]))
                                        elif isinstance(entry,str):
                                            lines.append(entry)
                                        else:
                                            raise NotImplementedError("Internal _flatten_facilities_json. Facilities data structure must have changed. "
                                                                      "Instance 2/2. "
                                                                      "Please report on github and/or check for an updated library.")
                                    new_data[f"match_{kk}_{kkk}"] = "\n".join(lines).replace("lng:","lon:")
                                pass
                            elif kk.startswith("ppe_"):
                                continue
                            else:
                                new_data[f"match_{kk}"] = "" if vv is None else vv
                        pass
                    else:
                        new_data[f"match_{k}"] = "" if v is None else v

                # shorten names of dictionary keys
                new_data_keys_shortened = {}
                for k,v in new_data.items():
                    if "match_extended_fields_" in k:
                        new_data_keys_shortened[k.replace("match_extended_fields_","match_ef_")] = v
                    else:
                        new_data_keys_shortened[k] = v
                        
                alldata.append(new_data_keys_shortened)
                match_no += 1
        else:
            alldata.append(base_entry)
            
        return alldata
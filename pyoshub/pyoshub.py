"""pyosh is a Package for accessing the `Open Supply Hub API <https://opensupplyhub.org/api/docs>`_ using python."""

__version__ = "0.5.1"

import os
import yaml
import requests
import json
import urllib
import time
from typing import Union
import io
import logging
import copy
import re
import inspect


class OSH_API():
    """This is a class that wraps API access to https://opensupplyhub.org.

        Example
        -------
        This is an example of a yaml configuration file which supplies a valid API endpoint URL, and an API token.

        .. code-block::

            OSH_URL: https://opensupplyhub.org
            OSH_TOKEN: 12345abcdef12345abcdef12345abcdef

    """
    def __init__(self, url: str = "http://opensupplyhub.org", token: str = "",
                 path_to_env_yml: str = "", url_to_env_yml: str = "",
                 check_token: bool = False):
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
        self._header = {}
        credentials = {}
        self._error = False

        if len(path_to_env_yml) > 0:
            try:
                with open(path_to_env_yml, "rt") as f:
                    credentials = yaml.load(f, yaml.Loader)
                    self._url = credentials["OSH_URL"]
                    self._token = credentials["OSH_TOKEN"]
                    logging.info("using specified env file")
            except Exception as e:
                self._result = {"code": -1, "message": str(e)}
                self._error = True
                logging.error(str(e))
                return
        elif len(url_to_env_yml) > 0:
            try:
                r = requests.get(url_to_env_yml)
                credentials = yaml.load(io.StringIO(r.text), yaml.Loader)
                self._url = credentials["OSH_URL"]
                self._token = credentials["OSH_TOKEN"]
            except Exception:
                pass
        elif os.path.exists("./.env.yml"):
            try:
                with open("./.env.yml", "rt") as f:
                    credentials = yaml.load(f, yaml.Loader)
                self._url = credentials["OSH_URL"]
                self._token = credentials["OSH_TOKEN"]
            except Exception:
                pass
        else:
            self._url = url
            if len(token) > 0:
                self._token = token

        if "OSH_URL" in os.environ.keys():
            self._url = os.environ["OSH_URL"]
        elif "OSH_URL" in credentials.keys():
            self._url = credentials["OSH_URL"]
        else:
            self._url = url

        if "OSH_TOKEN" in os.environ.keys():
            self._token = os.environ["OSH_TOKEN"]
        elif "OSH_TOKEN" in credentials.keys():
            self._token = credentials["OSH_TOKEN"]
        else:
            self._token = token

        self._url = self._url.strip("/")  # remove trailing slash as we add it

        self._header = {
            "accept": "application/json",
            "Authorization": f"Token {self._token}"
        }

        self._api_call_count = 0
        self.last_api_call_epoch = -1
        self.last_api_call_duration = -1
        self.countries = []
        self.countries_active_count = -1
        self._facilites_count = -1
        self._contributors = []
        self._raw_data = ""

        # Check valid URL
        try:
            r = requests.get(f"{self._url}/health-check/", timeout=5)
            if r.ok:
                self._result = {"code": 0, "message": "ok"}
                self._error = False
            else:
                self._result = {"code": r.status_code, "message": r.reason}
                self._error = False
        except Exception as e:
            self._result = {"code": -1, "message": str(e)}
            self._error = True
            return

        # Check header/token validity
        if check_token and len(self._token.strip()) == 0:
            self._result = {"code": -1, "message": "No/empty token"}
            self._error = True
        elif check_token:
            self._raw_data = ""
            try:
                self.last_api_call_epoch = time.time()
                r = requests.get(f"{self._url}/api/facilities/count/", headers=self._header)
                self._raw_data = copy.copy(r.text)
                self.last_api_call_duration = time.time()-self.last_api_call_epoch
                self._api_call_count += 1
                if not r.ok:
                    self._result = {"code": r.status_code, "message": str(r)}
                    self._error = True
                else:
                    # Check everything is working
                    try:
                        data = json.loads(r.text)
                        self._facilites_count = data["count"]
                        self._result = {"code": 0, "message": "ok"}
                        self._error = False
                    except Exception as e:
                        self._result = {"code": -1, "message": "JSON error: "+str(e)}
                        self._error = True
                        self._facilites_count = -1
                        return
            except Exception as e:
                self._result = {"code": -1, "message": str(e)}
                self._error = True
                self._facilites_count = -1
                return
        else:
            self._raw_data = ""

        return

    @property
    def api_call_count(self) -> int:
        """The accumulated number of API calls made during the lifetime of the object. This value is not
           persisted and gets initialised to 0 each time an object is instantiated. When called as a setter,
           the number provided is added to API calls made so far.
        """
        return self._api_call_count

    @api_call_count.setter
    def api_call_count(self, value: int):
        self._api_call_count += value

    @property
    def contributors(self) -> list:
        """Return the list of contributors, if call to get_contributors had been made, or an empty list.
        """
        return self._contributors

    @property
    def raw_data(self) -> str:
        """Return the raw data from the last request made. May be empty in some conditions
        """
        return self._raw_data

    @property
    def header(self) -> dict:
        """Return the header used to make calls to the API
        """
        return self._header

    @property
    def error(self) -> bool:
        """Return True if the previously made call returned an error, False otherwises.
        """
        return self._error

    @property
    def ok(self) -> bool:
        """Return the False if the previously made call returned an error, True otherwises.
           Provided to provide interface similar to :py:func:`requests <requests:requests.request>`.
        """
        return not self._error

    @property
    def url(self) -> str:
        """URL of endpoint to use, defaults to ``https://opensupplyhub.org``.
        """
        return self._url

    @property
    def token(self) -> str:
        """Access token to authenticate to the API if not using any other method described in the `Authentication section <authentication.html>`_ .
        """
        return self._token

    @property
    def result(self) -> dict:
        """A ditionary containing the result of the last call made. Key ``code`` is an int with an error
           code (0 being no errors, nonzero indicating an error), and ``message`` a str containing an error message.
        """
        return self._result

    @property
    def status_code(self) -> int:
        """Status code part of the last call result.
           Provided to provide interface similar to :py:func:`requests <requests:requests.request>`.
        """
        return self._result["code"]

    @property
    def reason(self) -> str:
        """Error text part of the last call result, "ok" if no error.
           Provided to provide interface similar to :py:func:`requests <requests:requests.request>`.
        """
        return self._result["message"]

    @property
    def facilities_count(self) -> int:
        """Number of facilities in database, if call has been made.
        """
        return self._facilites_count

    def get_facilities(self, q: str = "",
                       contributors: Union[int, list] = -1,
                       lists: int = -1,
                       contributor_types: Union[str, list] = "",
                       countries: str = "",
                       boundary: dict = {}, parent_company: str = "", facility_type: str = "",
                       processing_type: str = "", product_type: str = "", number_of_workers: str = "",
                       native_language_name: str = "", detail: bool = False, sectors: str = "",
                       page: int = -1, pageSize: int = -1) -> list:
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
        lists : int, optional
           List ID
        contributor_types : str, or list, optional
           Contributor Type
        countries : str, optional
           Country Code
        boundary : str, optional
           Pass a GeoJSON geometry to filter by facilities within the boundaries of that geometry.
        parent_company : str, optional
           Pass a Contributor ID or Contributor name to filter by facilities with that Parent Company.
        facility_type : str, optional
           Facility type
        processing_type : str, optional
           Processing type
        product_type : str, optional
           Product type
        number_of_workers : str, optional
           Submit one of several standardized ranges to filter by facilities with a number_of_workers matching those values. Options are: "Less than 1000", "1001-5000", "5001-10000", or "More than 10000".
        native_language_name : str, optional
           The native language name of the facility
        detail : boolean, optional
           Set this to true to return additional detail about contributors and extended fields with each result. setting this to true will make the response significantly slower to return.
        sectors : str, optional
           The sectors that this facility belongs to. Values must match those returned from the `GET /api/sectors` endpoint
        page : int, optional
           A page number within the paginated result set.
        pageSize : int, optional
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
            |has_approved_claim             | Flag indicating if facility has been          | bool  |
            |                               |                                               |       |
            |                               | claimed by owner, manager, or                 |       |
            |                               |                                               |       |
            |                               | other authorised person                       |       |
            +-------------------------------+-----------------------------------------------+-------+
            |is_closed                      | Flag indicating if facility has been          | bool  |
            |                               |                                               |       |
            |                               | closed (*True*), or is currently              |       |
            |                               |                                               |       |
            |                               | open (*False*)                                |       |
            +-------------------------------+-----------------------------------------------+-------+
            | Additional fields returned when *detail=True*                                         |
            +-------------------------------+-----------------------------------------------+-------+
            | other_names                   | Other names provided, joined with             | str   |
            |                               |                                               |       |
            |                               | vertical bar ``|``                            |       |
            +-------------------------------+-----------------------------------------------+-------+
            | other_addresses               | Other facility addresses, joined with         | str   |
            |                               |                                               |       |
            |                               | vertical bar ``|``                            |       |
            +-------------------------------+-----------------------------------------------+-------+
            | contributors                  | vertical bar ``|`` joined contributors        | str   |
            |                               |                                               |       |
            |                               | who provided data                             | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | claim_info                    | Who claimed the facility                      | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | other_locations               |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | is_closed                     | Flag indicating facility no longer            | bool  |
            |                               |                                               |       |
            |                               | active                                        |       |
            +-------------------------------+-----------------------------------------------+-------+
            | activity_reports              |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | contributor_fields            |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | has_inexact_coordinates       | Geocoordinates manually entered               | bool  |
            +-------------------------------+-----------------------------------------------+-------+
            | name_extended                 |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | address_extended              |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | number_of_workers_extended    | Text indicating size of facility              | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | native_language_name_extended | Name of native facility language              | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | facility_type_extended        | Type of facility, e.g. *"Office / HQ"*        | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | processing_type_extended      | Type of processing, e.g. *Packaging*          | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | product_type_extended         | Product type, e.g. *Radios*                   | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | parent_company_extended       | Name of Parent Company                        | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | created_from                  | Information about first record                | str   |
            |                               |                                               |       |
            |                               | which created entry                           |       |
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
            if isinstance(contributors, list):
                for contributor in contributors:
                    c = urllib.parse.quote_plus(str(contributor))
                    parameters.append(f"contributors={c}")
            else:
                contributors = urllib.parse.quote_plus(str(contributors))
                parameters.append(f"contributors={contributors}")
        if lists != -1:
            parameters.append(f"lists={lists}")
        if len(contributor_types) > 0:
            if isinstance(contributor_types, list):
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
            boundary = urllib.parse.quote_plus(str(boundary).replace(" ", ""))
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
            parameters.append("detail=true")
        else:
            parameters.append("detail=false")
        if len(sectors) > 0:
            sectors = urllib.parse.quote_plus(sectors)
            parameters.append(f"sectors={sectors}")

        parameters = "&".join(parameters)
        have_next = True
        request_url = f"{self._url}/api/facilities/?{parameters}"

        alldata = []
        self._raw_data = ""

        while have_next:
            try:
                self.last_api_call_epoch = time.time()
                r = requests.get(request_url, headers=self._header)
                self._raw_data = copy.copy(r.text)
                self.last_api_call_duration = time.time()-self.last_api_call_epoch
                self._api_call_count += 1
                if r.ok:
                    data = json.loads(r.text)

                    for entry in data["features"]:
                        new_entry = {
                            "os_id": entry["id"],
                            "lon": entry["geometry"]["coordinates"][0],
                            "lat": entry["geometry"]["coordinates"][1],
                        }
                        for k, v in entry["properties"].items():
                            if not k.startswith("ppe_") and not k == "new_os_id":
                                new_entry[k] = v
                        alldata.append(new_entry)

                    self._result = {"code": 0, "message": f"{r.status_code}"}
                    if 'next' in data.keys() and data["next"] is not None:
                        request_url = data["next"]
                    else:
                        have_next = False
                    self._error = False
                else:
                    self._result = {"code": -1, "message": f"{r.status_code}"}
                    have_next = False
                    self._error = True
            except Exception as e:
                self._result = {"code": -1, "message": str(e)}
                self._error = True
                return alldata

        return alldata

    def post_facilities(self, name: str = "", address: str = "",
                        country: str = "", sector: str = "",
                        data: dict = {},
                        create: bool = False, public: bool = True,
                        textonlyfallback: bool = False, timeout_secs: int = 20,
                        number_of_workers: Union[int, str] = "", facility_type: str = "",
                        processing_type: str = "", product_type: str = "",
                        parent_company_name: str = "", native_language_name: str = "") -> list:
        """Add a single facility record.

        There are two ways supplying data, either via the ``name``, ``address``, ``country`` etc parameters,
        or as a dict via the ``data`` parameters, in which case the optional parameters would need
        to be the keys of the dictionary.

        Maned parameters will overwrite entries in the ``data`` parameter, of both methods were used.

        Uploading a record may create a new entry, return a previously matched entry, or require you to make
        a confirm/reject selection by calling one of two corresponding API endpoints.

        For checking if a match already exists, we recommend calling this method with ``create=False``, then
        check the return value for existing matches. This will reduce unnecessary processing load on our
        machine.

        See also :ref:`facility_upload_lifecycle` for a description of the overall upload lifecycle.

        .. uml::

          @startuml
            (*) --> "ingest data"
            "ingest data"  --> "sector/product types"
            "sector/product types" --> "geocoding"
            "geocoding" --> "dedupe entry"

            "dedupe entry" --> "MATCHED"
            "dedupe entry" --> "NEW_FACILITY"
            "dedupe entry" --> "POTENTIAL_MATCH"
            "dedupe entry" --> "ERROR_MATCHING"

            "POTENTIAL_MATCH" --> "confirm/reject endpoints"

            "MATCHED" -->[existing os_id] (*)
            "NEW_FACILITY" -->[new os_id] (*)
            "confirm/reject endpoints" -->[second call required] "CONFIRMED_MATCH" 
            "CONFIRMED_MATCH" --> (*)
            "ERROR_MATCHING" -->[record invalid] (*)
          @enduml

        Parameters
        ----------
        name : str
            Name of the facility
        address : str
            Complete address of the facility
        country : str, optional
            Country the facility is based in, by default "". Ideally,
            this is an `ISO 3166-2 or -3 country code or name <https://iso.org/obp/ui/#search/code/>`_
        sector : str, optional
            Economic or Industrial Sector the facility operates in, by default "". Note
            that empty sector names will internally be mapped to ``Unspecified`` during
            upload.
        data : dict, optional
            A key,value dictionary which contains keys matching the parameter list (except timeout),
            by default {}. If optional parameters are speficied in addition to this parameter, the
            optional parameters will overwrite the ``data`` entries.
        create : bool, optional
            _description_, by default False
        public : bool, optional
            _description_, by default True
        textonlyfallback : bool, optional
            _description_, by default False
        timeout : int, optional
            Timeout for the case when rate limit throttling is encountered,
            by default 90 [seconds]
        number_of_workers : int or str, optional
            Number of workers in facility, or a range as returned by :meth:`pyoshub.OSH_API.get_workers_ranges`, by default ""
        facility_type : str, optional
            Facility type, consider the values returned by :meth:`pyoshub.OSH_API.get_facility_processing_types` 
            to use standard facility types already defined, by default ""
        processing_type : str, optional
            Processing type, consider the values returned by :meth:`pyoshub.OSH_API.get_facility_processing_types` 
            to use standard processing types already defined, by default ""
        product_type : str, optional
            Product type, consider the values returned by :meth:`pyoshub.OSH_API.get_product_types` 
            to use standard product types already defined, by default ""
        parent_company_name : str, optional
            Parent company name, consider the values returned by :meth:`pyoshub.OSH_API.get_parent_companies` 
            for parent companies already defined, by default ""
        native_language_name : str, optional
            Native language name used at facility, by default ""


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
        | status                         | Will be set to MATCHED                   | str   |
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
        | match_country_code             |Match `ISO 3166-2 country code            | str   |
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
        | match_has_inexact_coordinates  | Geocoordinates manually entered          | bool  |
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
        else:
            payload = data

        if len(name) > 0:
            payload["name"] = name.strip()
        elif "name" not in payload.keys():
            self._result = {"code": -100, "message": "Error: Empty facility name given, we need a name."}
            self._error = True
            return {"status": "PYTHON_PARAMETER_ERROR"}

        if len(address) > 0:
            payload["address"] = address.strip()
        elif "address" not in payload.keys():
            self._result = {"code": -101, "message": "Error: Empty address given, we need an address."}
            self._error = True
            return {"status": "PYTHON_PARAMETER_ERROR"}

        if len(country) > 0:
            payload["country"] = country.strip()
        elif "country" not in payload.keys():
            self._result = {"code": -102, "message": "Error: Empty country name given, we need a country."}
            self._error = True
            return {"status": "PYTHON_PARAMETER_ERROR"}

        if len(sector) > 0:
            payload["sector"] = sector.strip()

        if len(number_of_workers) > 0:
            payload["number_of_workers"] = str(number_of_workers).strip()

        if len(facility_type) > 0:
            payload["facility_type"] = facility_type.strip()

        if len(processing_type) > 0:
            payload["processing_type"] = processing_type.strip()

        if len(product_type) > 0:
            payload["product_type"] = product_type.strip()

        if len(parent_company_name) > 0:
            payload["parent_company_name"] = parent_company_name.strip()

        if len(native_language_name) > 0:
            payload["native_language_name"] = native_language_name.strip()

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

        self._raw_data = ""

        try_request = True
        timeout_timestamp = time.time()
        timeout_attempt_no = 0

        while try_request:  # Timeout guard
            try:
                self.last_api_call_epoch = time.time()
                s = inspect.stack()[0]
                logging.info(f"{s.function} Calling API URL {self._url}/api/facilities/?{parameters}")
                logging.info(f"{s.function} Calling API JSON {payload}")
                r = requests.post(f"{self._url}/api/facilities/?{parameters}", headers=self._header, data=payload)
                timeout_attempt_no += 1
                self._raw_data = copy.copy(r.text)
                self.last_api_call_duration = time.time()-self.last_api_call_epoch
                self._api_call_count += 1
                if r.ok:
                    data = json.loads(r.text)
                    data = self._flatten_facilities_json(data)
                    self._result = {"code": 0, "message": f"{r.status_code}"}
                    self._error = False
                    try_request = False
                else:
                    if r.status_code == 429:
                        pattern = re.compile(".+in ([0-9]+) seconds")
                        text = json.loads(r.text)["detail"]
                        wait_time_text = pattern.findall(text)
                        if len(wait_time_text) > 0:
                            try:
                                wait_time_s = int(wait_time_text[0])
                            except Exception:
                                self._result = {"code": -1, "message": f"{r.status_code} Unexpected: Could not detect timeout value, aborting"}
                                self._error = True
                                return {"status": "ERROR"}
                            time_already_spent = time.time()-timeout_timestamp
                            if round(time_already_spent + wait_time_s - 0.5) <= timeout_secs:
                                time.sleep(wait_time_s)
                                continue
                            else:
                                self._result = {"code": -2, "message": f"{r.status_code} Exceeded timeout after {timeout_attempt_no} attempt(s) (called with: {timeout_secs} s, asked for: {wait_time_s} s, already spent {time_already_spent:.2f} s)"}
                                self._error = True
                                return {"status": "TIMEOUT"}

                    elif r.status_code == 400:
                        self._result = {"code": -1, "message": f"{r.status_code} Bad Request"}
                        self._error = True
                        return {"status": "ERROR"}
                    else:
                        self._result = {"code": -1, "message": f"{r.status_code}"}
                        self._error = True
                        return {"status": "ERROR"}
            except Exception as e:
                self._result = {"code": -1, "message": str(e)}
                self._error = True
                return {"status": "ERROR"}

        return data

    def post_facilities_bulk(self, records: list, cleanse: bool = False, 
                             auto_create = False, timeout: int = 15,
                             column_mapping: dict = {}) -> list:
        """Add multiple records at once.

        This is a utility function that allows bulk upload of records, column name remapping, and
        reasonable data content cleansing.

        Parameters
        ----------
        records : list
            A list of dicts containing key,value pairs of facilities to be uploaded. When using
            pandas dataframes, a valid list can be created by converting a 
            :py:meth:`pandas DataFrame <pandas:pandas.DataFrame>`
            using :py:meth:`df.to_dict(orient="records") <pandas:pandas.DataFrame.to_dict>`
        cleanse : bool, optional
            Flag indicating if records should be cleansed. This removes ``N/A``, and multiple sequences of commas
            intermixed with blanks
        auto_create : bool, optional
            By default, the method will look up the database for existing records, trying to find matches,
            without creating them. Setting ``auto_create`` to ``True``, new facility records will be created
            as required.
        timeout : int, optional, default 15 [seconds]
            Timeout, in seconds, to apply to individual record calls. Creation of records may be rate limited,
            which is handled by :py:meth:`~pyoshub.OSH_API.post_facilities`, this parameter can be used to
            override the default. Note this is applied, per call, i.e. per row of data.
        column_mapping: dict, optional, default empty
            Mapping between source and OSH column names.


        Returns
        -------
        list(dict)
            An array of dictionaries (key,value pairs). See :py:meth:`~pyoshub.OSH_API.post_facilities` for 
            attributes returned based on the match ``status``.

            In addition, this method will always return

            +-----------+----------------------------------------------------------------------------+-------+
            | column    | description                                                                | type  |
            +===========+============================================================================+=======+
            | name      | Name of facility as supplied                                               | str   |
            +-----------+----------------------------------------------------------------------------+-------+
            | address	| Address of facility as supplied                                            | str   |
            +-----------+----------------------------------------------------------------------------+-------+
            | ...       | Other parameters of facility as supplied                                   | ...   |
            +-----------+----------------------------------------------------------------------------+-------+
            | diagnosis	| String indicating completeness of record(s) provided                       | str   |
            |           |                                                                            |       |
            |           | Either ``VALID``, or ``MISSING column(s)`` followed with                   |       |
            |           |                                                                            |       |
            |           | a comma separated list indicating ``name``\, ``address``\,                 |       |
            |           |                                                                            |       |
            |           | ``country``                                                                |       |
            +-----------+----------------------------------------------------------------------------+-------+
            | status    | ...                                                                        |       |
            +-----------+----------------------------------------------------------------------------+-------+

        .. attention::
          This function will become available at a later stage
        """
        alldata = []

        most_important_return_attributes = ['status', 'os_id', 'lon', 'lat', 'geocoded_address']
        
        for record in records:
            new_record = {}
            cleansed = False
            for k,v in record.items():
                v = v.strip()
                if cleanse:
                    while "N/A" in v:
                        v = v.replace("N/A","").strip()
                        cleansed = True
                    while ", ," in v:
                        v = v.replace(", ,",",").strip()
                        cleansed = True
                    while "  " in v:
                        v = v.replace("  "," ").strip()
                        cleansed = True
                    while ",," in v:
                        v = v.replace(",,",",").strip()
                        cleansed = True
                    while v.endswith(","):
                        v = v[:-1].strip().strip()
                        cleansed = True

                if k in column_mapping.keys():
                    new_record[column_mapping[k]] = v.strip()
                else:
                    new_record[k] = v.strip()
                    
            to_delete = []
            for k in new_record.keys():
                if len(new_record[k]) == 0:
                    to_delete.append(k)
            for k in to_delete:
                del new_record[k]
    
            if "country" in record.keys() and "name" in record.keys() and "address" in record.keys():
                new_record["diagnosis"] = "VALID"
                result = self.post_facilities(data=new_record,create=False)
                s = inspect.stack()[0]
                logging.info(f"{s.function} cleansed record {new_record}")
                _ = """
                ['item_id', 'lon', 'lat', 'geocoded_address', 'status', 'os_id']
                [
                  {
                    "item_id": 804450,
                    "lon": 51.9238373,
                    "lat": 47.0944959,
                    "geocoded_address": "Atyrau, Kazakhstan",
                    "status": "NEW_FACILITY",
                    "os_id": "KZ20222978AEQXH"
                  }
                ]"""
                # now append new 
                for match in result:
                    if match["status"] == "NEW_FACILITY":
                        new_record["match_no"] = -1
                    # Lets make sure the more important attributes are on the left
                    for key in most_important_return_attributes:
                        new_record[key] = match[key]
                    for k,v in match.items():
                        if k not in most_important_return_attributes:
                            new_record[k] = match[k]
            else:
                diagnosis = "MISSING column(s) "
                missing = []
                for field in ["name","address","country"]:
                    if field not in record.keys():
                        missing.append(field)
                diagnosis += ",".join(missing)
                new_record["diagnosis"] = diagnosis
                self._result = {"code": -3, "message": diagnosis}
                self._error = True

            new_record["cleansed"] = cleansed
            alldata.append(new_record)

        return alldata

    def get_facilities_match_record(self, match_id: int = -1, match_url: str = "") -> list:
        """This call is a utility call for retrieving a more detailed the match status result after a factory
        was uploaded.

        .. WARNING:: Implementation of this method has been postponed and an empty list will be returned.

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
            | status                       | one of ``PENDING``, ``REJECTED``,                       | str   |
            |                              |                                                         |       |
            |                              | ``CONFIRMED``                                           |       |
            +------------------------------+---------------------------------------------------------+-------+
            | confidence                   | return value of the matching                            | str   |
            |                              |                                                         |       |
            |                              | algorithm, str formatted float                          |       |
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

        # alldata = []
        # for k,v in api_facility_matches.items():
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
        """Confirm a match to an existing record as a response to a ``post_facilities`` call.

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

            +-----------------+----------------------------------------------+-------+
            |column           | description                                  | type  |
            +=================+==============================================+=======+
            | id              | Record number                                | int   |
            +-----------------+----------------------------------------------+-------+
            | country_name    | Match `ISO 3166 country name                 | str   |
            |                 | <https://iso.org/obp/ui/#search/code/>`_     |       |
            +-----------------+----------------------------------------------+-------+
            | matched_os_id   | ``OS ID`` of the matched facility            | str   |
            +-----------------+----------------------------------------------+-------+
            | matched_address | Address of the matched facility              | str   |
            +-----------------+----------------------------------------------+-------+
            | matched_name    | Name of the matched facility                 | str   |
            +-----------------+----------------------------------------------+-------+
            | matched_lat     | Geographic latitude of the matched facility  | float |
            +-----------------+----------------------------------------------+-------+
            | matched_lon     | Geographic longitude of the matched facility | float |
            +-----------------+----------------------------------------------+-------+
            | status          | ``CONFIRMED_MATCH``                          | str   |
            +-----------------+----------------------------------------------+-------+
            | name            | Facility name as provided                    | str   |
            +-----------------+----------------------------------------------+-------+
            | address         | Facility address as provided                 | str   |
            +-----------------+----------------------------------------------+-------+
            | country_code    | Country code from country name as provided   | str   |
            +-----------------+----------------------------------------------+-------+
            | sector          | Sector as provided                           | str   |
            +-----------------+----------------------------------------------+-------+
        """
        if len(match_url) > 0:
            url_to_call = match_url
        elif match_id > 0:
            url_to_call = f"/api/facility-matches/{match_id}/confirm/"
        else:
            data = {"status": "need a valid match_id or match_url"}
            self._result = {"code": -1, "message": "need a valid match_id or match_url"}
            self._error = True
            return data

        try:
            self.last_api_call_epoch = time.time()
            r = requests.post(f"{self._url}{url_to_call}", headers=self._header)
            self._raw_data = copy.copy(r.text)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self._api_call_count += 1
            if r.ok:
                data = json.loads(r.text)
                self._result = {"code": 0, "message": f"{r.status_code}"}
                self._error = False

                new_data = {}

                for k, v in data.items():
                    if k == "matched_facility":
                        for kk, vv in v.items():
                            if kk == "location":
                                new_data["matched_lat"] = vv["lat"]
                                new_data["matched_lon"] = vv["lng"]
                            elif "created_from_id" == kk:
                                continue
                            else:
                                new_data[f"matched_{kk}"] = vv
                    elif k == "sector":
                        new_data[k] = "|".join(v)
                    elif isinstance(v, dict):
                        pass
                    elif isinstance(v, list):
                        pass
                    elif k in ["raw_data", "row_index", "source"]:
                        continue
                    elif k.startswith("ppe_"):
                        continue
                    elif k.startswith("processing_"):
                        continue
                    elif k.startswith("clean_"):
                        continue
                    else:
                        new_data[k] = v

                data = new_data
            else:
                data = {"status": "HTTP_ERROR"}
                self._result = {"code": -1, "message": f"{r.status_code}"}
                self._error = True
        except Exception as e:
            self._result = {"code": -1, "message": str(e)}
            self._error = True
            return

        return data

    def post_facility_match_reject(self, match_id: int = -1, match_url: str = "") -> list:
        """Confirm a match to an existing record as a response to a ``post_facilities`` call,
        resulting in creation of a ``NEW_FACILITY`` new entry.

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

            +-----------------+----------------------------------------------+-------+
            |column           | description                                  | type  |
            +=================+==============================================+=======+
            | id              | Record number                                | int   |
            +-----------------+----------------------------------------------+-------+
            | country_name    | Match `ISO 3166 country name                 | str   |
            |                 | <https://iso.org/obp/ui/#search/code/>`_     |       |
            +-----------------+----------------------------------------------+-------+
            | matched_os_id   | ``OS ID`` of the matched facility            | str   |
            +-----------------+----------------------------------------------+-------+
            | matched_address | Address of the matched facility              | str   |
            +-----------------+----------------------------------------------+-------+
            | matched_name    | Name of the matched facility                 | str   |
            +-----------------+----------------------------------------------+-------+
            | matched_lat     | Geographic latitude of the matched facility  | float |
            +-----------------+----------------------------------------------+-------+
            | matched_lon     | Geographic longitude of the matched facility | float |
            +-----------------+----------------------------------------------+-------+
            | status          | ``CONFIRMED_MATCH``                          | str   |
            +-----------------+----------------------------------------------+-------+
            | name            | Facility name as provided                    | str   |
            +-----------------+----------------------------------------------+-------+
            | address         | Facility address as provided                 | str   |
            +-----------------+----------------------------------------------+-------+
            | country_code    | Country code from country name as provided   | str   |
            +-----------------+----------------------------------------------+-------+
            | sector          | Sector as provided                           | str   |
            +-----------------+----------------------------------------------+-------+
        """

        if len(match_url) > 0:
            url_to_call = match_url
        elif match_id > 0:
            url_to_call = f"/api/facility-matches/{match_id}/reject/"
        else:
            data = {"status": "need a valid match_id or match_url"}
            self._result = {"code": -1, "message": "need a valid match_id or match_url"}
            self._error = True
            return data

        try:
            self.last_api_call_epoch = time.time()
            r = requests.post(f"{self._url}{url_to_call}", headers=self._header)
            self._raw_data = copy.copy(r.text)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self._api_call_count += 1
            if r.ok:
                data = json.loads(r.text)
                self._result = {"code": 0, "message": f"{r.status_code}"}
                self._error = False

                new_data = {}

                for k, v in data.items():
                    if k == "matched_facility":
                        for kk, vv in v.items():
                            if kk == "location":
                                new_data["matched_lat"] = vv["lat"]
                                new_data["matched_lon"] = vv["lng"]
                            elif "created_from_id" == kk:
                                continue
                            else:
                                new_data[f"matched_{kk}"] = vv
                    elif k == "sector":
                        new_data[k] = "|".join(v)
                    elif isinstance(v, dict):
                        pass
                    elif isinstance(v, list):
                        pass
                    elif k in ["raw_data", "row_index", "source"]:
                        continue
                    elif k.startswith("ppe_"):
                        continue
                    elif k.startswith("processing_"):
                        continue
                    elif k.startswith("clean_"):
                        continue
                    else:
                        new_data[k] = v

                data = new_data
            else:
                data = {"status": "HTTP_ERROR"}
                self._result = {"code": -1, "message": f"{r.status_code}"}
                self._error = True
        except Exception as e:
            self._result = {"code": -1, "message": str(e)}
            self._error = True
            return

        return data

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
            r = requests.get(f"{self._url}/api/contributor-types", headers=self._header)
            self._raw_data = copy.copy(r.text)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self._api_call_count += 1

            if r.ok:
                data = [{"contributor_type": value} for value, display in json.loads(r.text)]
                self._result = {"code": 0, "message": f"{r.status_code}"}
            else:
                data = []
                self._result = {"code": -1, "message": f"{r.status_code}"}
            self._contributors = data
            self._error = False
        except Exception as e:
            self._result = {"code": -1, "message": str(e)}
            self._contributors = []
            self._error = True
            return []

        return data

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
            r = requests.get(f"{self._url}/api/countries", headers=self._header)
            self._raw_data = copy.copy(r.text)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self._api_call_count += 1
            if r.ok:
                data = [{"iso_3166_2": cid, "country": con} for cid, con in json.loads(r.text)]
                self._result = {"code": 0, "message": f"{r.status_code}"}
            else:
                data = []
                self._result = {"code": -1, "message": f"{r.status_code}"}
            self.countries = data
            self._error = False
        except Exception as e:
            self._result = {"code": -1, "message": str(e)}
            self._error = True
            return

        return data

    def get_countries_active_count(self) -> int:
        """Get a count of disctinct country codes used by active facilities.

        Returns
        -------
        int
           disctinct country codes used by active facilities
        """

        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self._url}/api/countries/active_count", headers=self._header)
            self._raw_data = copy.copy(r.text)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self._api_call_count += 1
            if r.ok:
                data = int(json.loads(r.text)["count"])
                self._result = {"code": 0, "message": f"{r.status_code}"}
            else:
                data = {}
                data = -1
                self._result = {"code": -1, "message": f"{r.status_code}"}
            self.countries_active_count = data
            self._error = False
        except Exception as e:
            self._result = {"code": -1, "message": str(e)}
            self._error = True
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
            r = requests.get(f"{self._url}/api/facility-processing-types/", headers=self._header)
            self._raw_data = copy.copy(r.text)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self._api_call_count += 1
            if r.ok:
                data = json.loads(r.text)
                facility_processing_types = data
                self._result = {"code": 0, "message": f"{r.status_code}"}
                alldata = []
                for facility_processing_type in facility_processing_types:
                    for processingType in facility_processing_type["processingTypes"]:
                        alldata.append({
                            "facility_type": facility_processing_type["facilityType"],
                            "processing_type": processingType
                        })
                data = alldata
                self._error = False
            else:
                data = []
                self._result = {"code": -1, "message": f"{r.status_code}"}
                self._error = True
        except Exception as e:
            self._result = {"code": -1, "message": str(e)}
            self._error = True
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
            r = requests.get(f"{self._url}/api/product-types/", headers=self._header)
            self._raw_data = copy.copy(r.text)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self._api_call_count += 1
            if r.ok:
                data = [{"product_type": sector} for sector in json.loads(r.text)]
                self._result = {"code": 0, "message": f"{r.status_code}"}
                self._error = False
            else:
                data = []
                self._result = {"code": -1, "message": f"{r.status_code}"}
                self._error = True
            self.product_types = data
        except Exception as e:
            self._result = {"code": -1, "message": str(e)}
            self._error = True
            return

        return data

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
            r = requests.get(f"{self._url}/api/sectors/", headers=self._header)
            self._raw_data = copy.copy(r.text)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self._api_call_count += 1
            if r.ok:
                data = [{"sector": sector} for sector in json.loads(r.text)]
                self._result = {"code": 0, "message": f"{r.status_code}"}
                self._error = False
            else:
                data = []
                self._result = {"code": -1, "message": f"{r.status_code}"}
                self._error = True
            self.sectors = data
        except Exception as e:
            self._result = {"code": -1, "message": str(e)}
            self._error = True
            return

        return data

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
            r = requests.get(f"{self._url}/api/workers-ranges/", headers=self._header)
            self._raw_data = copy.copy(r.text)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self._api_call_count += 1
            if r.ok:
                workers_ranges = json.loads(r.text)
                alldata = []
                for workers_range in workers_ranges:
                    if "-" in workers_range:
                        lower, upper = workers_range.split("-")
                    elif "Less" in workers_range:
                        upper = workers_range.split(" ")[-1]
                        lower = 1
                    elif "More" in workers_range:
                        lower = workers_range.split(" ")[-1]
                        upper = 99999999
                    else:
                        lower = -1
                        upper = -1
                    alldata.append({
                        "workers_range": workers_range,
                        "lower": int(lower),
                        "upper": int(upper),
                    })
                self._result = {"code": 0, "message": f"{r.status_code}"}
                data = alldata
                self._error = False
            else:
                data = {
                        "workers_range": [],
                        "lower": [],
                        "upper": [],
                }
                self._result = {"code": -1, "message": f"{r.status_code}"}
                self._error = True
            self.workers_ranges = data
        except Exception as e:
            self._result = {"code": -1, "message": str(e)}
            self._error = True
            return
        return data

    def post_disassociate_facility(self, osh_id: str) -> list:
        """Deactivate any matches to the facility submitted by the authenticated contributor making this call.

        .. WARNING:: Implementation of this method has been postponed and an empty list will be returned.

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
            |has_approved_claim             | Flag indicating if facility has been          | bool  |
            |                               |                                               |       |
            |                               | claimed by owner, manager, or other           |       |
            |                               |                                               |       |
            |                               | authorised person                             |       |
            +-------------------------------+-----------------------------------------------+-------+
            |is_closed                      | Flag indicating if facility is closed         | bool  |
            |                               |                                               |       |
            |                               | (*True*), or is currently open (*False*)      |       |
            +-------------------------------+-----------------------------------------------+-------+
            | Additional fields returned when *return_extended_fields=True*                         |
            +-------------------------------+-----------------------------------------------+-------+
            | other_names                   | Other names provided, joined with             | str   |
            |                               |                                               |       |
            |                               | vertical bar ``|``                            |       |
            +-------------------------------+-----------------------------------------------+-------+
            | other_addresses               | Other facility addresses, joined with         | str   |
            |                               |                                               |       |
            |                               | vertical bar ``|``                            |       |
            +-------------------------------+-----------------------------------------------+-------+
            | contributors                  | vertical bar ``|`` joined contributors        | str   |
            |                               |                                               |       |
            |                               | who provided data                             | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | claim_info                    | Who claimed the facility                      | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | other_locations               | The unique set of geographic                  | str   |
            |                               |                                               |       |
            |                               | coordinates                                   |       |
            +-------------------------------+-----------------------------------------------+-------+
            | activity_reports              | An audit trail record of changes              | str   |
            |                               |                                               |       |
            |                               | made                                          |       |
            +-------------------------------+-----------------------------------------------+-------+
            | contributor_fields            |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | has_inexact_coordinates       | Geocoordinates manually entered               | bool  |
            +-------------------------------+-----------------------------------------------+-------+
            | name_extended                 | The timestamped record of names               | str   |
            |                               |                                               |       |
            |                               | provided so far                               |       |
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
            | created_from                  | Information about first record                | str   |
            |                               |                                               |       |
            |                               | which created entry                           |       |
            +-------------------------------+-----------------------------------------------+-------+
            | sector                        | Business sector                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
        """

        return []

    def get_facility_history(self, osh_id: str) -> list:
        """Returns the history of changes, or audit trail, for a facility as a list of dictionaries describing the changes.

        .. WARNING:: Implementation of this method has been postponed and an empty list will be returned.

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

        return []

    def post_facility_open_or_closed(self, osh_id: str,
                                     closure_state: str,
                                     reason_for_report: str) -> list:
        """Report that a facility has been closed or opened.

        .. WARNING:: Implementation of this method has been postponed and an empty list will be returned.

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

        return []

    def post_facility_open(self, osh_id: str, reason_for_report: str) -> list:
        """Report that a facility has been opened.

        .. WARNING:: Implementation of this method has been postponed and an empty list will be returned.

        This is a short form of calling ``post_facility_open_or_closed`` with the named parameter
        ``closure_state="OPEN"``, helping to avoid possible errors due to typos.
        """

        return self.post_facility_open_or_closed(osh_id, "OPEN", reason_for_report)

    def post_facility_closed(self, osh_id: str, reason_for_report: str) -> list:
        """Report that a facility has been opened.

        .. WARNING:: Implementation of this method has been postponed and an empty list will be returned.

        This is a short form of calling ``post_facility_open_or_closed`` with the named parameter
        ``closure_state="CLOSED"``, helping to avoid possible errors due to typos.
        """

        return self.post_facility_open_or_closed(osh_id, "CLOSED", reason_for_report)

    def get_contributor_lists(self, contributor_id: Union[int, str]) -> list:
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
           return data structures. Note that an empty list will be
           returned, together with a status code indicating ``ok`` even
           if an invalid supplier was specified.

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
            r = requests.get(f"{self._url}/api/contributor-lists/?contributors={contributor_id}", headers=self._header)
            self._raw_data = copy.copy(r.text)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self._api_call_count += 1

            if r.ok:
                data = [{"list_id": cid, "list_name": con} for cid, con in json.loads(r.text)]
                self._result = {"code": 0, "message": f"{r.status_code}"}
                self._error = False
            else:
                data = []
                self._result = {"code": -1, "message": f"{r.status_code}"}
                self._error = True
            self._contributors = data
        except Exception as e:
            self._result = {"code": -1, "message": str(e)}
            self._error = True
            return

        return data

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
            r = requests.get(f"{self._url}/api/contributors", headers=self._header)
            self._raw_data = copy.copy(r.text)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self._api_call_count += 1

            if r.ok:
                data = [{"contributor_id": cid, "contributor_name": con} for cid, con in json.loads(r.text)]
                self._result = {"code": 0, "message": f"{r.status_code}"}
                self._error = False
            else:
                data = []
                self._result = {"code": -1, "message": f"{r.status_code}"}
                self._error = True
            self._contributors = data
        except Exception as e:
            self._result = {"code": -1, "message": str(e)}
            self._error = True
            return

        return data

    def get_contributors_active_count(self) -> int:
        """Returns the number of active contributors.

        Returns
        -------
        active_count: int
           Number of active contributors
        """
        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self._url}/api/contributors/active_count", headers=self._header)
            self._raw_data = copy.copy(r.text)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self._api_call_count += 1
            if r.ok:
                data = int(json.loads(r.text)["count"])
                self._result = {"code": 0, "message": f"{r.status_code}"}
                self._error = False
            else:
                data = -1
                self._result = {"code": -1, "message": f"{r.status_code}"}
                self._error = True
            self.countries_active_count = data
        except Exception as e:
            self._result = {"code": -1, "message": str(e)}
            self._error = True
            return
        return data

    def get_facility(self, osh_id: str, return_extended_fields: bool = False) -> dict:
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
            |has_approved_claim             | Flag indicating if facility has been          | bool  |
            |                               |                                               |       |
            |                               | claimed by owner, manager, or                 |       |
            |                               |                                               |       |
            |                               | other authorised person                       |       |
            +-------------------------------+-----------------------------------------------+-------+
            |is_closed                      | Flag indicating if facility has been          | bool  |
            |                               |                                               |       |
            |                               | closed (*True*), or is currently open         |       |
            |                               |                                               |       |
            |                               | (*False*)                                     |       |
            +-------------------------------+-----------------------------------------------+-------+
            | Additional fields returned when *return_extended_fields=True*                         |
            +-------------------------------+-----------------------------------------------+-------+
            | other_names                   | Other names provided, joined with             | str   |
            |                               |                                               |       |
            |                               | vertical bar ``|``                            |       |
            +-------------------------------+-----------------------------------------------+-------+
            | other_addresses               | Other facility addresses, joined with         | str   |
            |                               |                                               |       |
            |                               | vertical bar ``|``                            |       |
            +-------------------------------+-----------------------------------------------+-------+
            | contributors                  | vertical bar ``|`` joined contributors        | str   |
            |                               |                                               |       |
            |                               | who provided data                             | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | claim_info                    | Who claimed the facility                      | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | other_locations               |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | activity_reports              |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | contributor_fields            |                                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
            | has_inexact_coordinates       | Geocoordinates manually entered               | bool  |
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
            | created_from                  | Information about first record                | str   |
            |                               |                                               |       |
            |                               | which created entry                           |       |
            +-------------------------------+-----------------------------------------------+-------+
            | sector                        | Business sector                               | str   |
            +-------------------------------+-----------------------------------------------+-------+
        """
        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self._url}/api/facilities/{osh_id}/", headers=self._header)
            self._raw_data = copy.copy(r.text)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self._api_call_count += 1
            if r.ok:
                data = json.loads(r.text)
                self._result = {"code": 0, "message": f"{r.status_code}"}

                entry = {
                    "id": data["id"],
                    "lon": data["geometry"]["coordinates"][0],
                    "lat": data["geometry"]["coordinates"][1]
                }
                for k, v in data["properties"].items():
                    if k.startswith("ppe_") or k == "new_os_id":
                        continue
                    elif isinstance(v, list):
                        if len(v) > 0 and isinstance(v[0], dict):
                            lines = []
                            for vv in v:
                                lines.append("|".join([f"{kkk}:{vvv}" for kkk, vvv in vv.items()]))
                            entry[k] = "\n".join(lines).replace("lng:", "lon:")
                        else:
                            entry[k] = "\n".join(v)
                    elif k == "extended_fields" and return_extended_fields:
                        for kk in v.keys():
                            lines = []
                            for vv in v[kk]:
                                lines.append("|".join([f"{kkk}:{vvv}" for kkk, vvv in vv.items()]))
                            entry[f"{kk}_extended"] = "\n".join(lines).replace("lng:", "lon:")
                    elif k == "created_from":
                        self.v = v.copy()
                        entry[k] = "|".join([f"{kkk}:{vvv}" for kkk, vvv in v.items()])
                    elif k == "extended_fields" and not return_extended_fields:
                        pass
                    else:
                        if v is not None:
                            entry[k] = v
                        else:
                            entry[k] = ""

                data = entry.copy()
                self._error = False
            else:
                data = {}
                self._result = {"code": -1, "message": f"{r.status_code}"}
                self._error = True
        except Exception as e:
            self._result = {"code": -1, "message": str(e)}
            self._error = True
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
            r = requests.get(f"{self._url}/api/facilities/count", headers=self._header)
            self._raw_data = copy.copy(r.text)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self._api_call_count += 1
            if r.ok:
                data = int(json.loads(r.text)["count"])
                self._result = {"code": 0, "message": f"{r.status_code}"}
                self._error = False
            else:
                data = -1
                self._result = {"code": -1, "message": f"{r.status_code}"}
                self._error = True
            self.countries_active_count = data
        except Exception as e:
            self._result = {"code": -1, "message": str(e)}
            self._error = True
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
           |parent_company    | Name of parent company as uploaded                 | str         |
           +------------------+----------------------------------------------------+-------------+
        """

        try:
            self.last_api_call_epoch = time.time()
            r = requests.get(f"{self._url}/api/parent-companies/", headers=self._header)
            self._raw_data = copy.copy(r.text)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self._api_call_count += 1
            if r.ok:
                data = [{"key_or_contributor": k, "parent_company": p} for k, p in json.loads(r.text)]
                self._result = {"code": 0, "message": f"{r.status_code}"}
                self._error = False
            else:
                data = []
                self._result = {"code": -1, "message": f"{r.status_code}"}
                self._error = True
            self.parent_companies = data
        except Exception as e:
            self._result = {"code": -1, "message": str(e)}
            self._error = True
            return []

        return data

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
        request_url = f"{self._url}/api/facilities-downloads/"
        alldata = []

        while have_next:
            try:
                self.last_api_call_epoch = time.time()
                r = requests.get(request_url, headers=self._header)
                self._raw_data = copy.copy(r.text)
                self.last_api_call_duration = time.time()-self.last_api_call_epoch
                self._api_call_count += 1

                if r.ok:
                    data = json.loads(r.text)

                    for row in data["results"]["rows"]:
                        alldata.append(dict(zip(data["results"]["headers"], row)))

                    self._result = {"code": 0, "message": f"{r.status_code}"}
                    if 'next' in data.keys() and data["next"] is not None:
                        request_url = data["next"]
                    else:
                        have_next = False
                    self._error = False
                else:
                    self._result = {"code": -1, "message": f"{r.status_code}"}
                    have_next = False
                    self._error = True
                    return alldata
            except Exception as e:
                self._result = {"code": -1, "message": str(e)}
                self._error = True
                return alldata

        return alldata

    def get_contributor_embed_configs(self, contributor_id: Union[int, str]) -> list:
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
            r = requests.get(f"{self._url}/api/contributor-embed-configs/{contributor_id}/", headers=self._header)
            self._raw_data = copy.copy(r.text)
            self.last_api_call_duration = time.time()-self.last_api_call_epoch
            self._api_call_count += 1

            if r.ok:
                data = json.loads(r.text)
                alldata = {}
                num_undefined = 1
                have_undefined = False
                for k, v in data.items():
                    if k == 'embed_fields':
                        for embedded_field in v:
                            for column in ['display_name', 'visible', 'order', 'searchable']:
                                if len(embedded_field["column_name"]) == 0:  # ref https://github.com/open-apparel-registry/open-apparel-registry/issues/2200
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
                self._result = {"code": 0, "message": f"{r.status_code}"}
                self._error = False
            else:
                self._raw_data = []
                data = []
                self._result = {"code": -1, "message": f"{r.status_code}"}
                self._error = True
        except Exception as e:
            self._raw_data = []
            self._result = {"code": -1, "message": str(e)}
            self._error = True
            return

        return data

    def _flatten_facilities_json(self, json_data: dict) -> dict:
        """Convert deep facility data to a flat key,value dict.

        Internal use only.
        """
        base_entry = {}
        for k, v in json_data.items():
            if k == "matches":
                continue
            elif k == "geocoded_geometry":
                try:
                    base_entry["lon"] = v["coordinates"][0]
                    base_entry["lat"] = v["coordinates"][1]
                except Exception:
                    base_entry["lon"] = -1
                    base_entry["lat"] = -1
            else:
                if v is not None:
                    base_entry[k] = v
                else:
                    base_entry[k] = ""

        alldata = []
        if len(json_data["matches"]) > 0:
            match_no = 1
            for match in json_data["matches"]:
                new_data = {"match_no": match_no}
                new_data.update(base_entry)
                for k, v in match.items():
                    if isinstance(v, list):
                        raise NotImplementedError("Internal _flatten_facilities_json. Facilities data structure must have changed. "
                                                  "Instance 1/2. "
                                                  "Please report on github and/or check for an updated library.")
                        pass
                    elif k in ["Feature", "type"]:
                        pass
                    elif k == "geometry":
                        new_data["match_lon"] = v["coordinates"][0]
                        new_data["match_lat"] = v["coordinates"][1]
                    elif isinstance(v, dict):
                        for kk, vv in v.items():
                            if isinstance(vv, list):
                                if len(vv) == 0:
                                    new_data[f"match_{kk}"] = ""
                                else:
                                    lines = []
                                    for vvv in vv:
                                        if isinstance(vvv, dict):
                                            lines.append("|".join([f"{kkkk}:{vvvv}" for kkkk, vvvv in vvv.items()]))
                                        elif isinstance(vvv, str):
                                            lines.append(vvv)
                                    new_data[f"match_{kk}"] = "\n".join(lines).replace("lng:", "lon:")
                            elif isinstance(vv, dict):
                                for kkk, vvv in vv.items():
                                    lines = []
                                    if isinstance(vvv, str):
                                        lines = [vvv]
                                    else:
                                        for entry in vvv:
                                            if isinstance(entry, dict):
                                                lines.append("|".join([f"{kkkk}:{vvvv}" for kkkk, vvvv in entry.items()]))
                                            else:
                                                raise NotImplementedError("Internal _flatten_facilities_json. Facilities data structure must have changed. "
                                                                          "Instance 2/2. "
                                                                          "Please report on github and/or check for an updated library.")
                                    new_data[f"match_{kk}_{kkk}"] = "\n".join(lines).replace("lng:", "lon:")
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
                for k, v in new_data.items():
                    if "match_extended_fields_" in k:
                        new_data_keys_shortened[k.replace("match_extended_fields_", "match_ef_")] = v
                    else:
                        new_data_keys_shortened[k] = v

                alldata.append(new_data_keys_shortened)
                match_no += 1
        else:
            alldata.append(base_entry)

        return alldata

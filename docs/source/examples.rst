.. _examples:

Examples
========

The ``pyoshub`` API library provides python interface to the REST API, 
`available here <https://opensupplyhub.org/api/docs/>`_. 

As a general paradigm, two types of return values are provided:

- numbers of type ``int`` for queries which only return this value, e.g.

  .. code-block:: python

    number_of_active_countries = osh_api.get_countries_active_count()

- lists containing dictionaries (``dict``). These are formatted such that
  is is easily possible to convert them into a ``pandas.DataFrame``. This
  approach ensures seamless export of the resulting data frame by being
  able to export it to Office applications, or transfer the results using
  sql queries. Also, the format is similar to that returned by ``graphql``,
  a future API expansion we are considering.


Most Common (Core) Use Cases
----------------------------

The most common use cases include matching of user supplied records
for suppliers to OSH records, either to associate with OSH ID's,
or to support own deduplication efforts.



.. uml::

  @startuml
  skinparam actorStyle awesome
  left to right direction
  actor "User" as user
  package "facility records" {
    usecase "Search" as FS
    usecase "Match" as FM
    usecase "Upload" as FU
  }
  user --> FS
  user --> FM
  user --> FU
  FU --> FM
  @enduml

Facility Search
~~~~~~~~~~~~~~~

As an initial simple example, 
search for a facility with a known OS ID, this is just the intruductory example.

.. code-block:: python

   import pyoshub

   # Create connection
   osh_api = pyoshub.OSH_API()
   if osh_api.ok:
     osh_api.get_facility("IT20213143B7C4F",return_extended_fields=False)
   else:
     print(f"OSH_API returned error {osh_api.reason}")

This results in the following list to be returned, assuming valid credentials were provided. 

.. code-block:: json

  {
    "id": "IT20213143B7C4F",
    "lon": 11.1537759,
    "lat": 43.8134425,
    "name": "Alessi Luigi S.r.l.",
    "address": "Via Prunaia Loc. Maccione, Campi Bisenzio",
    "country_code": "IT",
    "os_id": "IT20213143B7C4F",
    "other_names": "",
    "other_addresses": "",
    "contributors": "id:2190|name:Fendi [Public List] (Fendi 2021 facility list)|is_verified:False|contributor_name:Fendi [Public List]|list_name:Fendi 2021 facility list",
    "country_name": "Italy",
    "claim_info": "",
    "other_locations": "",
    "is_closed": "",
    "activity_reports": "",
    "contributor_fields": "",
    "has_inexact_coordinates": false,
    "created_from": "created_at:2021-11-10T13:11:04.139764Z|contributor:Fendi [Public List]",
    "sector": "updated_at:2022-01-27T17:48:00.783691Z|contributor_id:2190|contributor_name:Fendi [Public List]|values:['Apparel']|is_from_claim:False"
  }

  
Facility matching
~~~~~~~~~~~~~~~~~

This is one of the most commonly used use cases. A locally available supplier list
needs to be checked for existing vs. new entries, may need local deduplication, or
is planned to be uploaded to Open Supply Hub.

When planning for uploads, we strongly suggest to initially run the facility matching
call setup. This way, no additional audit trail upload history record is created. We
prefer uploads primarily for known new facilities, or know changes to fields such
as facility name, address, or any other fields such as sector, product_type etc.

The overall flow of list updates from a contributor perspective is shown below.

.. uml::

  @startuml
  [*] --> facility_match
  facility_match --> MATCHED
  facility_match --> POTENTIAL_MATCH
  facility_match --> NEW_FACILITY
  
  MATCHED --> [*]
  POTENTIAL_MATCH --> upload_and_collect_matches
  upload_and_collect_matches --> review_matches
  review_matches --> CONFIRMED_MATCH
  CONFIRMED_MATCH --> [*]

  NEW_FACILITY --> direct_upload
  direct_upload --> [*]
  
  @enduml

Depending on the Open Supply Hub database content, 

- an update may not be required (MATCHED)
- an upload would result in a NEW_FACILITY record to be created
- there may be more than one potential matches, and user interaction is required to
  select the best match (POTENTIAL_MATCH)
- if the user confirms the POTENTIAL_MATCH, the newly uploaded record is assigned
  the OS ID of the matched record, and given a status of CONFIRMED_MATCH
- if the user rejects the POTENTIAL_MATCH, the newly uploaded record is assigned
  a newly created OS ID, and given a status of CONFIRMED_MATCH

To check if a record has a match in the database, the :py:meth:`~pyoshub.OSH_API.post_facilities` is
called with the ``create`` parameter being set to ``False`` (which also is its default value).

.. code-block:: python

  result = osh_api.post_facilities(
    name = "Eternal Sunshine Solar Power Ltd.",
    address = "Terrace House 13 Collins Ave PO, New Providence",
    country = "Bahamas",
    sector = "Renewable Energy",
    product_type = "Solar Panels|Wind Turbines",
    processing_type = "Assembly|Sales|Services",
    create = False,
    timeout = 15
  )

  if osh_api.ok:
    if result["status"] == "MATCHED":
      print('A match exists for the facility.')
      print(f'result[0]["os_id"]')
    elif result["status"] == "POTENTIAL_MATCH":
      print('One or more matches exists for the facility. ''
            'When uploading the data, you will need to confirm one of these matches, '
            'or reject the proposals to create a new facility.')
      match_no = 0
      for match in result["matches"]:
        match_no += 1
        print(f'Match[{match_no}]: {result[match_no]["os_id"]}\t{result[match_no]["name"]}\t{result[match_no]["address"]}')
    

Uploading new facilities, or facility changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to either upload individual records by calling :py:meth:`~pyoshub.OSH_API.post_facilities`
once per record, or use the bulk uploading method :py:meth:`~pyoshub.OSH_API.post_facilities_bulk`. The
latter allows for a list of facilities to be processed in one batch, and some convenience data
cleansing functions.

.. code-block:: python

  import pandas as pd
  import pyoshub

  df_my_facilities = pd.read_excel("my_facilities.xlsx")

  osh_api = pyoshub.OSH_API()
  if osh_api.ok:
    result = osh_api.post_facilities_bulk(
          df_my_facilities.to_dict(orient="records"),
          cleanse = True,
          auto_create = True,
          column_mapping = {"street and city":"address","supplier":"name","iso_2":"country"},
        )
    if osh_api.ok:
      df_my_mapped_facilities = pd.DataFrame(result)
      df_my_mapped_facilities.to_excel("my_mapped_facilities.xlsx",index=False)

The above code does multiple things:

- It checks for matches of each facility contained in the Excel file, and uploads facilities
  for which no match could be found (``auto_create=True``)
- Columns which are present in the original file, such as internal identifiers, will
  remain in the result 
- The cell contents will be cleansed by removing ``N/A``, multiple space characters, and
  commas, and combinations thereof (``cleanse=True``)
- Columns will be renamed as specified in the column_mapping dict. So, if the original
  file was called

  +----------+-----------------+-------+
  | supplier | street and city | iso_2 |
  +==========+=================+=======+
  | ...      | ...             | ...   |
  +----------+-----------------+-------+

  it will be renamed prior to upload such that the table appears to be called

  +----------+-----------------+-------+
  | name     | address         |country|
  +==========+=================+=======+
  | ...      | ...             | ...   |
  +----------+-----------------+-------+



Managing Facility Record changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. uml::

  @startuml
  skinparam actorStyle awesome
  left to right direction
  actor "User" as user
  package "facility status" {
    usecase "Open or Closed" as FOC
    usecase "Asccoiate" as FA
  }
  user --> FOC
  user --> FA
  @enduml



Reference Data Use Cases
------------------------


Advanced and Extended Use Cases
-------------------------------


Additional Information Use Cases
--------------------------------



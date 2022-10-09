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

Most Common Use Cases
---------------------

This is text

.. uml::

  @startuml
  skinparam actorStyle awesome
  left to right direction
  actor "User" as user
  package pyoshub {
    usecase "Search" as FS
    usecase "Match" as FM
    usecase "Upload" as FU
  }
  user --> FS
  user --> FM
  user --> FU
  @enduml

Facility Search
---------------

As an initial simple example, 
search for a facility with a known OS ID, this is just the intruductory example.

.. code-block:: python

   import pyoshub

   # Create connection
   osh_api = pyoshub.OSH_API()
   osh_spi.get_facility("IT20213143B7C4F",return_extended_fields=False)

This results in the following list to be returned. 

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
-----------------

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
  review_matches --> [*]

  NEW_FACILITY --> direct_upload
  direct_upload --> [*]
  
  @enduml

Depending on the Open Supply Hub database content, 

- an update may not be required (MATCHED)
- an upload would result in a NEW_FACILITY record to be created
- there may be more than one potential matches, and user interaction is required to
  select the best match (POTENTIAL_MATCH)

.. important::

  The functionality for upload_and_collect_matches is partially implemented, but
  the contributor review_matches functionality is not currently part of this package.

Uploading new facilities, or facility changes
---------------------------------------------



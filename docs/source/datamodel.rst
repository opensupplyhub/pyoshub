.. _datamodel:

Data Models and Signatures
==========================

Inputs
------
__init__
~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/__init__",
    "type": "object",
    "properties": {
      "url": {
        "type": "string"
      },
      "token": {
        "type": "string"
      },
      "path_to_env_yml": {
        "type": "string"
      },
      "url_to_env_yml": {
        "type": "string"
      },
      "check_token": {
        "type": "boolean"
      }
    }
  }

.. uml:: 

  @startuml
   class __init__ {
   url : str
   token : str
   path_to_env_yml : str
   url_to_env_yml : str
   check_token : bool
  }
  @enduml


get_contributor_embed_configs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_contributor_embed_configs",
    "type": "object",
    "properties": {
      "contributor_id": {
        "anyOf": [
          "int",
          "str"
        ]
      }
    },
    "required": [
      "contributor_id"
    ]
  }

.. uml:: 

  @startuml
   class get_contributor_embed_configs {
  contributor_id : Union[int,str]
  }
  @enduml


get_contributor_lists
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_contributor_lists",
    "type": "object",
    "properties": {
      "contributor_id": {
        "anyOf": [
          "int",
          "str"
        ]
      }
    },
    "required": [
      "contributor_id"
    ]
  }

.. uml:: 

  @startuml
   class get_contributor_lists {
  contributor_id : Union[int,str]
  }
  @enduml


get_contributor_types
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_contributor_types",
    "type": "object",
    "properties": {}
  }

.. uml:: 

  @startuml
   class get_contributor_types {
  }
  @enduml


get_contributors
~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_contributors",
    "type": "object",
    "properties": {}
  }

.. uml:: 

  @startuml
   class get_contributors {
  }
  @enduml


get_contributors_active_count
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_contributors_active_count",
    "type": "object",
    "properties": {}
  }

.. uml:: 

  @startuml
   class get_contributors_active_count {
  }
  @enduml


get_countries
~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_countries",
    "type": "object",
    "properties": {}
  }

.. uml:: 

  @startuml
   class get_countries {
  }
  @enduml


get_countries_active_count
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_countries_active_count",
    "type": "object",
    "properties": {}
  }

.. uml:: 

  @startuml
   class get_countries_active_count {
  }
  @enduml


get_facilities
~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_facilities",
    "type": "object",
    "properties": {
      "q": {
        "type": "string"
      },
      "contributors": {
        "anyOf": [
          "int",
          "list"
        ]
      },
      "lists": {
        "type": "integer"
      },
      "contributor_types": {
        "anyOf": [
          "str",
          "list"
        ]
      },
      "countries": {
        "type": "string"
      },
      "boundary": {
        "type": "object"
      },
      "parent_company": {
        "type": "string"
      },
      "facility_type": {
        "type": "string"
      },
      "processing_type": {
        "type": "string"
      },
      "product_type": {
        "type": "string"
      },
      "number_of_workers": {
        "type": "string"
      },
      "native_language_name": {
        "type": "string"
      },
      "detail": {
        "type": "boolean"
      },
      "sectors": {
        "type": "string"
      },
      "page": {
        "type": "integer"
      },
      "pageSize": {
        "type": "integer"
      }
    }
  }

.. uml:: 

  @startuml
   class get_facilities {
   q : str
   contributors : Union[int, list]
   lists : int
   contributor_types : Union[str, list]
   countries : str
   boundary : dict
   parent_company : str
   facility_type : str
   processing_type : str
   product_type : str
   number_of_workers : str
   native_language_name : str
   detail : bool
   sectors : str
   page : int
   pageSize : int
  }
  @enduml


get_facilities_count
~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_facilities_count",
    "type": "object",
    "properties": {}
  }

.. uml:: 

  @startuml
   class get_facilities_count {
  }
  @enduml


get_facilities_downloads
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_facilities_downloads",
    "type": "object",
    "properties": {}
  }

.. uml:: 

  @startuml
   class get_facilities_downloads {
  }
  @enduml


get_facilities_match_record
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_facilities_match_record",
    "type": "object",
    "properties": {
      "match_id": {
        "type": "integer"
      },
      "match_url": {
        "type": "string"
      }
    }
  }

.. uml:: 

  @startuml
   class get_facilities_match_record {
   match_id : int
   match_url : str
  }
  @enduml


get_facility
~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_facility",
    "type": "object",
    "properties": {
      "osh_id": "string",
      "return_extended_fields": {
        "type": "boolean"
      }
    },
    "required": [
      "osh_id"
    ]
  }

.. uml:: 

  @startuml
   class get_facility {
  osh_id : str
   return_extended_fields : bool
  }
  @enduml


get_facility_history
~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_facility_history",
    "type": "object",
    "properties": {
      "osh_id": "string"
    },
    "required": [
      "osh_id"
    ]
  }

.. uml:: 

  @startuml
   class get_facility_history {
  osh_id : str
  }
  @enduml


get_facility_processing_types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_facility_processing_types",
    "type": "object",
    "properties": {}
  }

.. uml:: 

  @startuml
   class get_facility_processing_types {
  }
  @enduml


get_parent_companies
~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_parent_companies",
    "type": "object",
    "properties": {}
  }

.. uml:: 

  @startuml
   class get_parent_companies {
  }
  @enduml


get_product_types
~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_product_types",
    "type": "object",
    "properties": {}
  }

.. uml:: 

  @startuml
   class get_product_types {
  }
  @enduml


get_sectors
~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_sectors",
    "type": "object",
    "properties": {}
  }

.. uml:: 

  @startuml
   class get_sectors {
  }
  @enduml


get_workers_ranges
~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/get_workers_ranges",
    "type": "object",
    "properties": {}
  }

.. uml:: 

  @startuml
   class get_workers_ranges {
  }
  @enduml


post_disassociate_facility
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/post_disassociate_facility",
    "type": "object",
    "properties": {
      "osh_id": "string"
    },
    "required": [
      "osh_id"
    ]
  }

.. uml:: 

  @startuml
   class post_disassociate_facility {
  osh_id : str
  }
  @enduml


post_facilities
~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/post_facilities",
    "type": "object",
    "properties": {
      "name": {
        "type": "string"
      },
      "address": {
        "type": "string"
      },
      "country": {
        "type": "string"
      },
      "sector": {
        "type": "string"
      },
      "data": {
        "type": "object"
      },
      "create": {
        "type": "boolean"
      },
      "public": {
        "type": "boolean"
      },
      "textonlyfallback": {
        "type": "boolean"
      },
      "timeout_secs": {
        "type": "integer"
      },
      "number_of_workers": {
        "anyOf": [
          "int",
          "str"
        ]
      },
      "facility_type": {
        "type": "string"
      },
      "processing_type": {
        "type": "string"
      },
      "product_type": {
        "type": "string"
      },
      "parent_company_name": {
        "type": "string"
      },
      "native_language_name": {
        "type": "string"
      }
    }
  }

.. uml:: 

  @startuml
   class post_facilities {
   name : str
   address : str
   country : str
   sector : str
   data : dict
   create : bool
   public : bool
   textonlyfallback : bool
   timeout_secs : int
   number_of_workers : Union[int, str]
   facility_type : str
   processing_type : str
   product_type : str
   parent_company_name : str
   native_language_name : str
  }
  @enduml


post_facilities_bulk
~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/post_facilities_bulk",
    "type": "object",
    "properties": {
      "records": {
        "type": "array"
      },
      "cleanse": {
        "type": "boolean"
      },
      "auto_create": {
        "type": "boolean"
      }
      "column_mapping": {
        "type": "object"
      }
    },
    "required": [
      "records"
    ]
  }

.. uml:: 

  @startuml
   class post_facilities_bulk {
   records : list
   cleanse : bool
   auto_create : bool
   column_mapping : dict
  }
  @enduml


post_facility_closed
~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/post_facility_closed",
    "type": "object",
    "properties": {
      "osh_id": "string",
      "reason_for_report": "string"
    },
    "required": [
      "osh_id",
      "reason_for_report"
    ]
  }

.. uml:: 

  @startuml
   class post_facility_closed {
  osh_id : str
  reason_for_report : str
  }
  @enduml


post_facility_match_confirm
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/post_facility_match_confirm",
    "type": "object",
    "properties": {
      "match_id": {
        "type": "integer"
      },
      "match_url": {
        "type": "string"
      }
    }
  }

.. uml:: 

  @startuml
   class post_facility_match_confirm {
   match_id : int
   match_url : str
  }
  @enduml


post_facility_match_reject
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/post_facility_match_reject",
    "type": "object",
    "properties": {
      "match_id": {
        "type": "integer"
      },
      "match_url": {
        "type": "string"
      }
    }
  }

.. uml:: 

  @startuml
   class post_facility_match_reject {
   match_id : int
   match_url : str
  }
  @enduml


post_facility_open
~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/post_facility_open",
    "type": "object",
    "properties": {
      "osh_id": "string",
      "reason_for_report": "string"
    },
    "required": [
      "osh_id",
      "reason_for_report"
    ]
  }

.. uml:: 

  @startuml
   class post_facility_open {
  osh_id : str
  reason_for_report : str
  }
  @enduml


post_facility_open_or_closed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

  {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensupplyhub/post_facility_open_or_closed",
    "type": "object",
    "properties": {
      "osh_id": "string",
      "closure_state": "string",
      "reason_for_report": "string"
    },
    "required": [
      "osh_id",
      "closure_state",
      "reason_for_report"
    ]
  }

.. uml:: 

  @startuml
   class post_facility_open_or_closed {
  osh_id : str
  closure_state : str
  reason_for_report : str
  }
  @enduml


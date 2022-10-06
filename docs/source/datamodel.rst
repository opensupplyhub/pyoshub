.. _datamodel:

Data Model
==========

contributor_embed_configs
-------------------------

Inputs
~~~~~~
JSON Schema
```````````

.. code-block:: json

   {
     "$schema": "https://json-schema.org/draft/2020-12/schema",

     "embedded_map_id": "integer"
     "width": "string"
     "height": "string"
     "color": "string"
     "font": "string"
     "contributor_id": "integer"
     "number_of_workers_display_name": "string"
     "number_of_workers_visible": "boolean"
     "number_of_workers_order": "integer"
     "number_of_workers_searchable": "boolean"
     "percent_female_workers_display_name": "string"
     "percent_female_workers_visible": "boolean"
     "percent_female_workers_order": "integer"
     "percent_female_workers_searchable": "boolean"
     "type_of_facility_display_name": "string"
     "type_of_facility_visible": "boolean"
     "type_of_facility_order": "integer"
     "type_of_facility_searchable": "boolean"
     "type_of_product_display_name": "string"
     "type_of_product_visible": "boolean"
     "type_of_product_order": "integer"
     "type_of_product_searchable": "boolean"
     "percent_migrant_workers_display_name": "string"
     "percent_migrant_workers_visible": "boolean"
     "percent_migrant_workers_order": "integer"
     "percent_migrant_workers_searchable": "boolean"
     "parent_company_display_name": "string"
     "parent_company_visible": "boolean"
     "parent_company_order": "integer"
     "parent_company_searchable": "boolean"
     "tier_display_name": "string"
     "tier_visible": "boolean"
     "tier_order": "integer"
     "tier_searchable": "boolean"
     "undefined_1_display_name": "string"
     "undefined_1_visible": "boolean"
     "undefined_1_order": "integer"
     "undefined_1_searchable": "boolean"
     "product_type_display_name": "string"
     "product_type_visible": "boolean"
     "product_type_order": "integer"
     "product_type_searchable": "boolean"
     "facility_type_display_name": "string"
     "facility_type_visible": "boolean"
     "facility_type_order": "integer"
     "facility_type_searchable": "boolean"
     "processing_type_display_name": "string"
     "processing_type_visible": "boolean"
     "processing_type_order": "integer"
     "processing_type_searchable": "boolean"
     "prefer_contributor_name": "boolean"
     "contributor_name": "string"
     "text_search_label": "string"
     "map_style": "string"
     "extended_fields_0": "string"
     "extended_fields_1": "string"
   }

Return Values
~~~~~~~~~~~~~

Class Diagram
`````````````

.. uml:: 
   
   @startuml
   class contributor_list {
   }
   @enduml

contributor_lists
-----------------

Inputs
~~~~~~

JSON Schema
```````````

.. code-block:: json

   {
     "$schema": "https://json-schema.org/draft/2020-12/schema",
     "contributor_id": {
        "anyOf": [
            {
                "type": "integer"
            },
            {
                "type":"string",
                "minLength": 1,
                "maxLength": 200
            }
        ]
   }



Return Values
~~~~~~~~~~~~~

JSON-LD
```````

.. code-block:: json

   {
     "@context": {
       "@vocab": "https://json-ld.opensupplyhub.org/contexts/contributor_list.jsonld",
       "list_id": "ContributorListID",
       "list_name": "ContributorListName"
     }
   }

Class Diagram
`````````````

.. uml:: 
   
   @startuml
   class contributor_list {
     list_id : int 
     list_name : str
   }
   @enduml
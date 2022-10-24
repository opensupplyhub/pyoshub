.. image:: https://images.squarespace-cdn.com/content/v1/628fa7cfd0b20d628a9b2b35/56e6e587-57b7-40ff-bdd2-79158e66eacf/OSH_Logo.png?format=1500w

Welcome to pyoshub's documentation!
===================================

Quickstart
----------

For installation, run.

.. code-block:: shell

   pip install pyoshub


In python, import the module, set up the API connection, and then use the various calls as required.

.. code-block:: python

   from pyoshub import OSH_API

   ...

   osh_api = OSH_API(token="<your token>")
   if osh_api.ok:
      print(osh_api.get_sectors())
   else:
      print(f"Error: {osh_api.reason}")

Head over to :doc:`Examples </examples>`\, or the :doc:`API documentation </doc>` for more details. 

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   doc
   authentication
   examples
   datamodel


Use Case Mapping to REST Endpoints
----------------------------------

Not all API endpoints are similarly simportant or address common use cases. 

* core API endpoints will be used most commonly to match addresses and upload data
* reference endpoints provide access to data that should be used, if possible, such as country, or sector names
* extended endpoints are for more specific use cases, such as changing facility open/close use cases
* info endpoints may be of less interest to most
* internal endpoints may be retired as there may not be a good use case for most



.. table::
   
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | endpoint                                      | verb  | level      | method                                                  |
    +===============================================+=======+============+=========================================================+
    | ``/facilities/``                              | GET   | core       | :py:meth:`~pyoshub.OSH_API.get_facilities`              |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/facilities/``                              | POST  | core       | :py:meth:`~pyoshub.OSH_API.post_facilities`             |
    |                                               |       |            |                                                         |
    |                                               |       |            | :py:meth:`~pyoshub.OSH_API.post_facilities_bulk`        |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/facility-matches/{id}/confirm/``           | POST  | core       | :py:meth:`~pyoshub.OSH_API.post_facility_match_confirm` |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/facility-matches/{id}/reject/``            | POST  | core       | :py:meth:`~pyoshub.OSH_API.post_facility_match_reject`  |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/contributor-types/``                       | GET   | reference  | :py:meth:`~pyoshub.OSH_API.get_contributor_types`       |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/countries/``                               | GET   | reference  | :py:meth:`~pyoshub.OSH_API.get_countries`               |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/countries/active_count/``                  | GET   | reference  | :py:meth:`~pyoshub.OSH_API.get_countries_active_count`  |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/facility-processing-types/``               | GET   | reference  |:py:meth:`~pyoshub.OSH_API.get_facility_processing_types`|
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/product-types/``                           | GET   | reference  | :py:meth:`~pyoshub.OSH_API.get_product_types`           |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/sectors/``                                 | GET   | reference  | :py:meth:`~pyoshub.OSH_API.get_sectors`                 |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/workers-ranges/``                          | GET   | reference  | :py:meth:`~pyoshub.OSH_API.get_workers_ranges`          |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/facilities/{id}/dissociate/``              | POST  | extended   | .. NOTE:: implementation deferred                       |
    +-----------------------------------------------+-------+------------+                                                         +
    | ``/facilities/{id}/history/``                 | GET   | extended   |                                                         |
    +-----------------------------------------------+-------+------------+                                                         +
    | ``/facilities/{id}/report/``                  | POST  | extended   |                                                         |
    +-----------------------------------------------+-------+------------+                                                         +
    | ``/facility-activity-reports/``               | GET   | extended   |                                                         |
    +-----------------------------------------------+-------+------------+                                                         +
    | ``/facility-activity-reports/{id}/approve/``  | POST  | extended   |                                                         |
    +-----------------------------------------------+-------+------------+                                                         +
    | ``/facility-activity-reports/{id}/reject/``   | POST  | extended   |                                                         |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/contributor-lists/``                       | GET   | info       | :py:meth:`~pyoshub.OSH_API.get_contributor_lists`       |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/contributors/``                            | GET   | info       | :py:meth:`~pyoshub.OSH_API.get_contributors`            |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/contributors/active_count/``               | GET   | info       |:py:meth:`~pyoshub.OSH_API.get_contributors_active_count`|
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/facilities/{id}/``                         | GET   | info       | :py:meth:`~pyoshub.OSH_API.get_facility`                |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/facilities/count/``                        | GET   | info       | :py:meth:`~pyoshub.OSH_API.get_facilities_count`        |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/parent-companies/``                        | GET   | info       | :py:meth:`~pyoshub.OSH_API.get_parent_companies`        |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/facilities-downloads/``                    | GET   | internal   | :py:meth:`~pyoshub.OSH_API.get_facilities_downloads`    |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/facility-matches/{id}/``                   | GET   | internal   | .. NOTE:: implementation deferred                       |
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+
    | ``/contributor-embed-configs/{id}/``          | GET   | internal   |:py:meth:`~pyoshub.OSH_API.get_contributor_embed_configs`|
    +-----------------------------------------------+-------+------------+---------------------------------------------------------+




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

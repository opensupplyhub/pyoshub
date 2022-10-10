.. image:: https://images.squarespace-cdn.com/content/v1/628fa7cfd0b20d628a9b2b35/56e6e587-57b7-40ff-bdd2-79158e66eacf/OSH_Logo.png?format=1500w

Welcome to pyoshub's documentation!
===================================

Not all API endpoints are similarly simportant or address common use cases. 

* core API endpoints will be used most commonly to match addresses and upload data
* reference endpoints provide access to data that should be used, if possible, such as country, or sector names
* extended endpoints are for more specific use cases, such as changing facility open/close use cases
* info endpoints may be of less interest to most
* internal endpoints may be retired as there may not be a good use case for most

.. table:: 
   
   +--------------------------------------------+-------+------------+
   | endpoint                                   | verb  | level      |
   +============================================+=======+============+
   |  /facilities/                              | GET   | core       |
   |  /facilities/                              | POST  | core       |
   |  /facility-matches/{id}/                   | GET   | core       |
   |  /facility-matches/{id}/confirm/           | POST  | core       |
   |  /facility-matches/{id}/reject/            | POST  | core       |
   |  /contributor-types/                       | GET   | reference  |
   |  /countries/                               | GET   | reference  |
   |  /countries/active_count/                  | GET   | reference  |
   |  /facility-processing-types/               | GET   | reference  |
   |  /product-types/                           | GET   | reference  |
   |  /sectors/                                 | GET   | reference  |
   |  /workers-ranges/                          | GET   | reference  |
   |  /facilities/{id}/dissociate/              | POST  | extended   |
   |  /facilities/{id}/history/                 | GET   | extended   |
   |  /facilities/{id}/report/                  | POST  | extended   |
   |  /facility-activity-reports/               | GET   | extended   |
   |  /facility-activity-reports/{id}/approve/  | POST  | extended   |
   |  /facility-activity-reports/{id}/reject/   | POST  | extended   |
   |  /contributor-lists/                       | GET   | info       |
   |  /contributors/                            | GET   | info       |
   |  /contributors/active_count/               | GET   | info       |
   |  /facilities/{id}/                         | GET   | info       |
   |  /facilities/count/                        | GET   | info       |
   |  /parent-companies/                        | GET   | info       |
   |  /facilities-downloads/                    | GET   | internal   |
   |  /contributor-embed-configs/{id}/          | GET   | internal   |
   +--------------------------------------------+-------+------------+


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   doc
   authentication
   examples
   datamodel

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

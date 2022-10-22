Documentation
=============

Introduction
------------

All class methods/library functions calling the `Open Supply Hub <https://opensupplyhub.org>`_ API
return ``lists`` of python ``dicts``. These can readily be converted into a ``pandas.DataFrame``.

.. _facility_upload_lifecycle:

Facility Upload Lifecycle
-------------------------

At the heart of the Open Supply Hub database are facilities, and the way they are being matched to
geolocations, and, possibly, multiple successfive submissions. For API users, the most relevant
lifecycle is that of matching, or creating facilities.

.. uml:: 
   
   @startuml
    [*] --> post_facilities
    post_facilities --> wait
    post_facilities --> POTENTIAL_MATCH
    post_facilities --> NEW_FACILITY
    post_facilities --> MATCHED
    post_facilities --> ERROR

    POTENTIAL_MATCH --> PENDING
    PENDING --> CONFIRMED : post_facility_match_confirm()
    PENDING --> REJECTED : post_facility_match_reject()
    wait --> wait
    wait --> POTENTIAL_MATCH
    wait --> NEW_FACILITY
    wait --> MATCHED
    wait --> ERROR
    wait --> TIMEOUT

    CONFIRMED --> [*]
    REJECTED --> [*]
    MATCHED --> [*]
    NEW_FACILITY --> [*]
    ERROR --> [*]
    TIMEOUT --> [*]

   @enduml

Each contribution has a unique numeric identifier, and, once matched, or created, will also have the
unique `OS_ID`.


Upload (POST) Request Throttling
--------------------------------

Uploads need to be processed before they can be checked for existing record matches. This is a rather time
consuming process, and, while care has been taken to architect and build a system which can cope with
varying load, we have decided to add a rate limit to API uploads.

Rate limits are configured by the Openshupplyhub team.

For *uploads*, the following return codes can be expected:

* 200 (``http OK``) for a record which was uploaded, and a match was found (``MATCHED``), or matches are suggested (``POTENTIAL_MATCH``)
* 201 (``http CREATED``) for a record for which a new facility was created (``NEW_FACILITY``)
* 429 (``http Too Many Requests``) when the rate limit was exceeded. In this case, the API will return a JSON like ``{'detail': 'Request was throttled. Expected available in 23 seconds.'}``

All pyoshub upload/post methods will, once encuntering a 429 return code, wait for the specfied amount of 
seconds before attempting another request. If the total amount of time exceeds a defined ``timeout``, the 
method aborts and returns an error code.


Module documentation
--------------------

.. automodule:: pyoshub
    :members: OSH_API
    :inherited-members:

.. comment autoclass:: pyoshub.OSH_API



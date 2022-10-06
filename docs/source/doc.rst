Documentation
=============

Introduction
------------

All class methods/library functions calling the `Open Supply Hub <https://opensupplyhub.org>`_ API
return ``lists`` of python ``dicts``. These can readily be converted into a ``pandas.DataFrame``.

Facility Lifecycle
------------------

At the heart of the Open Supply Hub database are facilities, and the way they are being matched to
geolocations, and, possibly, multiple successfive submissions. For API users, the most relevant
lifecycle is that of matching, or creating facilities.

.. uml:: 
   
   @startuml
   [*] --> post_facilities
    post_facilities --> POTENTIAL_MATCH
    post_facilities --> NEW_FACILITY
    post_facilities --> MATCHED
    post_facilities --> ERROR

    POTENTIAL_MATCH --> PENDING
    PENDING --> CONFIRMED : /facility-matches/{id}/confirm/
    PENDING --> REJECTED : /facility-matches/{id}/confirm/

    CONFIRMED --> [*]
    REJECTED --> [*]
    MATCHED --> [*]
    NEW_FACILITY --> [*]
    ERROR --> [*]
   @enduml

Each contribution has a unique numeric identifier, and, once matched, or created, will also have the
unique `OS_ID`.


Module documentation
--------------------

.. automodule:: pyoshub
    :members: OSH_API
    :inherited-members:

.. comment autoclass:: pyoshub.OSH_API



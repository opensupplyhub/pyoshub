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

Facility Search
---------------

Search for a facility with a known OS ID, this is just the intruductory example.

.. code-block:: python

   import pyoshub

   # Create connection
   osh_api = pyoshub.OSH_API()

Facility matching
-----------------

This is one of the most commonly used use cases

Uploading new facilities, or facility changes
---------------------------------------------



Authentication
==============

Access to the `Open Supply Hub API <https://opensupplyhub.org>`_ requires an access token. You can 
create, view (copy), or re-create yours from the `Setting page "Token" tab at <https://openapparel.org/settings>`_.

.. warning::
    Never include credentials of any form in your source code, not even for debugging. Once
    you decide to share your code, or upload it to public repositories, such as github, 
    or gitlab, they will easily leak to others. 
    
    Even removing them from the code will not remove them from a prior version if you use
    a config management system, and can be retrieved in the future.

    Please recreate your token from `setting page "Token" tab at <https://openapparel.org/settings>`_ after
    you inadvertenly used this token in your code. 

We support four methods of supplying the token, one is, supplying it as a parameter when creating an `OSH_API` object,
one is to supply is as part of a setting, or environment file, one is accepting a file via an URL, 
and lastly via setting it via an environment variable.

The latter is mostly likely the method of choice when using containers, or running managed services, where they may be
called secrets.

Supply as parameter
-------------------

As stated above, when using a configuration management tool, supplying credentials in source code
may cause these credentials to become visible to others.

Basic Example
`````````````

.. code-block:: python
   
   import pyoshub

   osh_api = pyoshub.OSH_API(token='a584abce2b159c4d8cf88eac3a26fbe3b1a13b8e')
  
Supply different URL
````````````````````

Supplying a different endpoint could be useful when using proxy servers, development environments, or
local installations. 

.. code-block:: python
   
   import pyoshub

   osh_api = pyoshub.OSH_API(url='https://proxyse.example.com/?url=https://opensupplyhub.org')



Supply as part of an .env.yml file
----------------------------------

The ``OSH-API`` initialisation will look for either a file path given in ``path_to_env_yml``, or look for
a file named ``.env.yml`` in its current folder. This file can contain entries for either, or both,
the url to contact, and the authentication token.

.. code-block:: python
   
   import pyoshub

   osh_api = pyoshub.OSH_API(path_to_env_yml='../../credentials/env.yaml')


.. code-block:: yaml

    OSH_URL: https://opensupplyhub.org
    OSH_TOKEN: 12345abcdef12345abcdef12345abcdef


Supply as part of an URL
------------------------

In addition to providing an ``.env.yml`` via a file system, the ``OSH-API`` initialisation also
accepts providing this file via a URL. This file can contain entries for either, or both,
the url to contact, and the authentication token.

.. code-block:: python
   
   import pyoshub

   osh_api = pyoshub.OSH_API(url_to_env_yml='https://configserver.cluster.local/pyoshubub/env.yaml')


.. code-block:: yaml

    OSH_URL: https://opensupplyhub.org
    OSH_TOKEN: 12345abcdef12345abcdef12345abcdef


Supply via an environment variable
----------------------------------

Lastly, the ``OSH-API`` initialisation checks for the existence of environment variables
``OSH_URL`` and ``OSH_TOKEN``. These can be set via shell configuration, or, for
containers or kubernetes pods, as environment variables. Some managed cloud services
will also allow setting these values securely.

Order of precedence
-------------------

These settings will be evaluate in the following sequence:

- Environment variables will always be considered, if present, else,
- an explicit path to an ``.env.yml`` file, else
- a URL providing an ``.env.yml`` file
- a local file ``.env.yml`` 

.. hint::

   When providing file paths and names, or URLs, the file name can obviously be different from ``.env.yml`` 

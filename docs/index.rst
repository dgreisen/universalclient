Universal Client
================
Python 2 and Python 3 Compatible

| Docs: https://universal-client.readthedocs.org  
| Repository: https://github.com/dgreisen/universalclient  
| PyPI: https://pypi.python.org/pypi/UniversalClient


Universal Client is an `Apache 2 <http://www.apache.org/licenses/LICENSE-2.0.html>`_ licensed client for quickly and easily interacting with any REST api.
Universal Client is compatible with Python 2 and Python 3.

You want to use a cool api, but the python client doesn't exist, or is out of date, or doesn't support the feature you want to use.
So you start making raw HTTP requests. 
But, even with the `best http library <http://docs.python-requests.org/en/latest/index.html>`_, passing in the right URL and options for every call is error prone and quickly becomes cumbersome for anything more than trivial scenarios.

The Universal Client is a wrapper around the excellent `Requests <http://docs.python-requests.org/en/latest/index.html>`_ HTTP library.
A Client instance corresponds to a single endpoint in the api.
Use dot notation to navigate the api paths. You can set any Requests parameters on a client instance and all child instances will inherit those parameters.

A quick example::

   >>> from universalclient import Client
   # create a client pointing to google
   >>> google = Client("http://google.com")
   # set a google cookie so we get "personalized" results (Yay!)
   >>> google = google.cookies(gv="5d41402abc4b2a76b9719d911017c592")
   # get the google home page at http://google.com
   >>> resp = google.get()
   # create an end point to google images, which inherits the cookies
   >>> images = google.images
   # get google site at http://google.com/images
   >>> resp = images.get()


The Client stores a complete api call.
It is immutable - any modification returns a new client.
This allows you to reuse endpoints over and over.

Contents:

.. toctree::
   :maxdepth: 2

   basics
   advanced


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Basics
======

Creating a URL
--------------

UniversalClient is a wrapper around the excellent `Requests <http://docs.python-requests.org/en/latest/index.html>`_ library for making HTTP requests.
Lets create a client for a fictitious photo sharing service::

   >>> from universalclient import Client
   # create a client pointing to myImages.com
   >>> Client("http://myImages.com")
   get: http://myImages.com

A client object is returned.
In this case, the client object points to the URL "http://myImages.com" and has defaulted to the "get" HTTP method.
We can add to this base URL using dot notation.
Getting an attribute on the client will return a new Client with the name of that attribute appended to the initial Client's URL::

	>>> Client("http://myImages.com").images
	get: http://myImages.com/user

Clients are immutable::

	>>> root = Client("http://myImages.com").images
	>>> davidsImages = root.user.dgreisen
	>>> root
	get: http://myImages.com
	>>> davidsImages
	get: http://myImages.com/user/dgreisen

Making requests
---------------

You can make the default request by calling client.request(), which returns a Requests response object.
You can make a specific type of request by calling that function::

	>>>
	# make the default get request
	>>> davidsImages.request()	
	<Response [200]>
	# make a head request
	>>> davidsImages.head()
	<Response [200]>

Arguments
---------

Any keyword argument available for Requests.request can be set on your client.
You can do this when a client is created, any time after creation, or just before sending the request.
Any kwargs passed to Client(), client.request(), client.get(), or any other client.<HTTP-METHOD>(), will be passed directly to request.request(),


At creation::

	>>> root = Client("http://myImages.com", auth=('user', 'pass'), method="get", params={"api_key":"123"})

Updating any client after initial creation::

	>>> uploadImage = root.user.dgreisen.images.method("put").params(size="full")

Just before sending the request::

	>>> uploadImage.request(files={'file': open('birthdayBash.jpg', 'rb'))
	<Response [200]>

You can display all the arguments::

	>>> uploadImage.getArgs()
	{'_http': <module 'requests' from '/usr/local/lib/python2.7/dist-packages/requests/__init__.pyc'>, 'params': {'api_key': '123', 'size': 'full'}, 'method': 'put', 'auth': ('user', 'pass'), '_path': ['http://myImages.com', 'user', 'dgreisen', 'images']}

You will notice there are a couple of other keys/values in there starting with an underscore.
Underscore keys are not passed to requests.request(). 
You can read about some of them in the :doc:`advanced` section.
You will also notice that the params object was updated with the new keys rather than being replaced by the new keys.
Args that are dictionaries are updated rather than replaced.

If you set an argument that already has a value, it will be overridden.
You can also delete an existing value::

	>>> getAllImages = uploadImage.method()

	>>> "method" in getAllImages.getArgs()
	False

No error will be thrown if an argument to be deleted does not exist.

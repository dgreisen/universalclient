Advanced
========

Creating a URL
--------------

The URL we created in :doc:`basics` section::

	>>> root = Client("http://myImages.com").images
	>>> davidsImages = root.user.dgreisen

is great if we know we are going to do a bunch of stuff to davidsImages.
But what if we want to be able to pass in a userid that isn't known until runtime?
That's when the _ (underscore) method is used.
The argument to _ will be added to the URL, just as if it were appended with dot notation::

	>>> somebody = "jsmith"
	>>> somebodysImages = root.user._(somebody)
	>>> somebodysImages
	get: http://myImages.com/images/user/jsmith

Even better, the string passed to _ can be formatted with all the args passed to a request() (or get(), post(), etc.).
Thus, we can make an endpoint for adding an arbitrary image to an arbitrary users album::

	>>> addImage = root.user._({}).images._({1}).method("put")
	>>> addImage.request("dgreisen", "birthdayBash", files={'file': open('birthdayBash.jpg', 'rb'))
	<Response [200]>
	>>> addImage.request("jsmith", "birthdayBash", files={'file': open('birthdayBash.jpg', 'rb'))
	<Response [200]>

You can only use positional arguments to format the string since the keyword arguments are passed to requests.request().
All arguments are passed to each string, so if you have multiple strings appended with _, you must use positional args properly.

Data formatting
---------------

Sometimes the data you need to send to a specific endpoint has to be formatted in a specific way.
You can perform this manipulation by adding a dataFilter.
A dataFilter is a function that takes one argument, the data, and returns a single value, the data to be sent to the server.
Data will be transformed just before it is sent in the request.

UniversalClient currently comes with one dataFilter built in, jsonFilter, which encodes the data as json::

	>>> from universalclient import jsonFilter
	>>> response = root.user.jdoe.put(data={"name": "Jane Doe", "email": "jdoe@example.com"}, dataFilter=jsonFilter)
	>>> response.request.body
	'{"name": "Jane Doe", "email": "jdoe@example.com"}'

If you write a dataFilter that you think others would find useful, please submit a pull request.

Oauth
-----

Because UniversalClient is just Requests at heart, you can use `Rauth <https://github.com/litl/rauth>`_ for oauth authentication.
To use, create a fully authenticated Rauth client (see `Rauth documentation <https://rauth.readthedocs.org/en/latest/>`_).
Then pass the fully authenticated client into your universal client::

	>>> root = Client("http://myImages.com").oauth(rauth_client).images

The client then uses the rauth client to make requests, rather than a default Requests instance.
Please note, this functionality has not been tested. Tests and bug reports are welcome.
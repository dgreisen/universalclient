import requests
from copy import deepcopy
import json


class Client(object):
    methods = ("get", "post", "put", "delete", "head", "options", "trace", "connect")

    def __init__(self, url="", oauth=None, **kwargs):
        _getattr = super(Client, self).__getattribute__
        self._attributes = attributes = {
            "_path": [url],
            "method": "get",
        }
        # we don't store http/oauth client in _attributes b/c don't want it deepcloned
        http = kwargs.pop("_http", requests)
        self._http = oauth or http
        method = kwargs.pop("method", "GET")
        attributes["method"] = method.lower()
        attributes.update(kwargs)

    def __getattribute__(self, name):
        _getattr = super(Client, self).__getattribute__
        attributes = _getattr("_attributes")
        attributes = deepcopy(attributes)
        attributes["_path"].append(name)
        attributes["oauth"] = _getattr("_http")
        return Client(**attributes)

    def __repr__(self):
        _getattr = super(Client, self).__getattribute__
        attributes = _getattr("_attributes")
        return "%s: %s" % (attributes["method"], self._getUrl())

    def __call__(self, *args, **kwargs):
        _getattr = super(Client, self).__getattribute__
        attributes = _getattr("_attributes")
        calledAttr = attributes["_path"].pop()

        # handle a method call (ie GET, POST)
        methods = _getattr("methods")
        if calledAttr.lower() in methods:
            # create new client with updated method, and call it
            return self.setArgs(method=calledAttr.lower()).request(*args, **kwargs)

        return _getattr(calledAttr)(*args, **kwargs)

    def request(self, *args, **kwargs):
        """
        make a request to the server. Any kwargs passed to request will override the
        attributes passed to requests.request.

        calls the function at dataFilter with the contents of the data
        attribute iff dataFilter and data exist

        runs the url through format (http://docs.python.org/2/library/string.html#formatspec)
        passing as arguments any *args passed to request.
        """
        # update with any last-minute modifications to the attributes
        c = self.setArgs(**kwargs) if kwargs else self
        attributes = c._cloneAttributes()
        requests = attributes.pop("_http")

        # run the data through the dataFilter if both exist
        if "data" in attributes and "dataFilter" in attributes:
            attributes["data"] = attributes["dataFilter"](attributes["data"])

        # format and set the url
        attributes["url"] = c._getUrl().format(*args)

        # remove uneeded attributes
        for attr in ["_path", "dataFilter"]:
            attributes.pop(attr, None)

        #make the request
        return requests.request(**attributes)

    def oauth(self, rauth):
        """
        provide a fully authenticated rauth oauth client
        """
        return self.setArgs(oauth=rauth)

    def getArgs(self):
        """
        return the arguments currently stored in this client object.

        >>> x = Client("example.com")
        >>> args = x.getArgs()
        >>> del args['_http'] # for testing purposes - args['_http'] different on every machine
        >>> args
        {'method': 'get', '_path': ['example.com']}

        the returned arguments are actually deep copies - cannot be used to modify the client arguments

        >>> args['method']='put'
        >>> x.getArgs()['method']
        'get'

        """
        return self._cloneAttributes()

    def setArgs(self, **kwargs):
        """
        passed kwargs will update and override existing attributes.

        >>> x = Client("example.com").setArgs(params={"first": "Jane", "last": "Jones"}, method="post")
        >>> y = x.setArgs(method="put")
        >>> y.getArgs()["method"]
        'put'
        >>> y.getArgs()["params"]
        {'last': 'Jones', 'first': 'Jane'}

        if an existing attribute is a dict, and replacement is a dict,
        then update the attribute with the new value

        >>> y = x.setArgs(params={"first": "Jim"})
        >>> y.getArgs()["params"]
        {'last': 'Jones', 'first': 'Jim'}
        """
        attributes = self._cloneAttributes()
        # update rather than replace attributes that can be updated
        for k, v in kwargs.items():
            if k in attributes and hasattr(v, "update") and hasattr(attributes[k], "update"):
                attributes[k].update(v)
                del kwargs[k]
        attributes.update(kwargs)
        return Client(**attributes)

    def delArgs(self, *args):
        """
        passed args will be deleted from the attributes hash. No error will
        throw if the attribute does not exist.
        """
        attributes = self._cloneAttributes()
        for attr in args:
            attributes.pop(attr)
        return Client(**attributes)

    def _(self, pathPart):
        """
        append a path part to the url. Should be used when the pathPart to
        append is not valid python dot notation. Can use positional, but
        not named, string formatters, ie {} or {3}, but not {name}.
        """
        attributes = self._cloneAttributes()
        attributes["_path"].append(pathPart)
        return Client(**attributes)

    def _cloneAttributes(self):
        """
        get all attributes, cloning occurrs in __getattribute__, so don't
        have to do twice
        """
        _getattr = super(Client, self).__getattribute__
        attributes = _getattr("_attributes")
        attributes["_http"] = _getattr("_http")
        return attributes

    def _getUrl(self):
        """
        get the url from _path
        """
        attributes = self._cloneAttributes()
        return "/".join(attributes["_path"])

    def __dir__(self):
        _getattr = super(Client, self).__getattribute__
        methods = _getattr("methods")
        methods += ("setArgs", "getArgs", "delArgs", "_", "oauth", "request")
        return list(methods)

jsonFilter = lambda data: json.dumps(data)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

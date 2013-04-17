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
            return self.setArgs(method=calledAttr.lower()).call(*args, **kwargs)

        return _getattr(calledAttr)(*args, **kwargs)

    def call(self, *args, **kwargs):
        """
        make a call to the server. Any kwargs passed to call will override the
        attributes passed to requests.request.

        calls the function at dataFilter with the contents of the data
        attribute iff dataFilter and data exist

        runs the url through format (http://docs.python.org/2/library/string.html#formatspec)
        passing as arguments any *args passed to call.
        """
        # update with any last-minute modifications to the attributes
        c = self.setArgs(kwargs) if kwargs else self

        attributes = c._cloneAttributes()
        requests = attributes.pop("_http")
        # remove uneeded attributes
        for attr in ["_path"]:
            attributes.pop(attr)

        # run the data through the dataFilter if both exist
        if "data" in attributes and "dataFilter" in attributes:
            attributes["data"] = attributes["dataFilter"](attributes["data"])

        # format and set the url
        attributes["url"] = c._getUrl().format(*args)
        #make the request
        return requests.request(**attributes)

    def oauth(self, rauth):
        """
        provide a fully authenticated rauth oauth client
        """
        self.setArgs(oauth=rauth)

    def getArgs(self):
        """
        return the attributes currently stored in this client object.
        """
        return self._cloneAttributes()

    def setArgs(self, **kwargs):
        """
        passed kwargs will update and override existing attributes.
        """
        attributes = self._cloneAttributes()
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

    def append(self, pathPart):
        """
        append a path part to the url. Should be used when the pathPart to
        append is not valid python dot notation. Can use positional, but
        not named, string formatters, ie {} or {3}, but not {name}.
        """
        attributes = self._cloneAttributes()
        attributes["_path"].append(pathPart)

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
        methods += ("setArgs", "getArgs", "delArgs", "append", "oauth", "call", "append")
        return list(methods)

jsonFilter = lambda data: json.dumps(data)

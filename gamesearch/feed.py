"""
    gamesearch.feed

    Feed related classes
"""
import urllib.request
import urllib.parse
import json


class FetchError(Exception):
    def __init__(self):
        pass


class JsonFeed:
    """
    Base class for json feeds.
    Child classes can override validate() to validate feed response
    """
    def __init__(self):
        self.base_url = None
        self.valid_http_status = [200]
        self.default_params = {}

    def validate(self, response):
        """
        Returns true if the response is valid, see giantbomb for an example
        """
        return True

    def fetch(self, params={}):
        """
        Fetch the feed with the provided params
        It returns a dictionary
        """
        fparams = self.default_params.copy()
        fparams.update(params)
        url = "%s/?%s" % (self.base_url, urllib.parse.urlencode(fparams))
        print (url)
        with urllib.request.urlopen(url) as f:
            if f.status not in self.valid_http_status:
                raise FetchError()
            data_json = json.loads(f.read().decode("UTF-8"))
            if not self.validate(data_json):
                raise FetchError()
            return data_json

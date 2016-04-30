import urllib.request
import urllib.parse
import json


class FetchError(Exception):
    def __init__(self):
        pass


class JsonFeed:
    def __init__(self):
        self.base_url = None
        self.valid_http_status = [200]
        self.default_params = {}

    def validate(self, response):
        return True

    def fetch(self, params={}):
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

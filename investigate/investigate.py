import requests
import json
import urlparse

class Investigate(object):
    BASE_URL = 'https://investigate.api.opendns.com/'
    DOMAIN_ERR = ValueError("domains must be a string or a list of strings")

    def __init__(self, api_key):
        self.api_key = api_key
        self._uris = {
            "categorization": "domains/categorization/",
        }
        self._auth_header = {"Authorization": "Bearer " + self.api_key}

    def get(self, uri, params={}):
        return requests.get(urlparse.urljoin(Investigate.BASE_URL, uri),
            params=params, headers=self._auth_header
        )

    def post(self, uri, params={}, data={}):
        return requests.post(
            urlparse.urljoin(Investigate.BASE_URL, uri),
            params=params, data=data, headers=self._auth_header
        )

    def _request_parse(self, method, *args):
        r = method(*args)
        r.raise_for_status()
        return r.json()

    def get_parse(self, uri, params={}):
        return self._request_parse(self.get, uri, params)

    def post_parse(self, uri, params={}, data={}):
        return self._request_parse(self.post, uri, params, data)

    def _get_categorization(self, domain, labels):
        uri = urlparse.urljoin(self._uris['categorization'], domain)
        params = {'showLabels': True} if labels else {}
        return self.get_parse(uri, params)

    def _post_categorization(self, domains, labels):
        params = {'showLabels': True} if labels else {}
        return self.post_parse(self._uris['categorization'], params,
            json.dumps(domains)
        )

    def get_categorization(self, domains, labels=False):
        if type(domains) is str:
            return self._get_categorization(domains, labels)
        elif type(domains) is list:
            return self._post_categorization(domains, labels)
        else:
            raise Investigate.DOMAIN_ERR

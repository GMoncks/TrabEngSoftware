from urllib.parse import urljoin, urlencode
import json
import requests

class request_helper:
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        
    def post(self, apiUrl, data):
        requestUrl = self.build_request(apiUrl)
        result = requests.post(requestUrl, data=data)
        if result.status_code != 200:
            raise Exception(result.json())
        return result.json()
        
    def get(self, apiUrl):
        requestUrl = self.build_request(apiUrl)
        result = requests.get(requestUrl)
        if result.status_code != 200:
            raise Exception(result.json())
        return result.json()
    
    def get(self, apiUrl, params):
        requestUrl = self.build_request(apiUrl, params)
        result = requests.get(requestUrl)
        if result.status_code != 200:
            raise Exception(result.json())
        return result.json()

    def build_request(self, apiUrl, params=None):
        if params != None:
            return urljoin(self.baseUrl, apiUrl) + "?" + urlencode(params)
        else:        
            return urljoin(self.baseUrl, apiUrl)

    def parse_data(self, data):
        return json.dumps(data)
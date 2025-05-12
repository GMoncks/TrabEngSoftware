from urllib.parse import urljoin, urlencode
import json
import requests

class request_helper:
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        
    def post(self, apiUrl, data):
        requestUrl = self.build_request(apiUrl)
        return requests.post(requestUrl, data=data).json()
        
    def get(self, apiUrl):
        requestUrl = self.build_request(apiUrl)
        return requests.get(requestUrl).json()
    
    def get(self, apiUrl, params):
        requestUrl = self.build_request(apiUrl, params)
        return requests.get(requestUrl).json()

    def build_request(self, apiUrl, params=None):
        if params != None:
            return urljoin(self.baseUrl, apiUrl) + "?" + urlencode(params)
        else:        
            return urljoin(self.baseUrl, apiUrl)

    def parse_data(self, data):
        return json.dumps(data)
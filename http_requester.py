import requests

class HttpRequester:

    def __init__(self, url_base):
        self.__url_base = url_base
        return

    def get(self, path, params, headers):
        url = self.__url_base +  path
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def post(self, path, headers, body):
        url = self.__url_base +  path
        response = requests.post(url, headers=headers, json=body)
        return response.text


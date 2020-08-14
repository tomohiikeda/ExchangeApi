import http_requester
from abc import ABCMeta, abstractmethod

class ExchangeApi:

    def __init__(self, url_base, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.http = http_requester.HttpRequester(url_base)
        return

    @abstractmethod
    def get_spot_ticker(self):
        pass

    @abstractmethod
    def get_fx_ticker(self):
        pass

    @abstractmethod
    def send_parentorders_ifd_stop(self, price, size, stop_price):
        pass
    
    @abstractmethod
    def send_childorders(self, order_type, side, price, size):
        pass

    @abstractmethod
    def send_parentorders_simple_stop(self, side, price, size):
        pass

    @abstractmethod
    def cancel_all_child_orders(self):
        pass

    @abstractmethod
    def get_positions(self):
        pass
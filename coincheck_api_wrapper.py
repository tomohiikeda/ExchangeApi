import pprint
import hashlib
import hmac
import time
import urllib
import json
from datetime import datetime
from exchange_api import ExchangeApi

#https://coincheck.com/ja/documents/exchange/api

class CoincheckAPIWrapper(ExchangeApi):

    url_base = 'https://coincheck.com'

    #----------------------------------------
    # コンストラクタ
    #----------------------------------------
    def __init__(self, api_key, api_secret, market_code):
        super().__init__(self.url_base, api_key, api_secret)
        self.__market_code = market_code
        return

    #----------------------------------------
    # Hashを計算
    #----------------------------------------
    def __generate_hash(self, timestamp, method, path, params, body):
        if params is not None:
            path = path + '?' + urllib.parse.urlencode(params)
        json_body = ''
        if body is not None:
            json_body = json.dumps(body)
        ba_text = bytearray(timestamp + self.url_base + path + json_body, 'ASCII')
        ba_secret = bytearray(self.api_secret, 'ASCII')
        hash = hmac.new(ba_secret, ba_text, hashlib.sha256).hexdigest()
        return hash

    #----------------------------------------
    # Private API用のヘッダを生成
    #----------------------------------------
    def __generate_header_for_private_api(self, method, path, params, body):
        timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
        hash = self.__generate_hash(timestamp, method, path, params, body)
        return { 'ACCESS-KEY': self.api_key,
                 'ACCESS-NONCE': timestamp,
                 'ACCESS-SIGNATURE': hash
               }
 
    #----------------------------------------
    # Private APIを実行(GET)
    #----------------------------------------
    def __submit_private_api_get(self, path, params):
        headers = self.__generate_header_for_private_api('GET', path, params, None)
        pprint.pprint(headers)
        return self.http.get(path, params, headers)

    #----------------------------------------
    # Private APIを実行(POST)
    #----------------------------------------
    def __submit_private_api_post(self, path, params, body):
        headers = self.__generate_header_for_private_api('POST', path, params, body)
        return self.http.post(path, headers, body)

    #----------------------------------------
    # Tickerを取得
    #----------------------------------------
    def get_ticker(self):
        resp = self.http.get('/api/ticker', None, None)
        last = float(resp['last'])
        resp = self.http.get('/api/order_books', None, None)
        bid = float(resp['bids'][0][0])
        ask = float(resp['asks'][0][0])
        return last, bid, ask

    #----------------------------------------
    # 板情報を取得
    #----------------------------------------
    def get_order_books(self):
        resp = self.http.get('/api/order_books', None, None)
        pprint.pprint(resp['bids'][0][0])
        return

    #----------------------------------------
    # 新規注文を出す
    #----------------------------------------
    def send_childorders(self, order_type, side, price, size):
        if order_type == 'MARKET' and side == 'BUY':
            ortype = 'market_buy'
        elif order_type == 'MARKET' and side == 'SELL':
            ortype = 'market_sell'
        elif order_type == 'LIMIT' and side == 'BUY':
            ortype = 'buy'
        elif order_type == 'LIMIT' and side == 'SELL':
            ortype = 'sell'
        else:
            ortype = ''

        body = {
            'id': 12345,
            'rate': str(price),
            'amount': str(size),
            'order_type': ortype,
            'stop_loss_rate': 'null',
            'pair': self.__market_code,
            'executionTYpe': order_type,
            
        }
        resp = self.__submit_private_api_post('/api/exchange/orders', None, body)
        pprint.pprint(resp)

    #----------------------------------------
    # 資産残高を取得
    #----------------------------------------
    def get_balance(self):
        resp = self.__submit_private_api_get('/api/accounts/balance', None)
        pprint.pprint(resp)
        return


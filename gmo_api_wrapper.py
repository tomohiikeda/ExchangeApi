import pprint
import hashlib
import hmac
import time
import urllib
import json
from datetime import datetime
from exchange_api import ExchangeApi

#https://api.coin.z.com/docs

class GmoAPIWrapper(ExchangeApi):

    #----------------------------------------
    # コンストラクタ
    #----------------------------------------
    def __init__(self, api_key, api_secret, market_code):
        super().__init__('https://api.coin.z.com', api_key, api_secret)
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
        ba_text = bytearray(timestamp + method + path + json_body, 'ASCII')
        ba_secret = bytearray(self.api_secret, 'ASCII')
        hash = hmac.new(ba_secret, ba_text, hashlib.sha256).hexdigest()
        return hash

    #----------------------------------------
    # Private API用のヘッダを生成
    #----------------------------------------
    def __generate_header_for_private_api(self, method, path, params, body):
        timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
        hash = self.__generate_hash(timestamp, method, path, params, body)
        return { 'API-KEY': self.api_key,
                 'API-TIMESTAMP': timestamp,
                 'API-SIGN': hash
               }
 
    #----------------------------------------
    # Private APIを実行(GET)
    #----------------------------------------
    def __submit_private_api_get(self, path, params):
        headers = self.__generate_header_for_private_api('GET', path, params, None)
        path = '/private' + path
        return self.http.get(path, params, headers)

    #----------------------------------------
    # Private APIを実行(POST)
    #----------------------------------------
    def __submit_private_api_post(self, path, params, body):
        headers = self.__generate_header_for_private_api('POST', path, params, body)
        path = '/private' + path
        return self.http.post(path, headers, body)

    #----------------------------------------
    # Tickerを取得
    #----------------------------------------
    def get_ticker(self):
        params = {'symbol': self.__market_code}
        resp = self.http.get('/public/v1/ticker', params, None)['data'][0]
        return int(resp['last']), int(resp['bid']), int(resp['ask'])

    #----------------------------------------
    # 新規注文を出す
    #----------------------------------------
    def send_childorders(self, order_type, side, price, size):
        body = {
            'symbol': self.__market_code,
            'side': side,
            'executionTYpe': order_type,
            'price': str(price),
            'size': str(size),
        }
        resp = self.__submit_private_api_post('/v1/order', None, body)
        pprint.pprint(resp)

    #----------------------------------------
    # 余力情報を取得
    #----------------------------------------
    def get_margin(self):
        resp = self.__submit_private_api_get('/v1/account/margin', None)
        pprint.pprint(resp)
        return

    #----------------------------------------
    # 資産残高を取得
    #----------------------------------------
    def get_balance(self):
        resp = self.__submit_private_api_get('/v1/account/assets', None)
        pprint.pprint(resp)
        return


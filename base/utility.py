from random import randint
import requests
from pprint import pprint
import json


class BtcPrice():
    def __init__(self):
        self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        self.params = {
            'symbol' : 'BTC',
            'convert': 'USD'
        }
        self.headers = {
            'Accepts' : 'application/json',
            'X-CMC_PRO_API_KEY' : '86c54475-e065-4001-8f36-6aa8f6ec8f18'
        }

    def fetchCurrenciesData(self):
        r = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        return r['data']['BTC']['quote']['USD']['price']


def random_btc_amount():
    btc_amount = randint(1,10)
    return btc_amount

from random import randint
import requests
from bson import ObjectId
import json
from datetime import datetime
from typing import Any


class BtcPrice():
    def __init__(self):
        self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        self.params = {
            'symbol': 'BTC',
            'convert': 'USD'
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '86c54475-e065-4001-8f36-6aa8f6ec8f18'
        }

    def fetchCurrenciesData(self):
        r = requests.get(url=self.url, headers=self.headers,
                         params=self.params).json()
        return r['data']['BTC']['quote']['USD']['price']


def btc_price():
    bot = BtcPrice()
    current_price = bot.fetchCurrenciesData()
    return current_price


def random_btc_amount():
    btc_amount = randint(1, 10)
    return btc_amount


class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

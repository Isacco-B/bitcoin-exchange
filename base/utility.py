from django.db.models import Q
from base import models
from random import randint
from pymongo import MongoClient
from pprint import pprint
import requests


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

def btc_price():
    bot = BtcPrice()
    current_price = bot.fetchCurrenciesData()
    return current_price

def random_btc_amount():
    btc_amount = randint(1,10)
    return btc_amount



def check_order_match():
    buy_orders = models.Order.objects.filter(order_type='Buy',order_status='Open').order_by('-date_of_creation')
    sell_orders = models.Order.objects.filter(order_type='Sell',order_status='Open').order_by('-date_of_creation')
    if buy_orders.count() >= 1 and sell_orders.count() >= 1:
        for buy_order in buy_orders:
            order_price = buy_order.order_price
            btc_amount = buy_order.btc_amount
            for sell_order in sell_orders.filter(~Q(user=buy_order.user),order_price__lte=order_price, btc_amount=btc_amount,):
                if sell_order:
                    return order_match(sell_order, buy_order)


def order_match(sell_order, buy_order):
    buy_user = models.User.objects.filter(pk=buy_order.user.pk)
    sell_user = models.User.objects.filter(pk=sell_order.user.pk)
    buy_user_btc = buy_user.get().wallet_btc
    buy_user_usd = buy_user.get().usd_balance
    sell_user_btc = sell_user.get().wallet_btc
    sell_user_usd = sell_user.get().usd_balance
    buy_user.update(wallet_btc = buy_user_btc + sell_order.btc_amount, usd_balance = buy_user_usd - sell_order.order_price)
    sell_user.update(wallet_btc = sell_user_btc - buy_order.btc_amount, usd_balance = sell_user_usd + buy_order.order_price)
    sell_order.order_status = 'Close'
    buy_order.order_status = 'Close'
    sell_order.save()
    buy_order.save()
    return save_order_transaction()

def save_order_transaction():
    client = MongoClient("mongodb://localhost:27017")
    db = client.exchange
    order_collection = db.orders_transactions
    order_collection.insert_one(
        {
        "name" : "Isacco",
        "subname" : "Bertoli",
        "age" : 22,
        "hobby" : ["moto","calcio","palestra"]
    }
    )



    # for b_order in buy_order:
    #     buy_price = b_order.order_price
    #     for s_order in sell_order.filter(order_price__lte=buy_price):
    #         ss_order = models.Order.objects.get(pk=s_order.pk)
    #         bb_order = models.Order.objects.get(pk=b_order.pk)
    #         sell_user = models.User.objects.filter(username=s_order.user)
    #         buy_user = models.User.objects.filter(username=b_order.user)
    #         sell_wallet = sell_user.get().wallet_btc
    #         buy_wallet = buy_user.get().wallet_btc
    #         sell_wallet -= bb_order.btc_amount
    #         buy_wallet += bb_order.btc_amount
    #         sell_user.update(wallet_btc=sell_wallet)
    #         buy_user.update(wallet_btc=buy_wallet)
    #         ss_order.order_status = 'Close'
    #         bb_order.order_status = 'Close'
    #         ss_order.save()
    #         bb_order.save()

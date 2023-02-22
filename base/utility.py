from django.db.models import Q
from base import models
from random import randint
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


def update_user_profile(current_order, old_order, type):
    user = models.User.objects.filter(pk=current_order.user.pk)
    user_usd_balance = user.get().usd_balance
    user_btc_balance = user.get().wallet_btc

    if type == 'create':
        if current_order.order_type == 'Sell':
            user.update(wallet_btc = user_btc_balance - current_order.btc_amount)
        else:
            user.update(usd_balance = user_usd_balance - current_order.order_price)
    elif type == 'update':
        btc_difference = current_order.btc_amount - old_order.btc_amount
        usd_difference = current_order.order_price - old_order.order_price
        if current_order.order_type == 'Buy':
            if current_order.order_price > old_order.order_price:
                user.update(usd_balance = user_usd_balance - usd_difference)
            else:
                user.update(usd_balance = user_usd_balance - usd_difference)
        else:
            if current_order.btc_amount > old_order.btc_amount:
                user.update(wallet_btc = user_btc_balance - btc_difference)
            else:
                user.update(wallet_btc = user_btc_balance - btc_difference)
    else:
        if current_order.order_type == 'Sell':
            user.update(wallet_btc = user_btc_balance + current_order.btc_amount)
        elif current_order.order_type == 'Buy':
            user.update(usd_balance = user_usd_balance + current_order.order_price)


def check_order_match():
    buy_orders = models.Order.objects.filter(order_type='Buy',order_status='Open').order_by('-date_of_creation')
    sell_orders = models.Order.objects.filter(order_type='Sell',order_status='Open').order_by('-date_of_creation')
    if buy_orders.count() >= 1 and sell_orders.count() >= 1:
        for buy_order in buy_orders:
            order_price = buy_order.order_price
            btc_amount = buy_order.btc_amount
            for sell_order in sell_orders.filter(~Q(user=buy_order.user),order_price__lte=order_price, btc_amount=btc_amount,):
                if sell_order:
                    print(sell_order.order_price)
                    print(buy_order.order_price)
                    order_match(sell_order, buy_order)


def order_match(sell_order, buy_order):
    buy_user = models.User.objects.filter(pk=buy_order.user.pk)
    sell_user = models.User.objects.filter(pk=sell_order.user.pk)
    buy_user_btc = buy_user.get().wallet_btc
    buy_user_usd = buy_user.get().usd_balance
    buy_user_profit = buy_user.get().profit
    sell_user_usd = sell_user.get().usd_balance
    sell_user_profit = sell_user.get().profit
    if buy_order.order_price > sell_order.order_price:
        price_difference = buy_order.order_price - sell_order.order_price
        buy_user.update(
            wallet_btc = buy_user_btc + sell_order.btc_amount,
            usd_balance = buy_user_usd + price_difference,
            profit = buy_user_profit - sell_order.order_price
            )
        sell_user.update(
            usd_balance = sell_user_usd + buy_order.order_price - price_difference,
            profit = sell_user_profit + sell_order.order_price
            )
        sell_order.order_status = 'Close'
        sell_order.buyer_user = str(buy_user.get().username)
        sell_order.selling_price = sell_order.order_price

        buy_order.order_status = 'Close'
        buy_order.buyer_user = str(sell_user.get().username)
        buy_order.selling_price = sell_order.order_price
        buy_order.order_refund = price_difference

        sell_order.save()
        buy_order.save()

    else:
        buy_user.update(
            wallet_btc = buy_user_btc + sell_order.btc_amount,
            profit = buy_user_profit - sell_order.order_price
            )
        sell_user.update(
            usd_balance = sell_user_usd + buy_order.order_price,
            profit = sell_user_profit + sell_order.order_price
            )

        sell_order.order_status = 'Close'
        sell_order.buyer_user = str(buy_user.get().username)
        sell_order.selling_price = sell_order.order_price

        buy_order.order_status = 'Close'
        buy_order.buyer_user = str(sell_user.get().username)
        buy_order.selling_price = sell_order.order_price

        sell_order.save()
        buy_order.save()

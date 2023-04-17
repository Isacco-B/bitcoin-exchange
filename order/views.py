from django.shortcuts import render, reverse
from django.db.models import Q
from django.contrib import messages
from django.http.response import JsonResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from base.models import Order, User
from base.forms import OrderForm, UpdateOrderForm
from base.utility import MongoJSONEncoder
from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017")
db = client.exchange
order_collection = db.order_transactions


class OrderListView(LoginRequiredMixin, generic.ListView):
    template_name = 'order/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.all()


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'order/order_create.html'
    form_class = OrderForm

    def get_form_kwargs(self):
        kwargs = super(OrderCreateView, self).get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def get_success_url(self):
        return reverse('landing-page')

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user)
        form = form.save(commit=False)
        form.user = user
        messages.success(self.request, 'You have successfuly created a order')
        return super(OrderCreateView, self).form_valid(form)


class OrderDetailView(generic.DetailView):
    template_name = 'order/order_detail.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.all()


class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'order/order_update.html'
    context_object_name = 'orders'
    form_class = UpdateOrderForm

    def get_form_kwargs(self):
        kwargs = super(OrderUpdateView, self).get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def get_success_url(self):
        check_order_match()
        return reverse('landing-page')

    def get_queryset(self):
        return Order.objects.filter(order_status='Open', user=self.request.user.pk)

    def form_valid(self, form):
        form.save()
        messages.info(self.request, 'You have successfuly update a order')
        return super(OrderUpdateView, self).form_valid(form)


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'order/order_delete.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(order_status='Open', user=self.request.user.pk)

    def get_success_url(self) -> str:
        messages.info(self.request, 'Order successfully deleted')
        return reverse('landing-page')


class OrderJsonView(generic.View):
    def get(self, request, type, *args, **kwargs):
        encode_orders = MongoJSONEncoder().encode(
            list(order_collection.find({'User': self.request.user.username, 'Type': type})))
        orders = json.loads(encode_orders)
        order = {
            'order': orders
        }
        return JsonResponse(order, safe=False, json_dumps_params={'indent': 3})


def update_user_profile(current_order, old_order, type):
    user = User.objects.filter(pk=current_order.user.pk)
    user_usd_balance = user.get().usd_balance
    user_btc_balance = user.get().wallet_btc

    if type == 'create':
        if current_order.order_type == 'Sell':
            user.update(wallet_btc=user_btc_balance - current_order.btc_amount)
        else:
            user.update(usd_balance=user_usd_balance - current_order.order_price)
    elif type == 'update':
        btc_difference = current_order.btc_amount - old_order.btc_amount
        usd_difference = current_order.order_price - old_order.order_price
        if current_order.order_type == 'Buy':
            if current_order.order_price > old_order.order_price:
                user.update(usd_balance=user_usd_balance - usd_difference)
            else:
                user.update(usd_balance=user_usd_balance - usd_difference)
        else:
            if current_order.btc_amount > old_order.btc_amount:
                user.update(wallet_btc=user_btc_balance - btc_difference)
            else:
                user.update(wallet_btc=user_btc_balance - btc_difference)
    else:
        if current_order.order_type == 'Sell':
            user.update(wallet_btc=user_btc_balance + current_order.btc_amount)
        elif current_order.order_type == 'Buy':
            user.update(usd_balance=user_usd_balance + current_order.order_price)


def check_order_match():
    buy_orders = Order.objects.filter(
        order_type='Buy', order_status='Open').order_by('order_price','date_of_creation')
    sell_orders = Order.objects.filter(
        order_type='Sell', order_status='Open').order_by('order_price','date_of_creation')

    if buy_orders.exists() and sell_orders.exists():
        for buy_order in buy_orders:
            match_type = None

            matching_sell_orders = sell_orders.filter(
                ~Q(user=buy_order.user),
                order_price=buy_order.order_price,
                btc_amount=buy_order.btc_amount
                )
            if matching_sell_orders.exists():
                match_type = 'A'
            else:
                matching_sell_orders = sell_orders.filter(
                    ~Q(user=buy_order.user),
                    order_price__lte=buy_order.order_price,
                    btc_amount=buy_order.btc_amount
                    )
                if matching_sell_orders.exists():
                    match_type = 'B'
                else:
                    matching_sell_orders = sell_orders.filter(
                        ~Q(user=buy_order.user),
                        order_price__lte=buy_order.order_price,
                        btc_amount__gte=buy_order.btc_amount
                        )
                    if matching_sell_orders.exists():
                        match_type = 'C'
            if match_type:
                matching_sell_order = matching_sell_orders.first()
                order_match(matching_sell_order, buy_order, match_type)


def order_match(sell_order, buy_order, match_type):
    buy_user = User.objects.filter(pk=buy_order.user.pk)
    sell_user = User.objects.filter(pk=sell_order.user.pk)
    buy_user_btc = buy_user.get().wallet_btc
    buy_user_usd = buy_user.get().usd_balance
    buy_user_profit = buy_user.get().profit
    sell_user_usd = sell_user.get().usd_balance
    sell_user_profit = sell_user.get().profit

    if match_type == 'A':
        buy_user.update(
            wallet_btc=buy_user_btc + sell_order.btc_amount,
            profit=buy_user_profit - sell_order.order_price
        )
        sell_user.update(
            usd_balance=sell_user_usd + buy_order.order_price,
            profit=sell_user_profit + sell_order.order_price
        )

        sell_order.order_status = 'Close'
        sell_order.buyer_user = buy_user.get().username
        sell_order.selling_price = sell_order.order_price

        buy_order.order_status = 'Close'
        buy_order.buyer_user = sell_user.get().username
        buy_order.selling_price = sell_order.order_price

        sell_order.save()
        buy_order.save()
        save_order_transactions(sell_order, buy_order)

    if match_type == 'B':
        price_difference = buy_order.order_price - sell_order.order_price
        buy_user.update(
            wallet_btc=buy_user_btc + sell_order.btc_amount,
            usd_balance=buy_user_usd + price_difference,
            profit=buy_user_profit - sell_order.order_price
        )
        sell_user.update(
            usd_balance=sell_user_usd + buy_order.order_price - price_difference,
            profit=sell_user_profit + sell_order.order_price
        )
        sell_order.order_status = 'Close'
        sell_order.buyer_user = buy_user.get().username
        sell_order.selling_price = sell_order.order_price

        buy_order.order_status = 'Close'
        buy_order.buyer_user = sell_user.get().username
        buy_order.selling_price = sell_order.order_price
        buy_order.order_refund = price_difference

        sell_order.save()
        buy_order.save()
        save_order_transactions(sell_order, buy_order)

    if match_type == 'C':
        new_sell_order = Order.objects.filter(pk=sell_order.pk)
        price_difference = buy_order.order_price - (buy_order.order_price - int(buy_order.btc_amount * (sell_order.order_price / sell_order.btc_amount)))
        btc_difference = sell_order.btc_amount - buy_order.btc_amount

        buy_user.update(
            wallet_btc=buy_user_btc + sell_order.btc_amount - btc_difference,
            usd_balance=buy_user_usd + (buy_order.order_price - price_difference),
            profit=buy_user_profit - price_difference,
        )
        sell_user.update(
            usd_balance=sell_user_usd + price_difference,
            profit=sell_user_profit + price_difference,
        )
        new_sell_order.update(
            order_status = 'Open',
            buyer_user = buy_user.get().username,
            order_price = sell_order.order_price - price_difference,
            btc_amount = sell_order.btc_amount - btc_difference,
        )

        buy_order.order_status = 'Close'
        buy_order.buyer_user = sell_user.get().username
        buy_order.selling_price = price_difference
        buy_order.order_refund = buy_order.order_price - price_difference
        buy_order.save()

        order = [

            {
                'User': buy_order.user.username,
                'Id': buy_order.pk,
                'Type': buy_order.order_type,
                'Status': buy_order.order_status,
                'Price': buy_order.order_price,
                'Qty': buy_order.btc_amount,
                'Refund': buy_order.order_refund,
                'Seller': sell_order.user.username,
                'Purchase Price': buy_order.selling_price,
            },
            {
                'User': sell_order.user.username,
                'Id': sell_order.pk,
                'Type': sell_order.order_type,
                'Status': 'Close',
                'Price': sell_order.order_price - buy_order.selling_price,
                'Qty': buy_order.btc_amount,
                'Buyer': buy_order.user.username,
                'Purchase Price': buy_order.selling_price,
            }
        ]
        order_collection.insert_many(order)


def save_order_transactions(sell_order, buy_order):

    order = [
        {
            'User': buy_order.user.username,
            'Id': buy_order.pk,
            'Type': buy_order.order_type,
            'Status': buy_order.order_status,
            'Price': buy_order.order_price,
            'Qty': buy_order.btc_amount,
            'Refund': buy_order.order_refund,
            'Buyer': sell_order.user.username,
            'Purchase Price': buy_order.selling_price,
        },
        {
            'User': sell_order.user.username,
            'Id': sell_order.pk,
            'Type': sell_order.order_type,
            'Status': sell_order.order_status,
            'Price': sell_order.order_price,
            'Qty': sell_order.btc_amount,
            'Buyer': buy_order.user.username,
            'Purchase Price': sell_order.selling_price,
        }
    ]
    order_collection.insert_many(order)

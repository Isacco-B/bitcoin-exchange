from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UsernameField
from base.models import Order, User


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop(
            "request", None
        )
        super(OrderForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = (
            'order_type',
            'btc_amount',
            'order_price',
        )

    def clean_btc_amount(self):
        btc_amount = self.cleaned_data['btc_amount']
        order_type = self.cleaned_data['order_type']
        user = User.objects.get(username=self.request.user)
        if btc_amount > user.wallet_btc and order_type == 'Sell':
            raise ValidationError('insufficient funds')
        elif btc_amount <= 0:
            raise ValidationError('enter a number greater than zero')
        return btc_amount

    def clean_order_price(self):
        order_price = self.cleaned_data['order_price']
        order_type = self.cleaned_data['order_type']
        user = User.objects.get(username=self.request.user)
        if order_price > user.usd_balance and order_type == 'Buy':
            raise ValidationError('insufficient funds')
        elif order_price <= 0:
            raise ValidationError('enter a number greater than zero')
        return order_price


class UpdateOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop(
            "request", None
        )
        super(UpdateOrderForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = (
            'order_type',
            'btc_amount',
            'order_price',
        )
        widgets = {'order_type': forms.HiddenInput()}

    def clean_btc_amount(self):
        btc_amount = self.cleaned_data['btc_amount']
        order_type = self.cleaned_data['order_type']
        user = User.objects.get(username=self.request.user)
        if order_type == 'Sell':
            if btc_amount > self.instance.btc_amount:
                if user.wallet_btc + self.instance.btc_amount < btc_amount:
                    raise ValidationError('insufficient funds')
            elif btc_amount <= 0:
                raise ValidationError('enter a number greater than zero')
        return btc_amount

    def clean_order_price(self):
        order_price = self.cleaned_data['order_price']
        order_type = self.cleaned_data['order_type']
        user = User.objects.get(username=self.request.user)
        if order_type == 'Buy':
            if order_price > self.instance.order_price:
                if user.usd_balance + self.instance.order_price < order_price:
                    raise ValidationError('insufficient funds')
            elif order_price <= 0:
                raise ValidationError('enter a number greater than zero')
        return order_price


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "username",
            'first_name',
            'last_name',
            'age',
            'gender',
            'email',
            'address',
            'phone_number',
        )
        field_classes = {"username": UsernameField}

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
        user = User.objects.get(username = self.request.user)
        if btc_amount > user.wallet_btc:
            raise ValidationError('insufficient funds')
        elif btc_amount <= 0:
            raise ValidationError('enter a number greater than zero')
        return btc_amount

    def clean_order_price(self):
        data = self.cleaned_data['order_price']
        user = User.objects.get(username = self.request.user)
        if data > user.usd_balance:
            raise ValidationError('insufficient funds')
        elif data <= 0:
            raise ValidationError('enter a number greater than zero')
        return data

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

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields =  (
            'username',
            'first_name',
            'last_name',
            'email',
            'age',
            'address',
            'phone_number',
        )

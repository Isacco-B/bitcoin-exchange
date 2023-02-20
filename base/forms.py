from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from base.models import Order, User

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            "order_type",
            'btc_amount',
            'order_price',
            )


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

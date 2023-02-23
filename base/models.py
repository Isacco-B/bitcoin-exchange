from django.db import models
from django.contrib.auth.models import AbstractUser
from base.utility import random_btc_amount



class User(AbstractUser):

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    ips = models.Field(default=[])
    wallet_btc = models.FloatField(null=True, blank=True)
    usd_balance = models.FloatField(null=True, blank=True)
    profit = models.FloatField(default=0)
    age = models.IntegerField(default=0)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=50)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")

    def save(self, *arg, **kwargs):
        if self.pk is None:
            self.wallet_btc = random_btc_amount()
            self.usd_balance = 10000
            super(User, self).save()

    def __str__(self):
        return self.username


class Order(models.Model):

    ORDER_STATUS = (
        ('Open', 'Open'),
        ('Close', 'Close'),
    )

    ORDER_TYPE = (
        ('Buy', 'Buy'),
        ('Sell', 'Sell'),
    )


    order_type = models.CharField(choices=ORDER_TYPE, default='Buy', max_length=50)
    order_status = models.CharField(choices=ORDER_STATUS, default='Open', max_length=50)
    btc_amount = models.FloatField(default= 0)
    order_price = models.FloatField(default=0)
    selling_price = models.FloatField(default=0)
    order_refund = models.FloatField(default=0)
    buyer_user = models.CharField(null=True, blank=True, max_length=20)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Order")
        verbose_name_plural = ("Orders")

    def __str__(self):
        return self.user.username














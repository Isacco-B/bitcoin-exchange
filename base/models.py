from django.db import models
from django.utils import timezone
from djongo.models.fields import ObjectIdField, Field
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from base.random_btc_amount import random_btc_amount


class User(AbstractUser):

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    _id = ObjectIdField()
    ips = models.Field(default=[])
    wallet_btc = models.FloatField(null=True, blank=True)
    age = models.IntegerField(default=0)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=50)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")

    # def save(self, *arg, **kwargs):
    #     self.wallet_btc = random_btc_amount()
    #     super(User, self).save()

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

    _id = ObjectIdField()
    order_type = models.CharField(choices=ORDER_TYPE, default='Buy', max_length=50)
    order_status = models.CharField(choices=ORDER_STATUS, default='Open', max_length=50)
    order_price = models.FloatField(default=0)
    date_of_creation = models.DateField(default=timezone.localdate())
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Order")
        verbose_name_plural = ("Orders")

    def __str__(self):
        return self.user.username + " " + self.date_of_creation


# class Transaction(models.Model):



#     class Meta:
#         verbose_name = ("Transaction")
#         verbose_name_plural = ("Transactions")

#     def __str__(self):
#         return self.name












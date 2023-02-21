from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from django.contrib import messages
from .models import User, Order
from .utility import check_order_match
from pprint import pprint


@receiver(user_logged_in)
def login_success(sender, request, user, **kwargs):
    user_ip = request.META['REMOTE_ADDR']
    user = User.objects.get(username=user.username)
    user_last_ip = user.ips
    print(user_last_ip)
    if not user_last_ip:
        user_last_ip.append(user_ip)
        User.objects.filter(username=user.username).update(ips=user_last_ip)
    elif user_ip not in user_last_ip:
        messages.warning(request,f'your ip has changed!')
        user_last_ip.append(user_ip)
        User.objects.filter(username=user.username).update(ips=user_last_ip)


@receiver(post_save)
def create_order(sender, instance, created, **kwargs):
        if created:
            check_order_match()

@receiver(post_save)
def update_order(sender, instance, created, **kwargs):
        if not created:
            check_order_match()


# @receiver(pre_save, sender=Order)
# def update_order(sender, instance, **kwargs):
#     if instance.id is not None:
#         current_order = instance
#         old_order = Order.objects.get(id=instance.id)
#         if current_order.order_price != old_order.order_price:
#             check_order_match()

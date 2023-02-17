from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from .models import User


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


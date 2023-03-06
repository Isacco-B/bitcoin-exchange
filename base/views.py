from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm
from .models import Order, User
from .utility import btc_price


class LandingPageView(LoginRequiredMixin, generic.TemplateView):
    template_name = "landing.html"

    def get_context_data(self, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        context = {
            'buy_orders': Order.objects.filter(order_type='Buy', user=user).order_by('-date_of_creation'),
            'sell_orders': Order.objects.filter(order_type='Sell', user=user).order_by('-date_of_creation'),
            'user': user,
            'btc_price': round(btc_price() * user.wallet_btc, 2)
        }
        return context


class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = UserForm

    def get_success_url(self) -> str:
        return reverse('login')

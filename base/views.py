from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm
from .models import Order

class LandingPageView(LoginRequiredMixin, generic.TemplateView):
    template_name = "landing.html"


class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = UserForm

    def get_success_url(self) -> str:
        return reverse('login')

class SearchResultsView(generic.ListView):
    model = Order
    template_name = 'search_result.html'
    context_object_name = 'orders'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Order.objects.all()
        return object_list













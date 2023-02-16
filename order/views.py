from django.shortcuts import render, reverse
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from base.models import Order
from base.forms import OrderForm
from .mixins import StaffAndLoginRequiredMixin


class OrderListView(LoginRequiredMixin, generic.ListView):
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        elif self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user.pk)


class OrderCreateView(StaffAndLoginRequiredMixin, generic.CreateView):
    template_name = 'orders/order_create.html'
    form_class = OrderForm

    def get_success_url(self) -> str:
        return reverse('orders:order-list')

    def form_valid(self, form):
        messages.success(self.request, 'You have successfuly created a order')
        return super(OrderCreateView, self).form_valid(form)


class OrderDetailView(generic.DetailView):
    template_name = 'orders/order_detail.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.all()


class OrderUpdateView(StaffAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'orders/order_update.html'
    context_object_name = 'orders'
    form_class = OrderForm

    def get_success_url(self) -> str:
        return reverse('orders:order-list')

    def get_queryset(self):
        return Order.objects.all()

    def form_valid(self, form):
        form.save()
        messages.info(self.request, 'You have successfuly update a order')
        return super(OrderUpdateView, self).form_valid(form)


class OrderDeleteView(StaffAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'orders/order_delete.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.all()

    def get_success_url(self) -> str:
        return reverse('orders:order-list')





from django.shortcuts import render, reverse
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from base.models import Order, User
from base.forms import OrderForm


class OrderListView(LoginRequiredMixin, generic.ListView):
    template_name = 'order/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.all()



class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'order/order_create.html'
    form_class = OrderForm

    def get_form_kwargs(self):
        kwargs = super(OrderCreateView, self).get_form_kwargs()
        # Update the existing form kwargs dict with the request's user.
        kwargs.update({"request": self.request})
        return kwargs

    def get_success_url(self):
        return reverse('orders:order-list')

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user)
        form = form.save(commit=False)
        form.user = user
        messages.success(self.request, 'You have successfuly created a order')
        return super(OrderCreateView, self).form_valid(form)


class OrderDetailView(generic.DetailView):
    template_name = 'order/order_detail.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.all()


class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'order/order_update.html'
    context_object_name = 'orders'
    form_class = OrderForm

    def get_form_kwargs(self):
        kwargs = super(OrderUpdateView, self).get_form_kwargs()
        # Update the existing form kwargs dict with the request's user.
        kwargs.update({"request": self.request})
        return kwargs

    def get_success_url(self) -> str:
        return reverse('orders:order-list')

    def get_queryset(self):
        return Order.objects.all()

    def form_valid(self, form):
        messages.info(self.request, 'You have successfuly update a order')
        return super(OrderUpdateView, self).form_valid(form)


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'order/order_delete.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.all()

    def get_success_url(self) -> str:
        return reverse('orders:order-list')





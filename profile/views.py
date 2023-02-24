from django.shortcuts import render, reverse
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from base.models import User


class UserListView(LoginRequiredMixin, generic.ListView):
    template_name = 'profile/profile_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(pk=self.request.user.pk)


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'profile/profile_detail.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all()


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'profile/profile_delete.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all()

    def get_success_url(self) -> str:
        return reverse('landing-page')

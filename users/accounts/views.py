from allauth.account.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import *

from ..models import *


class AccountLogoutView(LogoutView):
    template_name = 'account/logout.html'


class AccountProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

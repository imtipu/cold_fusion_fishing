from django.utils.translation import gettext_lazy as _
from allauth.account.views import LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
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


class AccountPasswordChangeView(PasswordChangeView):
    template_name = 'account/password_change.html'
    success_url = reverse_lazy('account_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = _('Change Password')
        context['user'] = self.request.user
        return context

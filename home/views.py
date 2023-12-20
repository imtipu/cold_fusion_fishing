from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import *


class HomeView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('dashboard:home'))

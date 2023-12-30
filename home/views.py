from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import *


class HomeView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('dashboard:home'))


class ChangeLanguageView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('dashboard:home'))

    def post(self, request, *args, **kwargs):
        print(request.POST)
        language = request.POST.get('language')
        # if language and language == 'bn':
        #     request.session['language'] = 'bn'
        # else:
        #     request.session['language'] = None
        if language:
            request.session['language'] = language
        return HttpResponseRedirect(reverse('dashboard:home'))

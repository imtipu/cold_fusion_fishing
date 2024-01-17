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


def set_color_mode_view(request):
    if 'is_light_theme' not in request.session:
        request.session['is_light_theme'] = True
    else:
        request.session['is_light_theme'] = not request.session['is_light_theme']
    # request.session['is_dark_theme'] = True
    print(request.session['is_light_theme'])
    redirect_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(redirect_url)

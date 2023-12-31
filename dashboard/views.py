from django.shortcuts import render
from django.views.generic import *


class HomeView(TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Home'
        return context

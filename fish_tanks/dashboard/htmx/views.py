import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import *

from fish_tanks.models import *


class HtmxFistTankListView(LoginRequiredMixin, ListView):
    template_name = 'fish_tanks/dashboard/htmx/fish_tank_card_list.html'

    model = FishTank
    context_object_name = 'fish_tanks'

    def get_queryset(self):
        return self.model.objects.select_related(
            'current_project'
        ).all()


class FishTankQuickView(LoginRequiredMixin, DetailView):
    template_name = 'fish_tanks/dashboard/htmx/fish_tank_quick_view.html'

    model = FishTank
    context_object_name = 'fish_tank'

    def get(self, request, *args, **kwargs):
        # time.sleep(2)
        return super(self.__class__, self).get(request, *args, **kwargs)

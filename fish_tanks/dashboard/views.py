from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import *

# from modules.view_mixins import *

from fish_tanks.models import *


class FishTankListView(LoginRequiredMixin, ListView):
    template_name = 'fish_tanks/dashboard/fish_tank_list.html'

    model = FishTank
    context_object_name = 'fish_tanks'



class FishTankDetailView(LoginRequiredMixin, DetailView):
    template_name = 'fish_tanks/dashboard/htmx/fish_tank_quick_view.html'

    model = FishTank
    context_object_name = 'fish_tank'

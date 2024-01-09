from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import *
from django.contrib.messages.views import SuccessMessageMixin

# from modules.view_mixins import *
from .forms import *
from fish_tanks.models import *


class FishTankListView(LoginRequiredMixin, ListView):
    template_name = 'fish_tanks/dashboard/fish_tank_list.html'

    model = FishTank
    context_object_name = 'fish_tanks'


class FishTankDetailView(LoginRequiredMixin, DetailView):
    template_name = 'fish_tanks/dashboard/detail.html'

    model = FishTank
    context_object_name = 'fish_tank'


class FishTankUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'fish_tanks/dashboard/update.html'

    model = FishTank
    # context_object_name = 'fish_tank'
    form_class = FishTankForm
    success_message = _('Fish Tank Updated Successfully')

    def get_success_url(self):
        return reverse('dashboard:fish_tanks:fish_tank_update', kwargs={'pk': self.object.pk})


class FishTankCreateView(CreateView):
    model = FishTank
    template_name = 'fish_tanks/dashboard/create.html'
    form_class = FishTankForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Create New Fish Tank'
        return context

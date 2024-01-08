import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.views.generic import *

from ..forms import DailyActivityForm
from projects.models import *


class HtmxDailyActivityTableListView(LoginRequiredMixin, ListView):
    template_name = 'projects/dashboard/daily_activities/htmx/project_daily_activity_list.html'

    model = DailyActivity
    context_object_name = 'daily_activities'

    def get_queryset(self):
        # time.sleep(10)
        return self.model.objects.filter(
            project_id=self.kwargs.get('pk')
        ).select_related(
            'project', 'project__tank', 'project__tank__current_project'
        ).order_by('-activity_date')


def htmx_daily_activity_activity_form(request, pk):
    project = Project.objects.get(pk=pk)
    form = DailyActivityForm()
    context = {
        'project': project,
        'form': form,
    }
    return render(request,
                  'projects/dashboard/daily_activities/htmx/project_daily_activity_form.html',
                  context)

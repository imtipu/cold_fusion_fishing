import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.views.generic import *

from ..forms import DailyActivityForm
from projects.models import *


class HTMXDashboardHomeProjectListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/dashboard/projects/htmx/home_project_list.html'

    def get_queryset(self):
        return Project.objects.filter(
            models.Q(end_date__isnull=True) |
            models.Q(end_date__gte=timezone.now().date())
        )


class HtmxDailyActivityTableListView(LoginRequiredMixin, ListView):
    template_name = 'projects/dashboard/daily_activities/htmx/project_daily_activity_list.html'

    model = DailyActivity
    context_object_name = 'daily_activities'

    def get_project(self):
        return Project.objects.annotate(
            total_dead=models.Sum('daily_activities__dead_fish', output_field=models.IntegerField(), default=0),
            total_live=models.F('initial_quantity') - models.F('total_dead'),
        ).get(pk=self.kwargs.get('pk'))

    def get_queryset(self):
        # time.sleep(10)
        return self.model.objects.filter(
            project_id=self.kwargs.get('pk'),
        ).select_related(
            'project', 'project__tank', 'project__tank__current_project'
        ).annotate(
            initial_quantity=models.F('project__initial_quantity'),
            project_total_dead=models.Sum(
                'project__daily_activities__dead_fish',
                filter=models.Q(project__daily_activities__activity_date__lt=models.F('activity_date')),
                output_field=models.IntegerField(),
                default=0
            ),
            project_total_live=models.F('initial_quantity') - models.F('project_total_dead'),
            day_total_live=models.F('project_total_live') - models.F('dead_fish'),
        ).order_by('-activity_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['project'] = self.get_project()
        return ctx


def htmx_daily_activity_activity_form(request, pk):
    project = Project.objects.get(pk=pk)
    first_date = None
    activities = project.daily_activities.all()
    if not activities.exists():
        start_date = project.start_date
        first_date = f'{start_date}'
    if first_date:
        form = DailyActivityForm(initial={'activity_date': first_date})
    else:
        form = DailyActivityForm()

    context = {
        'project': project,
        'form': form,
        'first_date': first_date,
    }
    return render(request,
                  'projects/dashboard/daily_activities/htmx/project_daily_activity_form.html',
                  context)

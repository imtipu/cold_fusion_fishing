from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *

from projects.dashboard.forms import DailyActivityForm
from projects.models import *


class ProjectListView(ListView):
    template_name = 'projects/dashboard/project_list.html'

    model = Project
    context_object_name = 'projects'

    def get_queryset(self):
        return self.model.objects.select_related('tank').order_by('-start_date')


class ProjectDetailView(DetailView):
    template_name = 'projects/dashboard/project_detail.html'

    model = Project
    context_object_name = 'project'


class ProjectDailyActivityListView(ListView):
    template_name = 'projects/dashboard/daily_activities/project_daily_activity_list.html'

    model = DailyActivity
    context_object_name = 'daily_activities'

    def get_queryset(self):
        return self.model.objects.filter(
            project_id=self.kwargs.get('pk')
        ).select_related('project').order_by('-activity_date')


class DailyActivityAddView(CreateView):
    # template_name = 'projects/dashboard/daily_activities/project_daily_activity_form.html'

    model = DailyActivity
    form_class = DailyActivityForm

    # success_url = reverse_lazy('dashboard:projects:project_detailprojects:project_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs.get('pk'))
        return context

    # def form_valid(self, form):
    #     project_id = self.kwargs.get('pk')
    #     form.instance.project_id = project_id
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard:projects:project_detail', kwargs={'pk': self.kwargs.get('pk')})

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs.get('pk'))
        form = DailyActivityForm(request.POST)
        if form.is_valid():
            form.instance.project = project
            instance = form.save()
            return render(
                request,
                'projects/dashboard/daily_activities/includes/daily_activity_row.html',
                {'activity': instance}
            )
        else:
            return render(request, 'projects/dashboard/daily_activities/htmx/project_daily_activity_form.html', {
                'form': form,
                'project': project
            })

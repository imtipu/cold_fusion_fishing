from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import *

from projects.dashboard.forms import DailyActivityForm
from projects.models import *


class ProjectListView(ListView):
    template_name = 'projects/dashboard/project_list.html'

    model = Project
    context_object_name = 'projects'

    def get_queryset(self):
        return self.model.objects.select_related('tank').annotate(
            total_dead=models.Sum('daily_activities__dead_fish', output_field=models.IntegerField()),
            total_live=models.F('initial_quantity') - models.F('total_dead'),
        ).order_by('-start_date')


class ProjectDetailView(DetailView, DeleteView):
    template_name = 'projects/dashboard/project_detail.html'

    model = Project
    context_object_name = 'project'

    def get_queryset(self):
        queryset = Project.objects.select_related('tank').annotate(
            total_dead=models.Sum('daily_activities__dead_fish', output_field=models.IntegerField()),
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = context.get('project')
        context['form'] = DailyActivityForm(initial={'project': project})
        return context


class ProjectDailyActivityListView(ListView):
    template_name = 'projects/dashboard/daily_activities/project_daily_activity_list.html'

    model = DailyActivity
    context_object_name = 'daily_activities'

    def get_project(self):
        return Project.objects.get(pk=self.kwargs.get('pk'))

    def get_queryset(self):
        return self.model.objects.filter(
            project_id=self.kwargs.get('pk')
        ).select_related('project').order_by('-activity_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.get_project()
        return context


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
            cleaned_data = form.cleaned_data
            activity_date = cleaned_data.get('activity_date')
            daily_activities = DailyActivity.objects.filter(activity_date=activity_date, project=project)
            if daily_activities.exists():
                form.add_error('activity_date', 'Daily activity for this date already exists.')
                res = render(request, 'projects/dashboard/daily_activities/htmx/project_daily_activity_form.html', {
                    'form': form,
                    'project': project
                })
                return HttpResponse(res, status=400)
            first_activity = project.daily_activities.first()
            if first_activity:
                if activity_date < first_activity.activity_date:
                    form.add_error('activity_date', 'Activity date cannot be less than the first activity date.')
                    res = render(request, 'projects/dashboard/daily_activities/htmx/project_daily_activity_form.html', {
                        'form': form,
                        'project': project
                    })
                    return HttpResponse(res, status=400)

            initial_quantity = project.initial_quantity
            total_dead_qs = DailyActivity.objects.filter(project=project).aggregate(
                total_dead=models.Sum('dead_fish', output_field=models.IntegerField())
            )
            dead_fish = cleaned_data.get('dead_fish', 0)
            total_dead = total_dead_qs.get('total_dead', 0)
            if total_dead and dead_fish:
                total_dead = total_dead + int(dead_fish)
            else:
                total_dead = int(dead_fish)
            total_live_fish = initial_quantity - total_dead
            form.instance.project = project
            form.instance.live_fish = total_live_fish
            instance = form.save()
            total_days = project.daily_activities.count()

            res = render(
                request,
                'projects/dashboard/daily_activities/includes/daily_activity_row.html',
                {'activity': instance, 'project': project, 'days': total_days},
            )
            return HttpResponse(res)
        else:
            res = render(request, 'projects/dashboard/daily_activities/htmx/project_daily_activity_form.html', {
                'form': form,
                'project': project
            })
            return HttpResponse(res, status=400)


class ProjectDailyActivityDetailView(DetailView, DeleteView):
    model = DailyActivity
    context_object_name = 'activity'
    template_name = 'projects/dashboard/daily_activities/project_daily_activity_detail.html'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.htmx:
            instance.delete()
            return HttpResponse('', status=200)
        return super(self.__class__, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        instance = self.get_object()
        return reverse_lazy('dashboard:projects:project_detail', kwargs={'pk': instance.project.pk})

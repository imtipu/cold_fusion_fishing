from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.messages.views import SuccessMessageMixin

from projects.dashboard.forms import DailyActivityForm, ProjectForm, ProjectUpdateForm
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
            total_dead=models.Sum('daily_activities__dead_fish', output_field=models.IntegerField(), default=0),
            total_live=models.F('initial_quantity') - models.F('total_dead'),
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = context.get('project')
        context['form'] = DailyActivityForm(initial={'project': project})
        return context


class ProjectUpdateView(SuccessMessageMixin, UpdateView):
    model = Project
    template_name = 'projects/dashboard/update.html'
    form_class = ProjectUpdateForm
    context_object_name = 'project'
    success_message = _('Project Updated Successfully')

    def get_initial(self):
        initial = super().get_initial()
        initial['start_date'] = self.object.start_date.strftime('%Y-%m-%d')
        initial['end_date'] = self.object.end_date.strftime('%Y-%m-%d') if self.object.end_date else None
        return initial

    def get_success_url(self):
        return reverse_lazy('dashboard:projects:project_update', kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'projects/dashboard/create.html'
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = _('Create New Project')
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
        ).select_related(
            'project', 'project__tank', 'project__tank__current_project'
        ).order_by('-activity_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.get_project()
        return context


class DailyActivityAddView(CreateView):
    # template_name = 'projects/dashboard/daily_activities/project_daily_activity_form.html'

    model = DailyActivity
    form_class = DailyActivityForm

    def get_project_queryset(self):
        return Project.objects.annotate(
            total_dead=models.Sum('daily_activities__dead_fish', output_field=models.IntegerField(), default=0),
            total_live=models.F('initial_quantity') - models.F('total_dead'),
        )

    # success_url = reverse_lazy('dashboard:projects:project_detailprojects:project_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.get_project_queryset().get(pk=self.kwargs.get('pk'))
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
                if activity_date < project.start_date:
                    form.add_error('activity_date', 'Activity date cannot be less than project start date.')
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
            current_total_live_fish = initial_quantity - total_dead
            if dead_fish > current_total_live_fish:
                form.add_error('dead_fish', 'Dead fish cannot be greater than total live fish.')
                res = render(request, 'projects/dashboard/daily_activities/htmx/project_daily_activity_form.html', {
                    'form': form,
                    'project': project
                })
                return HttpResponse(res, status=400)
            if total_dead and dead_fish:
                total_dead = total_dead + int(dead_fish)
            else:
                total_dead = int(dead_fish)
            total_live_fish = initial_quantity - total_dead
            form.instance.project = project
            form.instance.expected_cn = project.expected_cn
            form.instance.live_fish = total_live_fish
            instance = form.save()
            start_date = project.start_date
            activity_date = instance.activity_date
            delta = activity_date - start_date
            day_number = delta.days + 1

            res = render(
                request,
                'projects/dashboard/daily_activities/includes/daily_activity_row.html',
                {'activity': instance, 'project': project, 'day_number': day_number},
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

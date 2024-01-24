from rest_framework.generics import *
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from projects.api.v1.serializers import *


class HomePageProjectListAPIView(ListAPIView):
    serializer_class = ProjectListSerializer
    queryset = Project.objects.none()

    def get_queryset(self):
        return Project.objects.select_related('tank').annotate(
            total_dead=models.Sum('daily_activities__dead_fish', output_field=models.IntegerField()),
            total_live=models.F('initial_quantity') - models.F('total_dead'),
        ).order_by('-start_date')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)


class ProjectListAPIView(ListCreateAPIView):
    serializer_class = ProjectListSerializer
    queryset = Project.objects.none()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectSerializer
        return ProjectListSerializer

    def get_queryset(self):
        return Project.objects.select_related('tank').annotate(
            total_dead=models.Sum('daily_activities__dead_fish', output_field=models.IntegerField()),
            total_live=models.F('initial_quantity') - models.F('total_dead'),
        ).order_by('-start_date')


class ProjectDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = ProjectListSerializer
    queryset = Project.objects.none()

    def get_queryset(self):
        return Project.objects.select_related('tank').annotate(
            total_dead=models.Sum('daily_activities__dead_fish', output_field=models.IntegerField()),
            total_live=models.F('initial_quantity') - models.F('total_dead'),
        ).order_by('-start_date')


# daily activities
class ProjectDailyActivityListAPIView(ListAPIView):
    serializer_class = DailyActivityListSerializer
    queryset = DailyActivity.objects.none()

    def get_queryset(self):
        return DailyActivity.objects.filter(project_id=self.kwargs.get('pk')).select_related(
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

    def get_project(self):
        return Project.objects.annotate(
            total_dead=models.Sum('daily_activities__dead_fish', output_field=models.IntegerField(), default=0),
            total_live=models.F('initial_quantity') - models.F('total_dead'),
        ).get(pk=self.kwargs.get('pk'))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

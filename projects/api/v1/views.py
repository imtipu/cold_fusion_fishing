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


class ProjectListAPIView(ListAPIView):
    serializer_class = ProjectListSerializer
    queryset = Project.objects.none()

    def get_queryset(self):
        return Project.objects.select_related('tank').annotate(
            total_dead=models.Sum('daily_activities__dead_fish', output_field=models.IntegerField()),
            total_live=models.F('initial_quantity') - models.F('total_dead'),
        ).order_by('-start_date')

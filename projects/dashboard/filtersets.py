import django_filters

from ..models import Project
from fish_tanks.models import FishTank


class ProjectFilterSet(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title')
    tank = django_filters.ModelChoiceFilter(
        field_name='tank',
        label='Tank',
        queryset=FishTank.objects.all(),
    )

    class Meta:
        model = Project
        fields = ['title']

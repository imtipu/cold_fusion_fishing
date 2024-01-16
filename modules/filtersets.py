import django_filters
from django.db import models
from rest_framework.filters import SearchFilter


class SearchFilterMixin(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_search',
        label='Search',
    )

    def filter_search(self, queryset, name, value):
        search_fields = getattr(self.Meta, 'search_fields', [])
        search_conditions = models.Q()
        for field in search_fields:
            search_conditions |= models.Q(**{f'{field}__icontains': value})

        queryset = queryset.filter(search_conditions)
        return queryset

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models


class AdminLoginRequiredMixin(LoginRequiredMixin):
    # login_url = '/accounts/login/'
    pass


class SearchViewMixin:
    search_fields = []

    def search_queryset(self):
        queryset = self.model.objects
        if len(self.search_fields) > 0:
            search = self.request.GET.get('search', None)
            if search is not None:
                search_conditions = models.Q()
                for field in self.search_fields:
                    search_conditions |= models.Q(**{f'{field}__icontains': search})
                queryset = queryset.filter(search_conditions)
        return queryset

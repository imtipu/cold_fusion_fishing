import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardNumberPagination(PageNumberPagination):
    # page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        page_size = self.request.query_params.get('page_size', None)
        if page_size:
            self.page_size = int(page_size)

        total_page = math.ceil(self.page.paginator.count / self.page_size)
        next_page_number = 1
        prev_page_number = 1
        if self.page.number < total_page:
            next_page_number = self.page.number + 1

        if self.page.number > 1:
            prev_page_number = self.page.number - 1

        return Response(
            {
                'count': self.page.paginator.count,
                'page_size': self.page_size,
                'total_page': total_page,
                'current_page': self.page.number,
                'next_page_number': next_page_number,
                'prev_page_number': prev_page_number,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data,
            }
        )

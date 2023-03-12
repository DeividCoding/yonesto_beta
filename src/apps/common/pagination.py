from rest_framework import pagination

from .responses import EnvelopeResponse


class EnvelopePagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"  # items per page

    def get_paginated_response(self, data):
        return EnvelopeResponse(
            data=data,
            links={"next": self.get_next_link(), "previous": self.get_previous_link()},
            count=self.page.paginator.count,
        )

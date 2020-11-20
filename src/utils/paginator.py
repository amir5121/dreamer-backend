from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination

from utils.dreamer_response import DreamerResponse


class DreamerPaginator(PageNumberPagination):
    def get_paginated_response(self, data):
        return DreamerResponse(
            data=OrderedDict(
                [
                    # ('count', 10000),
                    ('next', self.get_next_link()),
                    ('previous', self.get_previous_link()),
                    ('results', data)
                ]
            )
        ).toJSONResponse()

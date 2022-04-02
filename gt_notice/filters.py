from django_filters import rest_framework as filters
from .models import *


class NoticeFilter(filters.FilterSet):
    user = filters.NumberFilter(field_name="user",
                                lookup_expr='exact',
                                required=True)

    class Meta:
        model = Notice

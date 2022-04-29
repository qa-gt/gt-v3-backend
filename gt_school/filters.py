from .models import *
from django_filters import rest_framework as filters


class CalendarEventFilter(filters.FilterSet):
    start_time = filters.DateTimeFilter(field_name="start",
                                        lookup_expr='gte',
                                        required=True)
    end_time = filters.DateTimeFilter(field_name="start",
                                      lookup_expr='lte',
                                      required=True)

    class Meta:
        model = CalendarEvent
        fields = {}

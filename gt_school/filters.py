from .models import *
from django_filters import rest_framework as filters


class CalendarEventFilter(filters.FilterSet):
    min_state = filters.NumberFilter(field_name="state", lookup_expr='gte')

    class Meta:
        model = CalendarEvent
        fields = {
            'start': ['gte', 'lte', 'range'],
        }

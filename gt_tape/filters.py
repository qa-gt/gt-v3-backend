from django_filters import rest_framework as filters
from .models import *


class QuestionFilter(filters.FilterSet):
    box = filters.NumberFilter(field_name='box', lookup_expr='exact', required=True)

    class Meta:
        model = TapeQuestion
        fields = []

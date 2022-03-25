from django_filters import rest_framework as filters
from .models import *


class ArticleFilter(filters.FilterSet):
    min_state = filters.NumberFilter(field_name="state", lookup_expr='gte')

    class Meta:
        model = Article
        fields = {
            'state': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'author': ['exact'],
            'topic': ['exact'],
        }

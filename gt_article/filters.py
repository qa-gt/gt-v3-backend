from django_filters import rest_framework as filters
from .models import *


class TopicFilter(filters.FilterSet):
    min_state = filters.NumberFilter(field_name="state", lookup_expr='gte')

    class Meta:
        model = Topic
        fields = {
            'state': ['exact', 'gt', 'gte', 'lt', 'lte'],
        }


class ArticleFilter(filters.FilterSet):
    min_state = filters.NumberFilter(field_name="state", lookup_expr='gte')
    # q = filters.CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model = Article
        fields = {
            'state': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'author': ['exact'],
            'topic': ['exact'],
        }


class LikeFilter(filters.FilterSet):
    class Meta:
        model = Like
        fields = {
            'user': ['exact'],
            'article': ['exact'],
        }


class CommentFilter(filters.FilterSet):
    min_state = filters.NumberFilter(field_name="state", lookup_expr='gte')

    class Meta:
        model = Comment
        fields = {
            'state': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'author': ['exact'],
            'article': ['exact'],
        }

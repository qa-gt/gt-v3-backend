from django_filters.rest_framework import DjangoFilterBackend
from gt.permissions import IsAdminOrReadOnly
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import *
from rest_framework.viewsets import GenericViewSet, ModelViewSet, mixins

from .models import *
from .serializers import *
from .filters import *


class CalendarEventViewSet(ModelViewSet):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CalendarEventFilter
    search_fields = ['title', 'content']
    ordering_fields = ['start']

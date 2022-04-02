from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import *
from .serializers import *


class NoticeView(GenericViewSet, mixins.ListModelMixin):
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Notice.objects.filter(
            state__gte=NoticeStateChoices.DELETED,
            recipient=self.request.user).order_by('-time')[:20]

    @action(methods=['post'],
            detail=False,
            permission_classes=[IsAuthenticated],
            url_path='read')
    def read(self, request, pk=None):
        Notice.objects.filter(recipient=self.request.user).update(
            state=NoticeStateChoices.READ)
        return Response(status=200)

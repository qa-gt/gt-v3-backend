from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response

from .models import *
from .serializers import *


class NoticeView(GenericViewSet, mixins.ListModelMixin):
    serializer_class = NoticeSerializer

    def get_queryset(self):
        return Notice.objects.filter(
            state__gte=NoticeStateChoices.DELETED,
            recipient=self.request.user).order_by('-time')

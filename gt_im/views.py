from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from .models import *
from .serializers import *


class RoomView(GenericViewSet, mixins.ListModelMixin):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def list(self, request, *args, **kwargs):
        rooms = RoomMember.objects.filter(
            user=request.user).order_by('-room__last_message__time')
        return Response(MyRoomSerializer(rooms, many=True).data)

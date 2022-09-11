from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import *
from .serializers import *


class RoomView(GenericViewSet, mixins.ListModelMixin):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def list(self, request, *args, **kwargs):
        rooms = RoomMember.objects.filter(user=request.user)
        return Response(MyRoomSerializer(rooms, many=True).data)

    # @action(methods=['get'], detail=True, url_path='messages')
    # def get_messages(self, request, pk=None):
    #     room = self.get_object()
    #     messages = Message.objects.filter(room=room)
    #     return Response(MessageSerializer(messages, many=True).data)

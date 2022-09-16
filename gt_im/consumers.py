from urllib.parse import parse_qsl
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from gt._jwt import jdecode
from gt_user.models import User
from .models import Room, RoomMember, Message
from .serializers import MessageSerializer, MyRoomSerializer


class ImConsumer(JsonWebsocketConsumer):

    def connect(self):
        query = dict(parse_qsl(self.scope['query_string'].decode()))
        user_id = jdecode(query['jwt'][4:])['id']
        self.user = User.objects.get(id=user_id)

        group_add = async_to_sync(self.channel_layer.group_add)
        rooms = RoomMember.objects.filter(user=self.user)
        self.rooms = ['room_%s' % room.room.id for room in rooms]
        for room in self.rooms:
            group_add(room, self.channel_name)

        self.accept()

        rooms = rooms.order_by('-room__last_message__time')
        res = MyRoomSerializer(rooms, many=True).data
        for i in range(len(res)):
            message = Message.objects.filter(
                room_id=res[i]['room']['id']).order_by('-time')[:20]
            res[i]['message'] = MessageSerializer(message,
                                                  many=True).data[::-1]

        self.send_json({'action': 'init', 'data': res})

    def disconnect(self, close_code):
        group_discard = async_to_sync(self.channel_layer.group_discard)
        for room in self.rooms:
            group_discard(room, self.channel_name)

    def receive_json(self, content):
        action = content['action']
        data = content.get('data', {})

        if action == 'heartbeat':
            # self.send_json({'action': 'heartbeat'})
            return

        elif action == 'update_last_read_time':
            try:
                room_id = data['room_id']
                room = RoomMember.objects.get(user=self.user, room_id=room_id)
                room.last_read_time = data['last_read_time']
                room.save()
            except:
                ...

        elif action == 'new_message':
            if 'room_%s' % data['room_id'] not in self.rooms:
                self.send_json({
                    'action': 'error',
                    'data': 'You are not in this room.',
                })
                return
            room = Room.objects.get(id=data['room_id'])
            message = Message(
                sender=self.user,
                room=room,
                content=data['content'],
                content_type=data['content_type'],
            )
            message.save()
            room.last_message = message
            room.save()

            res = dict(MessageSerializer(message).data)
            res['room_id'] = data['room_id']
            async_to_sync(self.channel_layer.group_send)(
                'room_%s' % data['room_id'], {
                    'type': 'send_to_client',
                    'action': 'new_message',
                    'data': res
                })

        elif action == 'more_message':
            room_id = data['room_id']
            if 'room_%s' % room_id not in self.rooms:
                self.send_json({
                    'action': 'error',
                    'data': 'You are not in this room.',
                })
                return
            message = Message.objects.filter(
                room_id=room_id,
                time__lt=data['oldest_time']).order_by('-time')[:50]
            self.send_json({
                'action': 'more_message',
                'data': {
                    'room_id': room_id,
                    'message': MessageSerializer(message, many=True).data[::-1]
                },
            })

    def send_to_client(self, event):
        self.send_json(event)

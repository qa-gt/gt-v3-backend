from random import choices
from urllib.parse import parse_qsl

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.utils import timezone
from gt._jwt import jdecode
from gt_user.models import User

from .models import InviteCode, Message, Room, RoomMember
from .serializers import MessageSerializer, MyRoomSerializer, RoomSerializer


def get_random_string(length=8):
    return ''.join(choices(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        k=length,
    ))


class ImConsumer(JsonWebsocketConsumer):

    def connect(self):
        query = dict(parse_qsl(self.scope['query_string'].decode()))
        user_id = jdecode(query['jwt'][4:])['id']
        user = User.objects.get(id=user_id)
        if not user.is_authenticated or not user.is_active:
            self.send_json({
                'action': 'error',
                'data': 'Your account is not active.',
            })
            self.close()
            return
        self.user = user

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
            self.send_json({'action': 'heartbeat'})
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

        elif action == 'create_group':
            room = Room.objects.create(
                name=data['name'],
                avatar=data['avatar'],
                is_group=True,
            )
            RoomMember.objects.create(user=self.user, room=room, is_admin=True)
            code = get_random_string()
            while InviteCode.objects.filter(code=code).exists():
                code = get_random_string()
            InviteCode.objects.create(room=room, code=code, creator=self.user)
            message = Message.objects.create(
                room=room,
                content='您已成功创建群聊',
            )
            message.save()
            room.last_message = message
            room.save()

            self.send_json({
                'action': 'create_group',
                'data': {
                    'invite_code': code,
                },
            })

        elif action == 'join_group':
            try:
                code = InviteCode.objects.get(code=data['invite_code'])
                if code.expire_time and code.expire_time < timezone.now():
                    self.send_json({
                        'action': 'error',
                        'data': '邀请码已过期',
                    })
                    return
                RoomMember.objects.create(user=self.user, room=code.room)
                message = Message.objects.create(
                    room=code.room,
                    content=
                    f'{self.user.username} 通过 {code.creator.username} 的邀请码加入了群聊',
                )
                message.save()
                code.room.last_message = message
                code.room.save()

                res = dict(MessageSerializer(message).data)
                res['room_id'] = code.room.id
                async_to_sync(self.channel_layer.group_send)(
                    'room_%s' % code.room.id, {
                        'type': 'send_to_client',
                        'action': 'new_message',
                        'data': res
                    })
                self.send_json({
                    'action': 'join_group',
                    'data': RoomSerializer(code.room).data,
                })
            except:
                self.send_json({
                    'action': 'error',
                    'data': 'Invalid invite code.',
                })

    def send_to_client(self, event):
        self.send_json(event)

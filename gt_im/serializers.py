from rest_framework import serializers
from .models import *

from gt_user.serializers import SimpleUserSerializer


class ContentField(serializers.ReadOnlyField):

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        return value


class MessageSerializer(serializers.ModelSerializer):
    sender = SimpleUserSerializer()
    content = ContentField()

    class Meta:
        model = Message
        fields = read_only_fields = ('id', 'sender', 'content', 'content_type',
                                     'time', 'recalled_time')


class RoomSerializer(serializers.ModelSerializer):
    last_message = MessageSerializer()

    class Meta:
        model = Room
        fields = read_only_fields = ('id', 'name', 'avatar', 'is_group',
                                     'announcement', 'last_message')


class SimpleRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = read_only_fields = ('id', 'name', 'is_group')


class MyRoomSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    single_chat_with = SimpleUserSerializer()

    class Meta:
        model = RoomMember
        fields = read_only_fields = ('room', 'single_chat_with')

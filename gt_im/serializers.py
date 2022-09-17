from rest_framework import serializers
from .models import *

from gt_user.serializers import SimpleUserSerializer


class ContentField(serializers.ReadOnlyField):

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        return value


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = read_only_fields = ('id', 'name', 'size')


class MessageSerializer(serializers.ModelSerializer):
    sender = SimpleUserSerializer()
    content = ContentField()
    file = FileSerializer()

    class Meta:
        model = Message
        fields = read_only_fields = ('id', 'sender', 'content', 'content_type',
                                     'file', 'time', 'recalled_time')


class RoomSerializer(serializers.ModelSerializer):
    # last_message = MessageSerializer()

    class Meta:
        model = Room
        fields = read_only_fields = ('id', 'name', 'avatar', 'is_group',
                                     'announcement')


class SimpleRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = read_only_fields = ('id', 'name', 'is_group')


class UnreadField(serializers.ReadOnlyField):

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        return value


class MyRoomSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    single_chat_with = SimpleUserSerializer()
    unread = serializers.SerializerMethodField()

    class Meta:
        model = RoomMember
        fields = read_only_fields = ('room', 'single_chat_with', 'unread')

    def get_unread(self, obj):
        return Message.objects.filter(
            room=obj.room,
            time__gt=obj.last_read_time,
        ).count()

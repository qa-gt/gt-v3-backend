from rest_framework import serializers
from .models import *


class Followed(serializers.ReadOnlyField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        request = self.context.get('request')
        return value.filter(follower=request.user).exists()


class YunxiaoField(serializers.ReadOnlyField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        if value.show:
            return f'{value.real_name}({value.student_id[:4]}****)'
        return ''

class WeChatField(serializers.ReadOnlyField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        return f"{value.unique_id[:4]}****"


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'portrait')
        read_only_fields = ('id', 'username', 'portrait')


class UserSerializer(serializers.ModelSerializer):
    yunxiao = YunxiaoField()
    followed = Followed(source="follower")

    class Meta:
        model = User
        fields = ('id', 'username', 'tags', 'grade', 'gender', 'portrait',
                  'yunxiao', 'introduction', 'followed')
        read_only_fields = ('id', 'username', 'tags', 'grade', 'gender',
                            'portrait', 'yunxiao', 'introduction')


class DetailUserSerializer(serializers.ModelSerializer):
    yunxiao = YunxiaoField()
    wechat = WeChatField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'grade', 'gender', 'introduction', 'tags',
            'portrait', 'ban_state', 'is_staff', 'is_superuser', 'yunxiao',
            'wechat', 'email'
        ]
        read_only_fields = ('id', 'username', 'yunxiao', 'wechat')


class FollowSerializer(serializers.ModelSerializer):
    follower = SimpleUserSerializer(read_only=True)
    following = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('follower', 'following')
        read_only_fields = ('follower', 'following')


class FollowerSerializer(serializers.ModelSerializer):
    follower = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('follower', )
        read_only_fields = ('follower', )


class FollowingSerializer(serializers.ModelSerializer):
    following = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('following', )
        read_only_fields = ('following', )


class DetailFollowSerializer(serializers.ModelSerializer):
    follower = SimpleUserSerializer(read_only=True)
    following = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following', 'follow_time')
        read_only_fields = ('id', 'follower', 'following', 'follow_time')

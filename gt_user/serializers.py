from rest_framework import serializers
from .models import *


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'portrait')
        read_only_fields = ('id', 'username', 'portrait')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'tags', 'grade', 'gender', 'portrait')
        read_only_fields = ('id', 'username', 'tags', 'grade', 'gender',
                            'portrait')


class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'grade', 'gender', 'introduction', 'tags',
            'portrait', 'email', 'ban_state', 'is_staff', 'is_superuser'
        ]
        read_only_fields = (
            'id',
            'username',
        )


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
        fields = ('following',)
        read_only_fields = ('following', )


class DetailFollowSerializer(serializers.ModelSerializer):
    follower = SimpleUserSerializer(read_only=True)
    following = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following', 'follow_time')
        read_only_fields = ('id', 'follower', 'following', 'follow_time')

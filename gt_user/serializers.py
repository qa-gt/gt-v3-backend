from rest_framework import serializers
from .models import *


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
        read_only_fields = ('id', 'username')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'tags', 'grade', 'gender')
        read_only_fields = ('id', 'username', 'tags', 'grade', 'gender')


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

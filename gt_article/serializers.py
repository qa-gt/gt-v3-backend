from rest_framework import serializers
from .models import *

from gt_user.serializers import UserSerializer, SimpleUserSerializer


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = Like
        fields = ('user', )


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    topic = TopicSerializer(required=False)
    like = LikeSerializer(many=True, required=False)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'author', 'create_time', 'update_time')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)

    class Meta:
        model = Comment
        fields = '__all__'

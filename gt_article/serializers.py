from rest_framework import serializers
from .models import *

from gt_user.serializers import *


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    # user = SimpleUserSerializer()
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Like
        fields = ('user', )


class SimpleCommentSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'author')


class CommentSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(required=False)
    reply = SimpleCommentSerializer(required=False)

    class Meta:
        model = Comment
        exclude = ('article', )


class SimpleArticleSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer()

    class Meta:
        model = Article
        fields = ('id', 'author', 'title', 'read_count', 'update_time')


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    topic = TopicSerializer(required=False, default=Topic.objects.get(id=0))
    like = LikeSerializer(many=True, required=False)
    comment = CommentSerializer(many=True, required=False)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'author', 'create_time', 'update_time',
                            'read_count', 'like', 'comment')

from email.policy import default
from rest_framework import serializers
from .models import *

from gt_user.serializers import *


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class SimpleArticleSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer()

    class Meta:
        model = Article
        fields = ('id', 'author', 'title', 'read_count', 'update_time')


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    topic = TopicSerializer(required=False)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'author', 'create_time', 'update_time',
                            'read_count', 'topic')


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


class DetailCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    reply = CommentSerializer(required=False, default=None)
    article = SimpleArticleSerializer(required=False)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'author', 'time')


class LikeSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = Like
        fields = ('user', )


class DetailLikeSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(required=False)
    article = serializers.IntegerField(source='article.id', required=False)
    comment = serializers.IntegerField(source='comment.id', required=False)

    class Meta:
        model = Like
        fields = ('id', 'user', 'article', 'comment')
        read_only_fields = ('id', 'user')


class CollectSerializer(serializers.ModelSerializer):
    article = SimpleArticleSerializer(required=False)

    class Meta:
        model = Collect
        fields = ('article', )
        read_only_fields = ('id', 'user')

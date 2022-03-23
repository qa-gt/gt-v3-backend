from django.utils import timezone
from gt.permissions import *
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from .models import *
from .permissions import *
from .serializers import *


class TopicViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAdminOrReadOnly]


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ArticlePermission]

    def get_queryset(self):
        page = self.request.data.get('page') or 'index'
        state = {
            'index':
            (ArticleStateChoices.HIDE_INDEX, ArticleStateChoices.TOP_INDEX),
            'topic':
            (ArticleStateChoices.HIDE_TOPIC, ArticleStateChoices.TOP_TOPIC),
            'user':
            (ArticleStateChoices.HIDE_USER, ArticleStateChoices.TOP_USER),
        }
        queryset = self.queryset.filter(
            state__gte=state[page][0]).order_by('-create_time')
        topset = self.queryset.filter(state__gte=state[page][1])
        return queryset | topset

    def perform_create(self, serializer):
        if self.request.data.get('topic'):
            topic = Topic.objects.filter(id=self.request.data['topic'])
            if topic.exists():
                serializer.save(author=self.request.user, topic=topic.first())
                return
        serializer.save(author=self.request.user, topic_id=0)

    def perform_update(self, serializer):
        if self.request.data.get('topic'):
            topic = Topic.objects.filter(id=self.request.data['topic'])
            if topic.exists():
                serializer.save(topic=topic.first())
                return
        serializer.save(topic_id=0)

    def perform_destroy(self, instance):
        instance.save(state=ArticleStateChoices.DELETE)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [NoEdit, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.save(state=TopicCommentStateChoices.DELETE)


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [NoEdit, IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        Like.objects.get_or_create(user=request.user,
                                   article_id=request.data['article'])
        return

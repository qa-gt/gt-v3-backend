from xml.etree.ElementTree import QName
from gt.permissions import *
from gt.authentications import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .permissions import *
from .serializers import *
from .filters import *


class TopicViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAdminOrReadOnly]


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly, ArticlePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleArticleSerializer
        return ArticleSerializer

    def perform_create(self, serializer):
        print(serializer)
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
    queryset = Comment.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly, NoEdit, CommentPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentSerializer
        return DetailCommentSerializer

    def perform_create(self, serializer):
        author = self.request.user
        article_id = self.request.data['article']
        reply = self.request.data.get('reply')
        reply = reply and Comment.objects.filter(id=reply)
        reply = reply and reply.exists() and reply.first()
        reply = reply and reply.article.id == int(article_id) and reply or None
        serializer.save(author=author, article_id=article_id, reply=reply)

    def perform_destroy(self, instance):
        instance.save(state=TopicCommentStateChoices.DELETE)


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all().order_by('-id')
    permission_classes = [NoEdit, IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = LikeFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return LikeSerializer
        return DetailLikeSerializer

    def create(self, request, *args, **kwargs):
        if request.data.get('article'):
            article = Article.objects.filter(id=request.data['article'])
            if article.exists():
                article = article.first()
            else:
                return Response({
                    'status': 'error',
                    'detail': '文章不存在!'
                })
            if article.like.filter(user=request.user).exists():
                article.like.filter(user=request.user).first().delete()
                return Response({
                    'status': 'success',
                    'opt': 'cancel',
                    'detail': '取消成功!'
                })
            article.like.get_or_create(user=request.user)
            return Response({'status': 'success', 'opt': 'add', 'detail': '点赞成功!'})
        elif request.data.get('comment'):
            Like.objects.get_or_create(user=request.user,
                                       comment_id=request.data['comment'])
        return

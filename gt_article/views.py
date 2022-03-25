from gt.permissions import *
from rest_framework.exceptions import ValidationError
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
    queryset = Article.objects.all()
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

    @action(detail=True,
            methods=['post'],
            permission_classes=[IsAuthenticated],
            url_path='like')
    def like(self, request, pk=None):
        article = self.get_object()
        if article.like.filter(user=request.user).exists():
            article.like.filter(user=request.user).first().delete()
            return Response({
                'status': 'success',
                'opt': 'deleted',
                'detail': '取消成功!'
            })
        article.like.get_or_create(user=request.user)
        return Response({
            'status': 'success',
            'opt': 'added',
            'detail': '点赞成功!'
        })

    @action(detail=True,
            methods=['post'],
            permission_classes=[IsAuthenticated],
            url_path='add_comment')
    def add_comment(self, request, pk=None):
        article = self.get_object()
        reply = request.data.get('reply') and Comment.objects.filter(
            id=request.data['reply'])
        if reply.exists() and reply.first().article == article:
            comment = article.comment.create(author=request.user,
                                             content=request.data['content'],
                                             reply=reply.first())
        else:
            comment = article.comment.create(author=request.user,
                                             content=request.data['content'])
        return Response({
            'status':
            'success',
            'comment':
            CommentSerializer().to_representation(comment)
        })


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [NoEdit, IsAuthenticatedOrReadOnly, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.save(state=TopicCommentStateChoices.DELETE)


# class LikeViewSet(ModelViewSet):
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer
#     permission_classes = [NoEdit, IsAuthenticatedOrReadOnly, IsAdminUser]

#     def create(self, request, *args, **kwargs):
#         Like.objects.get_or_create(user=request.user,
#                                    article_id=request.data['article'])
#         return

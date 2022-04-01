from gt.permissions import *
from gt.authentications import *
from rest_framework.permissions import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.utils import timezone

from .models import *
from .permissions import *
from .serializers import *
from .filters import *


class TopicViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = TopicFilter
    queryset = Topic.objects.all().order_by('id')
    serializer_class = TopicSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.filter(
        state__gt=ArticleStateChoices.HIDE).order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly, ArticlePermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ArticleFilter
    search_fields = ['title', 'content']

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleArticleSerializer
        return ArticleSerializer

    def perform_create(self, serializer):
        if self.request.data.get('_topic'):
            topic = Topic.objects.filter(id=self.request.data['_topic'])
            if topic.exists():
                serializer.save(author=self.request.user, topic=topic.first())
                return
        serializer.save(author=self.request.user, topic_id=0)

    def perform_update(self, serializer):
        if self.request.data.get('_topic'):
            topic = Topic.objects.filter(id=self.request.data['_topic'])
            if topic.exists():
                serializer.save(topic=topic.first(),
                                update_time=timezone.now())
                return
        serializer.save(topic_id=0, update_time=timezone.now())

    def perform_destroy(self, instance):
        instance.state = ArticleStateChoices.DELETE
        instance.save()

    @action(methods=['patch'],
            detail=True,
            authentication_classes=[],
            permission_classes=[],
            url_path='read')
    def add_read_count(self, request, pk=None):
        article = self.get_object()
        article.read_count += 1
        article.save()
        return Response(status=200)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.filter(state__gte=0).order_by('id')
    permission_classes = [IsAuthenticatedOrReadOnly, NoEdit, CommentPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentSerializer
        return DetailCommentSerializer

    def create(self, request, *args, **kwargs):
        content = request.data['content']
        author = request.user
        article_id = request.data['article']
        reply = request.data.get('reply')
        reply = reply and Comment.objects.filter(id=reply)
        reply = reply and reply.exists() and reply.first()
        reply = reply and reply.article.id == int(article_id) and reply or None
        Comment.objects.create(author=author,
                               article_id=article_id,
                               reply=reply,
                               content=content)
        return Response(status=201)

    def perform_destroy(self, instance):
        instance.save(state=TopicCommentStateChoices.DELETE)


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all().order_by('id')
    permission_classes = [NoEdit, IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = LikeFilter
    pagination_class = None

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
                return Response({'status': 'error', 'detail': '文章不存在!'})
            if article.like.filter(user=request.user).exists():
                article.like.filter(user=request.user).first().delete()
                return Response({
                    'status': 'success',
                    'opt': 'cancel',
                    'detail': '取消成功!'
                })
            article.like.get_or_create(user=request.user)
            return Response({
                'status': 'success',
                'opt': 'add',
                'detail': '点赞成功!'
            })
        elif request.data.get('comment'):
            Like.objects.get_or_create(user=request.user,
                                       comment_id=request.data['comment'])
        return


class CollectView(mixins.ListModelMixin, GenericViewSet):
    queryset = Collect.objects.all().order_by('id')
    serializer_class = CollectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, CollectPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CollectFilter
    search_fields = ['article__title', 'article__content']

    def create(self, request, *args, **kwargs):
        article = Article.objects.filter(id=request.data['article'])
        if article.exists():
            article = article.first()
        else:
            return Response({'status': 'error', 'detail': '文章不存在!'})
        Collect.objects.get_or_create(user=request.user, article=article)
        return Response({'status': 'success', 'detail': '收藏成功!'})

    def destroy(self, request, *args, **kwargs):
        article = Article.objects.filter(id=request.data['article'])
        if article.exists():
            article = article.first()
        else:
            return Response({'status': 'error', 'detail': '文章不存在!'})
        collect = Collect.objects.filter(user=request.user, article=article)
        if collect.exists():
            collect.first().delete()
            return Response({'status': 'success', 'detail': '取消成功!'})
        else:
            return Response({'status': 'error', 'detail': '收藏不存在!'})

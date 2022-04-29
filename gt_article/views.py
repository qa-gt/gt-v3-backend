import datetime
from random import randint

from django.conf import settings
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from gt.authentications import *
from gt.permissions import *
from gt.permissions import RequireWeChat, RobotCheck
from gt_notice.options import add_notice
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, mixins

from .filters import *
from .models import *
from .permissions import *
from .serializers import *


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
    permission_classes = [
        IsAuthenticatedOrReadOnly, ArticlePermission, RobotCheck, RequireWeChat
    ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ArticleFilter
    search_fields = ['title', 'content']
    ordering_fields = ['state', 'create_time', 'id']

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleArticleSerializer
        return ArticleSerializer

    def perform_create(self, serializer):
        start_time = timezone.now() - datetime.timedelta(days=1)
        articles_count = self.request.user.article.filter(
            create_time__gt=start_time).count()
        throttle = settings.ARTICLE_CREATE_THROTTLE[0 if self.request.user.
                                                    wechat else 1]
        if articles_count > throttle:
            raise ValidationError({
                'status': 'error',
                'detail': '近24小时发帖次数已达上限'
            })
        topic = Topic.objects.get(id=self.request.data['_topic'])
        serializer.save(author=self.request.user, topic=topic)

    def perform_update(self, serializer):
        topic = Topic.objects.get(id=self.request.data['_topic'])
        serializer.save(topic=topic, update_time=timezone.now())

    def perform_destroy(self, instance):
        instance.state = ArticleStateChoices.DELETE
        instance.save()

    @action(methods=['patch'],
            detail=True,
            permission_classes=[],
            url_path='read')
    def add_read_count(self, request, pk=None):
        article = self.get_object()
        article.read_count += 1
        article.save()
        return Response(status=200)

    @action(methods=['get'],
            detail=False,
            url_path='random',
            permission_classes=[])
    def get_random_article(self, request):
        count = request.data.get('len', 10)
        atcs = Article.objects.filter(state__gt=ArticleStateChoices.HIDE)
        start = randint(0, max(atcs.count() - count, 0))
        return Response(
            SimpleArticleSerializer(atcs[start:start + count], many=True).data)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.filter(state__gte=0).order_by('id')
    permission_classes = [
        IsAuthenticatedOrReadOnly, NoEdit, CommentPermission, RobotCheck,
        RequireWeChat
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentSerializer
        return DetailCommentSerializer

    def create(self, request, *args, **kwargs):
        content = request.data['content']
        author = request.user
        atc_id = request.data['article']
        reply = request.data.get('reply')
        reply = reply and Comment.objects.filter(id=reply)
        reply = reply and reply.exists() and reply.first()
        reply = reply and reply.article.id == int(atc_id) and reply or None
        Comment.objects.create(author=author,
                               article_id=atc_id,
                               reply=reply,
                               content=content)
        atc_author = Article.objects.get(id=atc_id).author
        if reply:
            if reply.author != atc_author:
                add_notice(
                    atc_author,
                    f"{author.username}评论了你的文章",
                    f"回复{reply.author.username}的评论：{content}",
                    f"/article/{atc_id}",
                )
            if reply.author != author:
                add_notice(
                    reply.author,
                    f"{author.username}回复了你的评论",
                    f"回复内容：{content}",
                    f"/article/{atc_id}",
                )
        else:
            if atc_author != author:
                add_notice(
                    atc_author,
                    f"{author.username}评论了你的文章",
                    f"评论内容：{content}",
                    f"/article/{atc_id}",
                )
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
                return Response({'status': 'error', 'detail': '文章不存在！'})
            if article.like.filter(user=request.user).exists():
                article.like.filter(user=request.user).first().delete()
                return Response({
                    'status': 'success',
                    'opt': 'cancel',
                    'detail': '取消成功！'
                })
            article.like.get_or_create(user=request.user)
            if article.author != request.user:
                add_notice(
                    article.author,
                    f"{request.user.username}点赞了你的文章",
                    f"文章标题：{article.title}",
                    f"/article/{article.id}",
                )
            return Response({
                'status': 'success',
                'opt': 'add',
                'detail': '点赞成功！'
            })
        elif request.data.get('comment'):
            Like.objects.get_or_create(user=request.user,
                                       comment_id=request.data['comment'])
            return Response({
                'status': 'success',
                'opt': 'add',
                'detail': '点赞成功！'
            })


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
            return Response({'status': 'error', 'detail': '文章不存在！'})
        Collect.objects.get_or_create(user=request.user, article=article)
        return Response({'status': 'success', 'detail': '收藏成功！'})

    def destroy(self, request, *args, **kwargs):
        Collect.objects.filter(user=request.user,
                               article_id=request.GET['article']).delete()
        return Response({'status': 'success', 'detail': '取消成功！'})

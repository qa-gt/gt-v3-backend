from re import search
from django.utils import timezone

from django.contrib.auth import authenticate
from gt import jencode
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins, ReadOnlyModelViewSet
from rest_framework.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from gt.permissions import RobotCheck

from .models import *
from .permissions import *
from .serializers import *


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError({'detail': '用户名或密码错误'})
        if not user.is_active:
            raise ValidationError({'detail': '用户被封禁'})
        user.last_login = timezone.now()
        user.save()
        return Response({
            'status': 'success',
            'detail': '登录成功',
            'token': jencode({'id': user.id}),
            'user': DetailUserSerializer(user).data
        })


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [RobotCheck]

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({'status': 'error', 'detail': '该用户名已被注册!'})
        user = User.objects.create_user(username=username, password=password)
        return Response({
            'status': 'success',
            'detail': '注册成功',
            'token': jencode({'id': user.id}),
            'user': DetailUserSerializer(user).data
        })


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = DetailUserSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticatedOrReadOnly, UserPermission]
    filterset_fields = [
        'username', 'is_active', 'ban_state', 'is_staff', 'is_superuser'
    ]

    def perform_destroy(self, instance):
        instance.save(state=BanStateChoices.NO_LOGIN)

    @action(methods=['post'],
            detail=True,
            permission_classes=[IsAuthenticated],
            url_path='follow')
    def follow(self, request, pk=None):
        user = self.get_object()
        follow = user.following.filter(follower=request.user)
        if not follow.exists():
            Follow.objects.create(follower=request.user, following=user)
        return Response({'status': 'success', 'detail': '关注成功'})

    @action(methods=['post'],
            detail=True,
            permission_classes=[IsAuthenticated],
            url_path='unfollow')
    def unfollow(self, request, pk=None):
        user = self.get_object()
        user.following.filter(follower=request.user).delete()
        return Response({'status': 'success', 'detail': '取消关注成功'})


class FollowView(ReadOnlyModelViewSet):
    queryset = Follow.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['follower', 'following']
    search_fields = [
        'follower__username', 'following__username', 'follower__id',
        'following__id'
    ]

    def get_serializer_class(self):
        if self.action == 'list':
            if self.request.GET.get('following'):
                return FollowerSerializer
            elif self.request.GET.get('follower'):
                return FollowingSerializer
            return FollowSerializer
        return DetailFollowSerializer

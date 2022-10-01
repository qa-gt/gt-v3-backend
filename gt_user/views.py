import uuid

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from gt import jencode
from gt.permissions import RobotCheck
from gt_im.models import Room, RoomMember, Message
from gt_notice.options import add_notice
from requests import get
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.parsers import FormParser
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import *
from .permissions import *
from .serializers import *
from .yunxiao import yx_login


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')
        expire_time = request.data.get('expire_time', 0)
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed({
                'status': 'forbidden',
                'detail': '用户名或密码错误'
            })
        if (not user.is_active) or (user.wechat and not user.wechat.is_active):
            raise AuthenticationFailed({
                'status': 'forbidden',
                'detail': '用户被封禁'
            })
        user.last_login = timezone.now()
        user.save()
        return Response({
            'status': 'success',
            'detail': '登录成功',
            'token': jencode({'id': user.id}, expire_time),
            'user': DetailUserSerializer(user).data
        })


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        user = request.user
        if not user.check_password(old_password):
            raise AuthenticationFailed({
                'status': 'forbidden',
                'detail': '旧密码错误'
            })
        user.set_password(new_password)
        user.save()
        return Response({
            'status': 'success',
            'detail': '密码修改成功',
        })


class OAuthLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed({
                'status': 'forbidden',
                'detail': '用户名或密码错误'
            })
        if (not user.is_active) or (user.wechat and not user.wechat.is_active):
            raise AuthenticationFailed({
                'status': 'forbidden',
                'detail': '用户被封禁'
            })
        user.last_login = timezone.now()
        user.save()
        token = str(
            uuid.uuid5(uuid.NAMESPACE_DNS, f"{user.id}:{user.last_login}"))
        cache_key = "oauth-" + str(token)
        cache.set(cache_key, user.id, 30)
        return Response({
            'status': 'success',
            'detail': '登录成功',
            'token': token
        })


class OAuthCallbackView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        if request.data.get('server') not in ['ctf']:
            raise AuthenticationFailed({
                'status': 'forbidden',
                'detail': '非法请求'
            })
        token = request.data.get('token')
        cache_key = "oauth-" + str(token)
        user_id = cache.get(cache_key)
        user = User.objects.filter(id=user_id)
        if not token or not user_id or not user.exists():
            raise ValidationError({'status': 'fail', 'detail': 'token错误或已过期'})
        user = user.first()
        cache.delete(cache_key)
        return Response({
            'status': 'success',
            'detail': '登录成功',
            'user': DetailUserSerializer(user).data
        })


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [RobotCheck]

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')
        cache_key = f"register-{request.ip}"
        register_count = int(cache.get(cache_key, 0))
        if register_count > 500:
            return Response({'status': 'error', 'detail': '当日只能注册账号数已达上限！'})
        if User.objects.filter(username=username).exists():
            return Response({'status': 'error', 'detail': '该用户名已被注册！'})
        user = User.objects.create_user(username=username, password=password)
        cache.set(cache_key, register_count + 1, 24 * 3600)
        return Response({
            'status': 'success',
            'detail': '注册成功',
            'token': jencode({'id': user.id}),
            'user': DetailUserSerializer(user).data
        })


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [IsAuthenticatedOrReadOnly, UserPermission]
    filterset_fields = [
        'username', 'is_active', 'ban_state', 'is_staff', 'is_superuser'
    ]
    search_fields = ['id', 'username', 'email']

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return DetailUserSerializer
        return UserSerializer

    def perform_destroy(self, instance):
        instance.save(active=False)

    @action(methods=['post'],
            detail=True,
            permission_classes=[IsAuthenticated],
            url_path='follow')
    def follow(self, request, pk=None):
        user = self.get_object()
        follow = user.follower.filter(follower=request.user)
        if not follow.exists():
            Follow.objects.create(follower=request.user, following=user)
        add_notice(
            user,
            '有人关注了你',
            f'{request.user.username}关注了你',
            f'/user/{user.id}',
        )

        # 创建私聊房间
        room = RoomMember.objects.filter(user=request.user,
                                         single_chat_with=user)
        if not room.exists():
            room = Room.objects.create()
            RoomMember.objects.create(user=request.user,
                                      room=room,
                                      single_chat_with=user)
            RoomMember.objects.create(user=user,
                                      room=room,
                                      single_chat_with=request.user)
            Message.objects.create(
                room=room,
                content=f'你们已经成为好友，可以开始聊天了',
            )

        return Response({'status': 'success', 'detail': '关注成功'})

    @action(methods=['post'],
            detail=True,
            permission_classes=[IsAuthenticated],
            url_path='unfollow')
    def unfollow(self, request, pk=None):
        user = self.get_object()
        user.follower.filter(follower=request.user).delete()
        return Response({'status': 'success', 'detail': '取消关注成功'})

    @action(methods=['post'],
            detail=False,
            permission_classes=[IsAuthenticated],
            url_path='yunxiao_auth')
    def yunxiao_auth(self, request, pk=None):
        show = request.data.get('show') == 'true'
        if request.user.yunxiao_state:
            yunxiao = Yunxiao.objects.get(user=request.user)
            yunxiao.show = show
            yunxiao.save()
            request.user.yunxiao = yunxiao
            return Response({
                'status': 'success',
                'detail': '实名信息展示状态更新成功',
                'user': DetailUserSerializer(request.user).data
            })
        student_id = request.data.get('student_id')
        password = request.data.get('password')
        if not student_id or not password:
            return Response({'status': 'error', 'detail': '用户名或密码不能为空'})
        r = yx_login(student_id, password)
        if r['status'] != 'success':
            return Response({'status': 'error', 'detail': r['msg']})
        r = r['data']
        if Yunxiao.objects.filter(student_id=student_id).exists():
            return Response({'status': 'error', 'detail': '该学号已被绑定'})
        yunxiao = Yunxiao(
            user=request.user,
            student_id=student_id,
            uid=r['user_id'],
            real_name=r['real_name'],
            mobile=r['mobile'],
            show=show,
            role=r['role'],
            gender=r['gender'],
        )
        yunxiao.save()
        return Response({
            'status': 'success',
            'detail': '认证成功',
            'user': DetailUserSerializer(request.user).data
        })

    @action(methods=['get'],
            detail=False,
            permission_classes=[IsAuthenticated],
            url_path='wechat_auth')
    def wechat_auth(self, request):
        get_qrcode = request.query_params.get('qrcode') is not None
        if get_qrcode:
            r = get(
                'https://server01.vicy.cn/8lXdSX7FSMykbl9nFDWESdc6zfouSAEz/wxLogin/tempUserId',
                {
                    'secretKey': settings.VICY_SECRET
                }).json()['data']
            cache.set(f'wechat-{request.user.id}', r['tempUserId'], 10 * 60)
            return Response({
                'status': 'success',
                'data': {
                    'qrCode': r['qrCodeReturnUrl'],
                }
            })
        temp_uid = cache.get(f'wechat-{request.user.id}')
        cache_key = f'wechat-{temp_uid}'
        unique_id = cache.get(cache_key)
        if unique_id is None:
            return Response({'status': 'success', 'detail': 'pending'})
        WeChat.objects.get_or_create(unique_id=unique_id)
        request.user.wechat = WeChat.objects.get(unique_id=unique_id)
        request.user.save()
        cache.delete(cache_key)
        return Response({
            'status': 'success',
            'detail': 'success',
            'user': DetailUserSerializer(request.user).data
        })

    @action(methods=['post'],
            detail=False,
            authentication_classes=[],
            permission_classes=[],
            parser_classes=[FormParser],
            url_path='wechat_update')
    def wechat_update(self, request):
        cache.set(f'wechat-{request.data["tempUserId"]}',
                  request.data["userId"], 10 * 60)
        return Response({'errcode': 0, 'message': '验证成功'})


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

import datetime

from django.contrib.auth import authenticate
from django.shortcuts import render
from gt import jencode
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import *
from .permissions import *
from .serializers import *


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError({"detail": "用户名或密码错误"})
        if not user.is_active:
            raise ValidationError({"detail": "用户被封禁"})
        return Response({
            "token":
            jencode({
                "id": user.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            }),
            "user":
            UserSerializer(user).data
        })


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.create_user(username=username, password=password)
        return Response({
            "detail": "注册成功",
            "token":
            jencode({
                "id": user.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            }),
            "user":
            UserSerializer(user).data
        })


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

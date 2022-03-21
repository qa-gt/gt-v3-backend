import datetime
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
        user = User.objects.filter(username=username)
        if not user:
            print(username, password)
            raise ValidationError({"detail": "用户名未找到"})
        user = user.first()
        if user.state <= -3:
            raise ValidationError({"detail": "用户被封禁"})
        elif user.pwd != password:
            raise ValidationError({"detail": "密码错误"})
        return Response({
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

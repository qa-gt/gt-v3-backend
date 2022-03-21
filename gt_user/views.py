from django.shortcuts import render

from .models import *

from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

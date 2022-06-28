from rest_framework import serializers
from .models import *


class LiveInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveInfo
        fields = '__all__'


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'

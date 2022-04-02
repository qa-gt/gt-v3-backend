from rest_framework import serializers
from .models import *


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        exclude = ('recipient', )

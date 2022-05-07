from rest_framework import serializers
from .models import *

from gt_user.serializers import SimpleUserSerializer


class TapeReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = TapeReply
        fields = '__all__'


class TapeBoxSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = TapeBox
        fields = '__all__'
        read_only_fields = ('id', 'user')


class TapeQuestionSerializer(serializers.ModelSerializer):
    reply = TapeReplySerializer(many=True)

    class Meta:
        model = TapeQuestion
        exclude = ('token',)


class TapeQuestionCreatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TapeQuestion
        fields = '__all__'

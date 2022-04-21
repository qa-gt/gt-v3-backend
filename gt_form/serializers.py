from rest_framework import serializers
from .models import *

from gt_user.serializers import SimpleUserSerializer


class Followed(serializers.ReadOnlyField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        request = self.context.get('request')
        return value.filter(follower=request.user).exists()


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = ('id', 'num', 'title')


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, source='choice')

    class Meta:
        model = Question
        fields = ('id', 'title', 'type', 'choices')


class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source='question')
    creator = SimpleUserSerializer()

    class Meta:
        model = Form
        fields = '__all__'

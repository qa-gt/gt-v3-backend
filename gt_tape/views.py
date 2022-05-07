import string
import random
from .models import *
from .serializers import *
from .filters import QuestionFilter
from .permissions import TapeBoxPermission
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from gt.permissions import *
from gt_notice.options import add_notice
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins


def random_string(length=10):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


class TapeBoxViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = TapeBox.objects.all()
    serializer_class = TapeBoxSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, TapeBoxPermission)


class TapeQuestionViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = TapeQuestion.objects.all().order_by('-time')
    serializer_class = TapeQuestionSerializer
    permission_classes = [RobotCheck, NoEdit]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = QuestionFilter

    @staticmethod
    def create(request, *args, **kwargs):
        try:
            question = TapeQuestion(box=TapeBox.objects.get(id=request.data['box']), content=request.data['content'],
                                    author=request.user, token=random_string())
            question.save()
        except TapeBox.DoesNotExist:
            raise ValidationError('问题创建失败')
        return Response(TapeQuestionCreatingSerializer(question).data, status=201)


class TapeReplyViewSet(GenericViewSet):
    queryset = TapeReply.objects.all()
    permission_classes = [RobotCheck, NoEdit]

    @staticmethod
    def create(request, *args, **kwargs):
        try:
            question = TapeQuestion.objects.get(id=request.data['question'])
            if request.data['token'] != question.token and (not request.user or request.user != question.author):
                raise AuthenticationFailed('提问者身份验证失败')
            reply = TapeReply(question=question, content=request.data['content'],
                              is_owner=request.user == question.box.user)
            reply.save()
        except TapeQuestion.DoesNotExist:
            raise ValidationError('回复失败')
        return Response(status=201)

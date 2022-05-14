import string
import random
from .models import *
from .serializers import *
from .filters import QuestionFilter
from .permissions import TapeBoxPermission
from django_filters.rest_framework import DjangoFilterBackend
from gt.permissions import *
from gt_notice.options import add_notice
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins


def random_string(length=10):
    return ''.join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(length))


class TapeBoxViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                     GenericViewSet):
    queryset = TapeBox.objects.all()
    serializer_class = TapeBoxSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, TapeBoxPermission)

    def create(self, request, *args, **kwargs):
        if TapeBox.objects.filter(user=request.user).exists():
            raise ValidationError('您的TapeBox已经存在')
        tape_box = TapeBox(user=request.user,
                           title=request.data['title'],
                           image=request.data['image'])
        tape_box.save()
        return Response(TapeBoxSerializer(tape_box).data)

    @action(detail=False,
            methods=['GET'],
            permission_classes=[IsAuthenticated],
            url_path='me')
    def get_my_tape_box(self, request):
        tape_box = TapeBox.objects.filter(user=request.user)
        if tape_box.exists():
            return Response(TapeBoxSerializer(tape_box.first()).data)
        return Response({'not_found': True})


class TapeQuestionViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = TapeQuestion.objects.all().order_by('-time')
    serializer_class = TapeQuestionSerializer
    permission_classes = [RobotCheck, NoEdit]
    filter_backends = (DjangoFilterBackend, )
    filterset_class = QuestionFilter

    @staticmethod
    def create(request, *args, **kwargs):
        try:
            tape_box = TapeBox.objects.get(id=request.data['box'])
            question = TapeQuestion(box=tape_box,
                                    content=request.data['content'],
                                    author=request.user,
                                    token=random_string())
            question.save()
            add_notice(tape_box.user, "您的TapeBox有新的问题",
                       request.data['content'],
                       "/tapebox/" + request.data['box'])
            return Response(TapeQuestionSerializer(question).data, 201)
        except TapeBox.DoesNotExist:
            raise ValidationError('问题创建失败')


class TapeReplyViewSet(GenericViewSet):
    queryset = TapeReply.objects.all()
    permission_classes = [RobotCheck, NoEdit]

    @staticmethod
    def create(request, *args, **kwargs):
        try:
            question = TapeQuestion.objects.get(id=request.data['question'])
            if request.data['token'] != question.token and (
                    not request.user or
                (request.user != question.author
                 and request.user != question.box.user)):
                raise AuthenticationFailed('提问者身份验证失败')
            reply = TapeReply(question=question,
                              content=request.data['content'],
                              is_owner=request.user == question.box.user)
            reply.save()
            if reply.is_owner and question.author:
                add_notice(question.author, "您的Tape提问有新的回复",
                           request.data['content'],
                           "/tapebox/" + str(question.id))
            return Response(status=201)
        except TapeQuestion.DoesNotExist:
            raise ValidationError('回复失败')

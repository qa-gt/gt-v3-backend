from django.core.cache import cache
from rest_framework.response import Response as DRFResponse
from rest_framework.decorators import action
from gt.permissions import RequireWeChat
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.permissions import *
from rest_framework import mixins

from .models import *
from .serializers import *


class FormView(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, RequireWeChat]

    def create(self, request, *args, **kwargs):
        form = Form(creator=request.user, title=request.data["title"])
        form.save()
        for i in request.data["questions"]:
            question = Question(form=form, title=i["title"], type=i["type"])
            question.save()
            for j in i.get("choices") or []:
                choice = QuestionChoice(question=question,
                                        num=j["num"],
                                        title=j["title"])
                choice.save()
        return DRFResponse(
            {
                "status": "success",
                "data": FormSerializer(form).data
            },
            status=201)


class ResponseView(GenericViewSet):
    queryset = Response.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        form = Form.objects.get(id=request.data["form"])
        response = Response(form=form, user=request.user)
        response.save()
        for i in request.data["questions"]:
            question = Question.objects.get(id=i["id"])
            for j in i["answer"]:
                answer = Answer(question=question,
                                response=response,
                                choice_id=j)
                answer.save()
                if question.type == "radio":
                    break
        return DRFResponse({"status": "success"}, status=201)

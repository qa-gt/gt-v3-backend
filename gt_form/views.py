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
        return DRFResponse({"status": "success", "data": FormSerializer(form).data})

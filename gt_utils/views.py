import datetime
import hashlib
import random
import time

import musicapi
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseRedirect, JsonResponse
from gt.permissions import IsAdminOrReadOnly, RequireWeChat, RobotCheck
from rest_framework.permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, mixins

from gt_utils.serializers import *
from .serializers import LiveInfoSerializer
from .dogecloud import dogecloud_api


def md5sum(src):
    src = src.encode("utf-8")
    m = hashlib.md5()
    m.update(src)
    return m.hexdigest()


def visit_count(request):
    interval = request.GET.get("interval", "minute")
    now = request.GET.get("now", int(time.time()))
    now = datetime.datetime.fromtimestamp(now)
    if interval == "day":
        res = cache.get_many([
            "viscnt_" + (now - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(7)
        ])
    elif interval == "minute":
        res = cache.get_many([
            "viscnt_" +
            (now - datetime.timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M")
            for i in range(0, 60, 10)
        ])
    else:
        res = cache.get_many([
            "viscnt_" +
            (now - datetime.timedelta(hours=i)).strftime("%Y-%m-%d %H")
            for i in range(7)
        ])
    return JsonResponse(res)


class UploadImageView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        file = request.FILES["file"]
        if file.size > 1024 * 1024 * 5:
            return Response({"status": "error", "detail": "图片大小不能超过5M"})
        name = f"{time.time()}_{request.ip}.{file.name.split('.')[-1]}"
        if settings.GT_SERVER == "PRODUCTION":
            path = f"{settings.STATIC_ROOT}/article_images/{name}"
        else:
            path = f"{settings.STATICFILES_DIRS[0]}/article_images/{name}"
        with open(path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        return Response({
            "status": "success",
            "detail": "上传成功",
            "url": f"/static/article_images/{name}"
        })


class UploadKeyView(APIView):
    permission_classes = [IsAuthenticated, RequireWeChat]

    @staticmethod
    def post(request):
        scope = f"atc_images/{request.user.id}/*"
        r = dogecloud_api(
            "/auth/tmp_token.json", {
                "channel": "OSS_UPLOAD",
                "scopes": [f"gt-image:{scope}"],
                "ttl": 1800,
            })
        if r["code"] != 200:
            return Response({"status": "error", "detail": r["msg"]})
        r = r["data"]
        r["scope"] = scope
        return Response({"status": "success", "detail": "获取成功", "data": r})


class AboutView(mixins.ListModelMixin, GenericViewSet):
    queryset = About.objects.all().order_by("time")
    serializer_class = AboutSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None


def get_music_url(request):
    url = ""
    if request.GET["site"] == "QQ":
        if request.GET["by"] == "ID":
            url = musicapi.qq.get_by_id(request.GET["value"])
        elif request.GET["by"] == "NAME":
            url = musicapi.qq.get_by_name(request.GET["value"])
    elif request.GET["site"] == "WYY":
        if request.GET["by"] == "ID":
            url = musicapi.wyy.get_by_id(request.GET["value"])
        elif request.GET["by"] == "NAME":
            url = musicapi.wyy.get_by_name(request.GET["value"])
    return HttpResponseRedirect(url)


class LiveKeyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly, RobotCheck]

    @staticmethod
    def get(request):
        path = request.GET['path']
        timestamp = int(time.time())
        rand = str(random.random()).replace('.', '')
        sstring = f'{path}-{timestamp}-{rand}-0-{settings.ALI_LIVE_PULL_KEY}'
        hashvalue = md5sum(sstring)
        auth_key = f'{timestamp}-{rand}-0-{hashvalue}'
        return Response({'status': 'success', 'auth_key': auth_key})

    @staticmethod
    def post(request):
        path = request.data['path']
        timestamp = int(time.time())
        rand = str(random.random()).replace('.', '')
        sstring = f'{path}-{timestamp}-{rand}-0-{settings.ALI_LIVE_PUSH_KEY}'
        hashvalue = md5sum(sstring)
        auth_key = f'{timestamp}-{rand}-0-{hashvalue}'
        return Response({'status': 'success', 'auth_key': auth_key})


def get_live_info(request):
    return JsonResponse({
        'status':
        'success',
        'data':
        LiveInfoSerializer(
            LiveInfo.objects.filter(show=True).order_by('-id').first()).data
    })

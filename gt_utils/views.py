import time
import musicapi
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from .dogecloud import dogecloud_api


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
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        scope = f"atc_images/{request.ip}/{request.user.id}/*"
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

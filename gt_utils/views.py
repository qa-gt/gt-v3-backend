import time
import musicapi
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.conf import settings


class UploadView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

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


class MusicUrlView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        url = ""
        if request.POST["site"] == "qq":
            if request.POST["by"] == "id":
                url = musicapi.qq.get_by_id(request.POST["value"])
            elif request.POST["by"] == "name":
                url = musicapi.qq.get_by_name(request.POST["value"])
        elif request.POST["site"] == "wyy":
            if request.POST["by"] == "id":
                url = musicapi.wyy.get_by_id(request.POST["value"])
            elif request.POST["by"] == "name":
                url = musicapi.wyy.get_by_name(request.POST["value"])
        return Response({"status": "success", "detail": "获取成功", "url": url})

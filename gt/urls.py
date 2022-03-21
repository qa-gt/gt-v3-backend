# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
import gt_user.views

# 创建路由器并注册我们的视图。
router = DefaultRouter()
router.register(r'user', gt_user.views.UserViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^api-auth/',
            include('rest_framework.urls', namespace='rest_framework'))
]

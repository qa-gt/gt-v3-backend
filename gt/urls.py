import gt_user.views
import gt_article.views
import gt_utils.views
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

# 创建路由器并注册我们的视图。
router = DefaultRouter()
router.register(r'user', gt_user.views.UserViewSet)
router.register(r'article', gt_article.views.ArticleViewSet)
router.register(r'topic', gt_article.views.TopicViewSet)
router.register(r'like', gt_article.views.LikeViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path("user/login", gt_user.views.LoginView.as_view()),
    path("user/register", gt_user.views.RegisterView.as_view()),
    re_path(r'^api-auth/',
            include('rest_framework.urls', namespace='rest_framework')),
    path("utils/upload", gt_utils.views.UploadView.as_view()),
    path('admin/', admin.site.urls),
]

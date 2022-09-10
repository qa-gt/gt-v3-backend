import gt_user.views
import gt_article.views
import gt_utils.views
import gt_notice.views
import gt_school.views
import gt_tape.views
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

# 创建路由器并注册我们的视图。
router = DefaultRouter()
router.register(r'user', gt_user.views.UserViewSet)
router.register(r'article', gt_article.views.ArticleViewSet)
router.register(r'topic', gt_article.views.TopicViewSet)
router.register('like', gt_article.views.LikeViewSet)
router.register(r'comment', gt_article.views.CommentViewSet)
router.register(r'collect', gt_article.views.CollectView)
router.register(r'follow', gt_user.views.FollowView)
router.register(r'notice', gt_notice.views.NoticeView, basename='notice')
router.register('about', gt_utils.views.AboutView)
router.register('calendar_event', gt_school.views.CalendarEventViewSet)
router.register('tape_box', gt_tape.views.TapeBoxViewSet)
router.register('tape_question', gt_tape.views.TapeQuestionViewSet)
router.register('tape_reply', gt_tape.views.TapeReplyViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path("user/login", gt_user.views.LoginView.as_view()),
    path("user/change_password", gt_user.views.ChangePasswordView.as_view()),
    path("user/oauth_login", gt_user.views.OAuthLoginView.as_view()),
    path("user/oauth_callback", gt_user.views.OAuthCallbackView.as_view()),
    path("user/register", gt_user.views.RegisterView.as_view()),
    re_path(r'^api-auth/',
            include('rest_framework.urls', namespace='rest_framework')),
    path("utils/upload_image", gt_utils.views.UploadImageView.as_view()),
    path("utils/get_music_url", gt_utils.views.get_music_url),
    path("utils/upload_key", gt_utils.views.UploadKeyView.as_view()),
    path("utils/visit_count", gt_utils.views.visit_count),
    path("utils/live_key", gt_utils.views.LiveKeyView.as_view()),
    path("utils/live_info", gt_utils.views.get_live_info),
    path('admin/', admin.site.urls),
]

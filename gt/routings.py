from django.urls import re_path

from gt_im import consumers

websocket_urlpatterns = [
    re_path(r'^ws/im/$', consumers.ImConsumer.as_asgi()),
]

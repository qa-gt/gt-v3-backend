from tabnanny import verbose
from django.apps import AppConfig


class GtUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gt_user'
    verbose_name = '用户管理'

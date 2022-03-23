from tabnanny import verbose
from django.apps import AppConfig


class GtAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gt_admin'
    verbose_name = '管理'

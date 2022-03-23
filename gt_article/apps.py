from tabnanny import verbose
from django.apps import AppConfig


class GtArticleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gt_article'
    verbose_name = '文章'

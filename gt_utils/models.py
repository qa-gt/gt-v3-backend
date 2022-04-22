from django.db import models

# Create your models here.


class About(models.Model):
    time = models.DateTimeField(verbose_name="时间节点")
    title = models.CharField(max_length=100, verbose_name="节点标题")
    content = models.CharField(max_length=200, verbose_name="详细内容")
    types = models.CharField(max_length=100, verbose_name="节点状态")

    class Meta:
        db_table = 'about'
        verbose_name = verbose_name_plural = "关于瓜田"

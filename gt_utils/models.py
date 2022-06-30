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


class LiveInfo(models.Model):
    time = models.DateTimeField(verbose_name="时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    title = models.CharField(max_length=100, verbose_name="标题")
    description = models.CharField(max_length=500, verbose_name="描述")
    show = models.BooleanField(default=False, verbose_name="是否显示")
    watched = models.IntegerField(default=0, verbose_name="观看人数")

    class Meta:
        verbose_name = verbose_name_plural = "直播间信息"

from django.db import models

from gt_user.models import User


class TapeBox(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='tape_box',
                             verbose_name='用户')
    title = models.CharField(max_length=35, verbose_name='标题')
    image = models.URLField(max_length=500,
                            verbose_name='图片',
                            null=True,
                            blank=True)


class TapeQuestion(models.Model):
    box = models.ForeignKey(TapeBox,
                            on_delete=models.CASCADE,
                            related_name='question',
                            verbose_name='盒子')
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               verbose_name='提问者',
                               blank=True,
                               null=True)
    token = models.CharField(max_length=50, verbose_name='识别码')
    time = models.DateTimeField(auto_now_add=True, verbose_name='提问时间')
    content = models.CharField(max_length=500, verbose_name='内容')


class TapeReply(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               verbose_name='提问者',
                               blank=True,
                               null=True)
    content = models.CharField(max_length=500, verbose_name='内容')
    time = models.DateTimeField(auto_now_add=True, verbose_name='回复时间')

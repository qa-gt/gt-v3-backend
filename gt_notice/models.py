from django.db import models
from gt_user.models import User


class NoticeStateChoices(models.IntegerChoices):
    READ = 1, "已读"
    UNREAD = 0, "未读"
    DELETED = -1, "已删除"


class Notice(models.Model):
    recipient = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='notice',
                                  verbose_name='接收人')
    title = models.CharField(max_length=100, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    state = models.SmallIntegerField(default=NoticeStateChoices.UNREAD,
                                     choices=NoticeStateChoices.choices,
                                     verbose_name='状态')
    time = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    url = models.CharField(max_length=1000,
                           default='',
                           blank=True,
                           null=True,
                           verbose_name='地址')

    def __str__(self):
        return f"{self.recipient} 收到 {self.title}"

    class Meta:
        db_table = "notice"
        verbose_name = verbose_name_plural = "通知"

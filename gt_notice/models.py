from django.db import models

from gt_user.models import User


class Notices(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    recipient = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='notice')
    title = models.CharField(max_length=100)
    content = models.TextField()
    state = models.SmallIntegerField(default=0,
                                     choices=(
                                         (1, "已读"),
                                         (0, "未读"),
                                         (-1, "已删除"),
                                     ))
    time = models.BigIntegerField()
    url = models.CharField(max_length=1000, default="", blank=True, null=True)

    def __str__(self):
        return f"{self.recipient} 收到 {self.title}"

    class Meta:
        db_table = "notices"

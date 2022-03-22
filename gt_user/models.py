from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    portrait = models.TextField(default="")
    pwd = models.CharField(max_length=30)
    grade = models.CharField(max_length=10,
                             null=True,
                             blank=True,
                             default="保密")
    gender = models.SmallIntegerField(default=0,
                                      choices=[(0, "保密"), (1, "男"), (2, "女")])
    introduction = models.TextField(max_length=100,
                                    null=True,
                                    blank=True,
                                    default="")
    state = models.SmallIntegerField(default=0,
                                     null=True,
                                     blank=True,
                                     choices=(
                                         (2, "超级管理员"),
                                         (1, "管理员"),
                                         (0, "普通用户"),
                                         (-1, "禁止发贴"),
                                         (-2, "禁止发言"),
                                         (-3, "封禁帐号"),
                                     ))
    tags = models.TextField(max_length=20, null=True, blank=True, default="")

    def __str__(self):
        return f"{self.id}:{self.username}"

    class Meta:
        db_table = "user"


class Follow(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    follower = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='follower')
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='following')
    state = models.SmallIntegerField(
        default=1,
        choices=(
            (1, "正常"),
            (2, "已取关"),
        ),
    )

    def __str__(self):
        return f"{self.follower} 关注 {self.following}"

    class Meta:
        db_table = "follow"

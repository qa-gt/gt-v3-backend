from django.db import models
from django.contrib.auth.models import AbstractUser, Group as BaseGroup


class GenderChoices(models.IntegerChoices):
    SECRET = 0, "保密"
    MALE = 1, "男"
    FEMALE = 2, "女"


class BanStateChoices(models.IntegerChoices):
    NO_POST = -1, "禁止发贴"
    NO_COMMENT = -2, "禁止发言"


class User(AbstractUser):
    portrait = models.CharField(max_length=50,
                                default="",
                                null=True,
                                blank=True,
                                verbose_name="头像")
    grade = models.CharField(max_length=10,
                             default="保密",
                             verbose_name="年级")
    gender = models.SmallIntegerField(default=GenderChoices.SECRET,
                                      choices=GenderChoices.choices,
                                      verbose_name="性别")
    introduction = models.TextField(
        max_length=100,
        null=True,
        blank=True,
        default="",
        verbose_name="介绍"
    )
    ban_state = models.SmallIntegerField(default=None,
                                         null=True,
                                         blank=True,
                                         choices=BanStateChoices.choices,
                                         verbose_name="封禁状态")
    tags = models.CharField(max_length=20,
                            null=True,
                            blank=True,
                            default="",
                            verbose_name="认证信息")

    def __str__(self):
        return f"[{self.id}] {self.username}"

    class Meta:
        db_table = "user"
        verbose_name = verbose_name_plural = "用户"


class Group(BaseGroup):
    class Meta:
        verbose_name = '组'
        verbose_name_plural = '组'
        proxy = True


class Follow(models.Model):
    follower = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='follower',
                                 verbose_name='当前用户')
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='following',
                                  verbose_name='关注用户')
    follow_time = models.DateTimeField(auto_now_add=True, verbose_name='关注时间')

    def __str__(self):
        return f"{self.follower} 关注 {self.following}"

    class Meta:
        db_table = "follow"
        verbose_name = verbose_name_plural = "关注"

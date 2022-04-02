from django.db import models
from django.contrib.auth.models import AbstractUser, Group as BaseGroup


class GenderChoices(models.IntegerChoices):
    SECRET = 0, "保密"
    MALE = 1, "男"
    FEMALE = 2, "女"


class BanStateChoices(models.IntegerChoices):
    NORMAL = 0, '正常'
    NO_POST = -1, "禁止发贴"
    NO_COMMENT = -2, "禁止发言"


class YxRoleChoices(models.IntegerChoices):
    UNKNOWN = 0, '未知'
    STUDENT = 1, '学生'
    TEACHER = 2, '老师'


class User(AbstractUser):
    portrait = models.CharField(max_length=200,
                                default="",
                                null=True,
                                blank=True,
                                verbose_name="头像")
    grade = models.CharField(max_length=8, default="保密", verbose_name="年级")
    gender = models.SmallIntegerField(default=GenderChoices.SECRET,
                                      choices=GenderChoices.choices,
                                      verbose_name="性别")
    introduction = models.TextField(max_length=100,
                                    null=True,
                                    blank=True,
                                    default="",
                                    verbose_name="介绍")
    ban_state = models.SmallIntegerField(default=BanStateChoices.NORMAL,
                                         choices=BanStateChoices.choices,
                                         verbose_name="封禁状态")
    tags = models.CharField(max_length=20,
                            null=True,
                            blank=True,
                            default="",
                            verbose_name="认证信息")

    def __str__(self):
        return f"[{self.id}] {self.username}"

    @property
    def yunxiao_state(self):
        try:
            self.yunxiao
            return True
        except Yunxiao.DoesNotExist:
            return False

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
                                 related_name='following',
                                 verbose_name='关注用户')
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='follower',
                                  verbose_name='被关注用户')
    follow_time = models.DateTimeField(auto_now_add=True, verbose_name='关注时间')

    def __str__(self):
        return f"{self.follower} 关注 {self.following}"

    class Meta:
        db_table = "follow"
        verbose_name = verbose_name_plural = "关注"


class Yunxiao(models.Model):
    user = models.OneToOneField(User,
                             on_delete=models.CASCADE,
                             related_name='yunxiao',
                             verbose_name='用户')
    student_id = models.CharField(
        max_length=20,
        unique=True,
    )
    uid = models.CharField(
        max_length=50,
        unique=True,
    )
    real_name = models.CharField(max_length=10, verbose_name='真实姓名')
    show = models.BooleanField(default=False, verbose_name='显示认证信息')
    gender = models.SmallIntegerField(
        default=GenderChoices.SECRET,
        choices=GenderChoices.choices,
        verbose_name="性别",
    )
    mobile = models.CharField(
        max_length=11,
        verbose_name='手机号',
        null=True,
        blank=True,
    )
    role = models.SmallIntegerField(default=YxRoleChoices.UNKNOWN,
                                    choices=YxRoleChoices.choices,
                                    verbose_name="角色")
    time = models.DateTimeField(auto_now_add=True, verbose_name='认证时间')

    def __str__(self):
        return f"{self.user}云校认证"

    class Meta:
        db_table = "yunxiao"
        verbose_name = verbose_name_plural = "云校认证"

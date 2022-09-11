from django.db import models
from gt_user.models import User


class ContentTypeChoice(models.IntegerChoices):
    TEXT = 0, '文本'
    IMAGE = 1, '图片'
    VIDEO = 2, '视频'
    FILE = 3, '文件'


class IsAdminChoice(models.IntegerChoices):
    NONE = 0, '无'
    ADMIN = 1, '管理员'
    OWNER = 2, '群主'


class Room(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='名称',
        default=None,
        null=True,
        blank=True,
    )
    avatar = models.CharField(
        max_length=511,
        verbose_name='头像',
        default=None,
        null=True,
        blank=True,
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
    )
    is_group = models.BooleanField(default=False, verbose_name='是否为群聊')
    announcement = models.TextField(
        default='',
        verbose_name='公告',
        max_length=5000,
        null=True,
    )
    last_message = models.ForeignKey(
        'Message',
        on_delete=models.SET_NULL,
        related_name='last_message',
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "聊天室"


class RoomMember(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='im_rooms',
        verbose_name='用户',
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name='聊天室',
    )
    single_chat_with = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='single_chats',
        verbose_name='单聊对象',
        null=True,
        blank=True,
    )
    is_admin = models.SmallIntegerField(
        choices=IsAdminChoice.choices,
        default=IsAdminChoice.NONE,
        verbose_name='是否为管理员',
    )
    notificate = models.BooleanField(default=True, verbose_name='是否接收通知')
    joined_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='加入时间',
    )
    last_read_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='最后阅读时间',
    )


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_im_messages',
        verbose_name='发送人',
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='im_messages',
        verbose_name='聊天室',
    )
    content = models.TextField(verbose_name='内容')
    content_type = models.SmallIntegerField(
        choices=ContentTypeChoice.choices,
        default=ContentTypeChoice.TEXT,
        verbose_name='内容类型',
    )
    time = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    recalled_time = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        verbose_name='撤回时间',
    )

    def __str__(self):
        return f"{self.sender} 发送 {self.content} 到 {self.room}"

    class Meta:
        verbose_name = verbose_name_plural = "聊天消息"

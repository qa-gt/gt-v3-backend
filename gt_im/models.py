from django.db import models
from gt_user.models import User


class ContentTypeChoice(models.IntegerChoices):
    TEXT = 0, '文本'
    IMAGE = 1, '图片'
    VIDEO = 2, '视频'
    FILE = 3, '文件'
    AUDIO = 4, '音频'


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
        verbose_name = verbose_name_plural = '聊天室'


class InviteCode(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name='邀请码')
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name='聊天室',
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='创建者',
    )
    expire_time = models.DateTimeField(
        verbose_name='过期时间',
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = verbose_name_plural = '邀请码'


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
        default=None,
        null=True,
        blank=True,
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='im_messages',
        verbose_name='聊天室',
    )
    content = models.TextField(verbose_name='内容', default='')
    content_type = models.SmallIntegerField(
        choices=ContentTypeChoice.choices,
        default=ContentTypeChoice.TEXT,
        verbose_name='内容类型',
    )
    file = models.ForeignKey(
        'File',
        on_delete=models.SET_NULL,
        related_name='im_messages',
        verbose_name='文件',
        default=None,
        null=True,
        blank=True,
    )
    time = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    recalled_time = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        verbose_name='撤回时间',
    )

    def __str__(self):
        return f'{self.sender} 发送 {self.content} 到 {self.room}'

    class Meta:
        verbose_name = verbose_name_plural = '聊天消息'


class FilePolicy(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称')
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
    )
    client_id = models.CharField(
        max_length=8191,
        verbose_name='客户端ID',
    )
    client_secret = models.CharField(
        max_length=8191,
        verbose_name='客户端密钥',
    )
    redirect_uri = models.CharField(
        max_length=8191,
        verbose_name='重定向URI',
    )
    access_token = models.CharField(
        max_length=8191,
        verbose_name='access_token',
    )
    refresh_token = models.CharField(
        max_length=8191,
        verbose_name='refresh_token',
    )
    root = models.CharField(
        max_length=8191,
        verbose_name='根目录',
    )
    expires_in = models.IntegerField(verbose_name='过期时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '文件策略'


class File(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='im_files',
        verbose_name='用户',
    )
    name = models.CharField(max_length=2047, verbose_name='文件名')
    source_name = models.CharField(max_length=2047, verbose_name='原文件存储路径')
    size = models.BigIntegerField(verbose_name='文件大小')
    upload_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='上传时间',
    )
    policy = models.ForeignKey(
        FilePolicy,
        on_delete=models.CASCADE,
        verbose_name='文件策略',
    )
    uploaded = models.BooleanField(default=False, verbose_name='是否已上传')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '文件'

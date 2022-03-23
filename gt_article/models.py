from django.db import models

from gt_user.models import User


class TopicCommentStateChoices(models.IntegerChoices):
    TOP = 1, '置顶'
    NORMAL = 0, '正常'
    HIDE = -1, '隐藏'
    DELETE = -2, '删除'


class ArticleStateChoices(models.IntegerChoices):
    TOP_INDEX = 3, '全站置顶'
    TOP_TOPIC = 2, '话题页置顶'
    TOP_USER = 1, '个人页置顶'
    NORMAL = 0, '正常'
    HIDE_INDEX = -1, '首页隐藏'
    HIDE_TOPIC = -2, '话题页隐藏'
    HIDE_USER = -3, '个人页隐藏'
    HIDE = -4, '禁止查看'
    DELETE = -5, '删除'


class Topic(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='话题名称')
    description = models.TextField(max_length=100,
                                   null=True,
                                   blank=True,
                                   default='',
                                   verbose_name='描述')
    state = models.SmallIntegerField(null=True,
                                     blank=True,
                                     default=TopicCommentStateChoices.NORMAL,
                                     choices=TopicCommentStateChoices.choices,
                                     verbose_name='状态')

    def __str__(self):
        return f'{self.id}:{self.name}'

    class Meta:
        db_table = 'topic'
        verbose_name = verbose_name_plural = '话题'


class Article(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='article',
        verbose_name='作者',
    )
    title = models.CharField(max_length=100, verbose_name='标题')
    content = models.TextField(verbose_name='正文')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    state = models.SmallIntegerField(
        null=True,
        blank=True,
        default=ArticleStateChoices.NORMAL,
        choices=ArticleStateChoices.choices,
        verbose_name='状态',
    )
    topic = models.ForeignKey(
        Topic,
        default=0,
        on_delete=models.SET_DEFAULT,
        related_name='article',
        verbose_name='话题',
    )
    read_count = models.IntegerField(default=0, verbose_name='阅读数')

    def __str__(self):
        return f'{self.id}:{self.title}'

    class Meta:
        db_table = 'article'
        verbose_name = verbose_name_plural = '文章'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='作者',
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='关联文章',
    )
    reply = models.ForeignKey(
        'self',
        on_delete=models.SET_DEFAULT,
        related_name='replys',
        default=None,
        blank=True,
        null=True,
        verbose_name='回复',
    )
    content = models.CharField(max_length=300, verbose_name='正文')
    time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    state = models.SmallIntegerField(
        null=True,
        blank=True,
        default=TopicCommentStateChoices.NORMAL,
        choices=TopicCommentStateChoices.choices,
        verbose_name='状态',
    )

    def __str__(self):
        return f'{self.id}-{self.author} 于 {self.under}'

    class Meta:
        db_table = 'comment'
        verbose_name = verbose_name_plural = '评论'


class Like(models.Model):
    type = models.SmallIntegerField(
        default=1,
        choices=(
            (1, '文章'),
            (2, '评论'),
        ),
        verbose_name='类型',
    )
    article = models.ForeignKey(Article,
                                null=True,
                                blank=True,
                                on_delete=models.CASCADE,
                                related_name='like',
                                verbose_name='获赞文章')
    comment = models.ForeignKey(
        Comment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='like',
        verbose_name='获赞评论',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='like',
        verbose_name='用户',
    )

    def __str__(self):
        return f'{self.user} 赞 {self.article}'

    class Meta:
        db_table = 'like'
        verbose_name = verbose_name_plural = '点赞'


class Collect(models.Model):
    article = models.ForeignKey(
        Article,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='collect',
        verbose_name='被收藏文章',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collect',
        verbose_name='用户',
    )

    def __str__(self):
        return f'{self.user} 收藏 {self.article}'

    class Meta:
        db_table = 'collect'
        verbose_name = verbose_name_plural = '收藏'

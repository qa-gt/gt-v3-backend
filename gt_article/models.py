from django.db import models

from gt_user.models import User


class Topic(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=100,
                                   null=True,
                                   blank=True,
                                   default="")
    state = models.SmallIntegerField(null=True,
                                     blank=True,
                                     default=0,
                                     choices=(
                                         (1, "置顶"),
                                         (0, "正常"),
                                         (-1, "隐藏"),
                                         (-2, "删除"),
                                     ))

    def __str__(self):
        return f"{self.id}:{self.name}"

    class Meta:
        db_table = "topic"


class Article(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    author = models.ForeignKey(User,
                               on_delete=models.DO_NOTHING,
                               related_name='article')
    title = models.CharField(max_length=100)
    content = models.TextField()
    create_time = models.BigIntegerField()
    update_time = models.BigIntegerField()
    state = models.SmallIntegerField(null=True,
                                     blank=True,
                                     default=0,
                                     choices=(
                                         (3, "全站置顶"),
                                         (2, "话题页置顶"),
                                         (1, "个人页置顶"),
                                         (0, "正常"),
                                         (-1, "禁止首页列出"),
                                         (-2, "禁止首页和话题列出"),
                                         (-3, "禁止首页、话题和个人页列出"),
                                         (-4, "禁止查看"),
                                         (-5, "删除"),
                                     ))
    topic = models.ForeignKey(Topic,
                              default=0,
                              on_delete=models.SET_DEFAULT,
                              related_name='article')
    read_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}:{self.title}"

    class Meta:
        db_table = "article"


class Comment(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    author = models.ForeignKey(User,
                               on_delete=models.DO_NOTHING,
                               related_name='comment')
    article = models.ForeignKey(Article,
                                on_delete=models.DO_NOTHING,
                                related_name='comment')
    reply = models.ForeignKey("self",
                              on_delete=models.DO_NOTHING,
                              related_name='reply',
                              default=None,
                              blank=True,
                              null=True)
    content = models.CharField(max_length=300)
    time = models.BigIntegerField()
    state = models.SmallIntegerField(null=True,
                                     blank=True,
                                     default=0,
                                     choices=(
                                         (1, "置顶"),
                                         (0, "正常"),
                                         (-1, "隐藏"),
                                         (-2, "删除"),
                                     ))

    def __str__(self):
        return f"{self.id}-{self.author} 于 {self.under}"

    class Meta:
        db_table = "comment"


class Like(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    type = models.SmallIntegerField(default=1,
                                    choices=(
                                        (1, "文章"),
                                        (2, "评论"),
                                    ))
    article = models.ForeignKey(Article,
                                null=True,
                                blank=True,
                                on_delete=models.DO_NOTHING,
                                related_name='like')
    comment = models.ForeignKey(Comment,
                                null=True,
                                blank=True,
                                on_delete=models.DO_NOTHING,
                                related_name='like')
    user = models.ForeignKey(User,
                             on_delete=models.DO_NOTHING,
                             related_name='like')

    def __str__(self):
        return f"{self.user} 赞 {self.article}"

    class Meta:
        db_table = "like"


class Collect(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    article = models.ForeignKey(Article,
                                null=True,
                                blank=True,
                                on_delete=models.DO_NOTHING,
                                related_name='collect')
    user = models.ForeignKey(User,
                             on_delete=models.DO_NOTHING,
                             related_name='collect')

    def __str__(self):
        return f"{self.user} 收藏 {self.article}"

    class Meta:
        db_table = "collect"

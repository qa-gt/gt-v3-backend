from django.db import models

from gt_user.models import User
from gt_article.models import Article, Comment


class Report(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    reporter = models.ForeignKey(User,
                                 on_delete=models.DO_NOTHING,
                                 related_name='report')
    type = models.SmallIntegerField(default=1,
                                    choices=(
                                        (1, "文章"),
                                        (2, "评论"),
                                    ))
    article = models.ForeignKey(Article,
                                on_delete=models.DO_NOTHING,
                                blank=True,
                                null=True,
                                related_name='report')
    comment = models.ForeignKey(Comment,
                                on_delete=models.DO_NOTHING,
                                blank=True,
                                null=True,
                                related_name='report')
    state = models.SmallIntegerField(default=0,
                                     choices=(
                                         (1, "无违规"),
                                         (0, "未处理"),
                                         (-1, "已处理"),
                                     ))
    report_time = models.BigIntegerField()
    operated_time = models.BigIntegerField(null=True, blank=True)
    operator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="operated_reports",
    )

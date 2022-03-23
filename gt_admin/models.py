from django.db import models

from gt_user.models import User
from gt_article.models import Article, Comment


class ReportStateChoices(models.IntegerChoices):
    PASSED = 1, '无违规'
    WAITING = 0, '等待审核'
    OPERATED = -1, '已处理'


class Report(models.Model):
    reporter = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='report',
                                 verbose_name='举报人')
    type = models.SmallIntegerField(default=1,
                                    choices=(
                                        (1, "文章"),
                                        (2, "评论"),
                                    ),
                                    verbose_name='举报类型')
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                related_name='report',
                                verbose_name='被举报文章')
    comment = models.ForeignKey(Comment,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                related_name='report',
                                verbose_name='被举报评论')
    state = models.SmallIntegerField(
        default=ReportStateChoices.WAITING,
        choices=ReportStateChoices.choices,
        verbose_name='处理状态',
    )
    report_time = models.DateTimeField(auto_now_add=True, verbose_name='举报时间')
    operated_time = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        verbose_name='处理时间',
    )
    operator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="operated_report",
        verbose_name='处理人',
    )

    class Meta:
        db_table = 'report'
        verbose_name = verbose_name_plural = '举报'

from turtle import title

from django.db import models
from gt_user.models import User

NUM_TO_LETTER = list(' ABCDEFGHIJKLMNOPQRSTUVWXYZ')


class PermissionChoices(models.IntegerChoices):
    EVERYONE = 0, '所有人'
    LOGIN = 1, '登录用户'
    WECHAT = 2, '微信认证用户'


class QuestionTypeChoices(models.IntegerChoices):
    RADIO = 1, '单选题'
    SELECT = 2, '多选题'
    BLANK = 3, '填空题'


class Form(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    description = models.TextField(null=True, blank=True, verbose_name='描述')
    creator = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='form',
                                verbose_name='创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    start_time = models.DateTimeField(verbose_name='开始时间',
                                      null=True,
                                      blank=True)
    end_time = models.DateTimeField(verbose_name='截止时间', null=True, blank=True)
    permission = models.SmallIntegerField(choices=PermissionChoices.choices,
                                          default=PermissionChoices.LOGIN,
                                          verbose_name='提交权限')
    anonymous = models.BooleanField(default=True, verbose_name='匿名提交')

    def __str__(self):
        return f"[{self.id}]{self.title}"

    class Meta:
        db_table = "form"
        verbose_name = verbose_name_plural = "表单"


class Question(models.Model):
    title = models.CharField(max_length=200, verbose_name='题目标题')
    type = models.SmallIntegerField(choices=QuestionTypeChoices.choices,
                                    verbose_name='题目类型')
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name='question',
        verbose_name='所属表单',
    )
    required = models.BooleanField(default=True, verbose_name='必填')

    def __str__(self):
        return f"[{self.id}]{self.title}"

    class Meta:
        db_table = "question"
        verbose_name = verbose_name_plural = "题目"


class QuestionChoice(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='choice',
                                 verbose_name='所属题目')
    num = models.SmallIntegerField(verbose_name='选项序号')
    title = models.CharField(max_length=200, verbose_name='选项标题')

    def __str__(self):
        return f"[{NUM_TO_LETTER[self.num]}]{self.title}"

    class Meta:
        db_table = "question_choice"
        verbose_name = verbose_name_plural = "选项"


class Response(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='填写时间')
    form = models.ForeignKey(Form,
                             on_delete=models.CASCADE,
                             related_name='response',
                             verbose_name='所属表单')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='填写用户')

    def __str__(self):
        return f"[{self.id}]{self.user.username} 于 {self.form.title}"

    class Meta:
        db_table = "response"
        verbose_name = verbose_name_plural = "表单收集"


class Answer(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='answer',
                                 verbose_name='所属题目')
    response = models.ForeignKey(Response,
                                 on_delete=models.CASCADE,
                                 related_name='answer',
                                 verbose_name='所属填写')
    choice = models.ForeignKey(QuestionChoice,
                               on_delete=models.CASCADE,
                               verbose_name='选项答案',
                               blank=True,
                               null=True)
    text = models.TextField(verbose_name='填空答案', blank=True, null=True)

    def __str__(self):
        return f"题目 [{self.question}] 的答案"

    class Meta:
        db_table = "answer"
        verbose_name = verbose_name_plural = "答案"

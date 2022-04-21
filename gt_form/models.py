from turtle import title
from django.db import models

from gt_user.models import User

# Create your models here.


class QuestionTypeChoices(models.IntegerChoices):
    RADIO = 1, '单选题'
    SELECT = 2, '多选题'
    BLANK = 3, '填空题'


class Form(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    creator = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                verbose_name='创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    end_time = models.DateTimeField(verbose_name='截止时间')

    def __str__(self):
        return f"[{self.id}]{self.title}"

    class Meta:
        db_table = "form"
        verbose_name = verbose_name_plural = "表单"


class Question(models.Model):
    title = models.CharField(max_length=200, verbose_name='题目标题')
    type = models.IntegerField(choices=QuestionTypeChoices.choices,
                               verbose_name='题目类型')
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        verbose_name='所属表单',
    )

    def __str__(self):
        return f"[{self.id}]{self.title}"

    class Meta:
        db_table = "question"
        verbose_name = verbose_name_plural = "题目"


class Response(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='填写时间')
    form = models.ForeignKey(Form,
                             on_delete=models.CASCADE,
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
                                 verbose_name='所属题目')
    response = models.ForeignKey(Response,
                                 on_delete=models.CASCADE,
                                 verbose_name='所属填写')
    content = models.TextField(verbose_name='答案')

    def __str__(self):
        return f"[{self.id}]{self.content}"

    class Meta:
        db_table = "answer"
        verbose_name = verbose_name_plural = "答案"

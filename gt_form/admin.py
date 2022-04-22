from django.contrib import admin

from .models import *


class AnswerInline(admin.StackedInline):
    extra = 0
    model = Answer
    can_delete = False
    fields = ('question', 'choice')
    readonly_fields = ('question', )


class ChoiceInline(admin.StackedInline):
    extra = 0
    model = QuestionChoice
    fields = ('num', 'title')
    readonly_fields = ('num', )


class QuestionInline(admin.StackedInline):
    extra = 0
    model = Question
    fields = ('id', 'title', 'type')
    inlines = [ChoiceInline]


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'creator', 'end_time')
    inlines = [QuestionInline]


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'form', 'user')
    inlines = [AnswerInline]

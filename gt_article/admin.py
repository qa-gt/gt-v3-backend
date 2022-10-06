from django.contrib import admin

from .models import Article, Collect, Comment, Like, Topic


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'topic', 'read_count', 'state',
                    'create_time', 'update_time')


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'user')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'author', 'time', 'state')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'article', 'comment', 'user')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'state', 'priority')

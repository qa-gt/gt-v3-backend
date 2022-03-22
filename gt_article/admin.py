from django.contrib import admin

from .models import Article, Collect, Comment, Like, Topic

admin.site.register(Article)
admin.site.register(Collect)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Topic)

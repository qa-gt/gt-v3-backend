from django.contrib import admin

from .models import Report

admin.site.site_header = 'QA瓜田'
admin.site.site_title = 'QA瓜田管理'
admin.site.index_title = '欢迎使用QA瓜田后台管理'


admin.site.register(Report)

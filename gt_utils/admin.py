from django.contrib import admin

from .models import About, LiveInfo


# Register your models here.
@admin.register(LiveInfo)
class LiveInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'time', 'show')

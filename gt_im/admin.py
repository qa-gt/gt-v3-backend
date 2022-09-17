from django.contrib import admin

from .models import FilePolicy


@admin.register(FilePolicy)
class LiveInfoAdmin(admin.ModelAdmin):
    list_display = ('name', )

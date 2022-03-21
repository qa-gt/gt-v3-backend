from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *

ADDITIONAL_FIELDS = (('附加数据', {
    'fields': ('grade', 'introduction', 'tags', 'portrait', 'gender')
}), )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # list_display = ('__str__', 'pwd', 'grade', 'tags',
    #                 'introduction', 'state')
    fieldsets = BaseUserAdmin.fieldsets + ADDITIONAL_FIELDS
    add_fieldsets = BaseUserAdmin.fieldsets + ADDITIONAL_FIELDS

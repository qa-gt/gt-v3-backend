from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin

from .models import User, Group, BaseGroup, Follow, Yunxiao

admin.site.unregister(BaseGroup)


class YunxiaoInline(admin.TabularInline):
    model = Yunxiao
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'grade', 'gender', 'tags',
                    'is_active', 'is_staff', 'ban_state')
    fieldsets = (
        ('账号信息', {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('portrait', 'grade',
         'gender', 'introduction', 'tags')}),
        ('权限', {'fields': ('is_active', 'ban_state', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('时间信息', {'fields': ('last_login', 'date_joined')}),
    )
    inlines = [YunxiaoInline]


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following', 'follow_time')

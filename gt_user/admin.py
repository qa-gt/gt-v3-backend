from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin

from .models import User, Group, BaseGroup, Follow, Yunxiao, WeChat

admin.site.unregister(BaseGroup)


class UserInline(admin.TabularInline):
    model = User
    fields = ['username']
    readonly_fields = ['username']
    extra = 0


class YunxiaoInline(admin.TabularInline):
    model = Yunxiao
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'tags', 'is_active', 'is_staff',
                    'ban_state')
    actions = ['ban_user', 'ban_user_and_wechat']
    fieldsets = (
        ('账号信息', {
            'fields': ('username', 'password')
        }),
        ('个人信息', {
            'fields':
            ('portrait', 'grade', 'gender', 'introduction', 'tags', 'wechat')
        }),
        ('权限', {
            'fields': ('is_active', 'ban_state', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')
        }),
        ('时间信息', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    inlines = [YunxiaoInline]

    def ban_user(self, request, queryset):
        queryset.update(is_active=False)

    ban_user.short_description = '封禁用户'

    def ban_user_and_wechat(self, request, queryset):
        queryset.update(is_active=False)
        dealed = []
        for i in queryset:
            if i.wechat and i.wechat.id not in dealed:
                i.wechat.is_active = False
                i.wechat.save()
                dealed.append(i.wechat.id)

    ban_user_and_wechat.short_description = '封禁用户和微信'


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following', 'follow_time')


@admin.register(WeChat)
class WeChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'unique_id', 'time')
    inlines = [UserInline]
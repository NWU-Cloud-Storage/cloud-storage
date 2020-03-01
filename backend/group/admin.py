from django.contrib import admin
from .models import Group, MembershipTmp, Intention


# Register your models here.

@admin.register(Group)
class Group(admin.ModelAdmin):
    list_display = ('pk', 'name', 'num_of_members')
    fields = ('name',)

@admin.register(MembershipTmp)
class Membership(admin.ModelAdmin):
    list_display = ('group_name', 'user_name', 'permission')
    fields = ('group', 'user', 'permission')

    def group_name(self, obj):
        return obj.group
    group_name.short_description = '群组'

    def user_name(self, obj):
        return obj.user
    user_name.short_description = '用户'

@admin.register(Intention)
class Intention(admin.ModelAdmin):
    list_display = ('group_name', 'user_name', 'date_intended')
    fields = ('group', 'user')

    def group_name(self, obj):
        return obj.group
    group_name.short_description = '群组'

    def user_name(self, obj):
        return obj.user
    user_name.short_description = '用户'

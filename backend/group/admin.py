from django.contrib import admin
from .models import Group, Membership


# Register your models here.

@admin.register(Group)
class Group(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name',)

@admin.register(Membership)
class Membership(admin.ModelAdmin):
    list_display = ('id','group_name','user_name','permission')
    fields = ('group','user','permission')

    def group_name(self, obj):
        return obj.group
    group_name.short_description = '群组'

    def user_name(self, obj):
        return obj.user
    user_name.short_description = '用户'
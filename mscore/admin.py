from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from mscore.models import *


class TaskInline(admin.StackedInline):
    model = Task
    readonly_fields = ('publish_date',)
    extra = 0


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'publish_date')
    readonly_fields = ('publish_date',)
    list_filter = ('publish_date',)
    inlines = [TaskInline]


class PersonInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (PersonInLine,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

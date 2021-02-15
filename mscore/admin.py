from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from mscore.models import *

admin.site.register(Space)
admin.site.register(Task)


class PersonInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (PersonInLine,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

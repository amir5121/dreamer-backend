from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User

UserAdmin.list_display += ("avatar",)  # don't forget the commas
# UserAdmin.list_filter += ('can_charge', )
UserAdmin.fieldsets += (("Extra Fields", {"fields": ("avatar", "last_app_open")}),)

admin.site.register(User, UserAdmin)

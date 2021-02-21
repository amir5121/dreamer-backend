from django.contrib import admin

from notification.models import Notification, UserNotification
from utils.admin import DreamerAdmin


@admin.register(Notification)
class NotificationAdmin(DreamerAdmin):
    list_display = ("text",)


@admin.register(UserNotification)
class UserNotificationAdmin(DreamerAdmin):
    list_display = ("user", "notification", "state", "created")
    list_filter = ("state",)
    raw_id_fields = ["user", "notification"]

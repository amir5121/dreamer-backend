from django.contrib import admin

from configuration.models import DreamerConfiguration
from utils.admin import DreamerAdmin


@admin.register(DreamerConfiguration)
class PostAdmin(DreamerAdmin):
    list_display = ("version", "main_background", "created")
    ordering = ("-created",)
    list_filter = ("version",)

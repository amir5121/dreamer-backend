from django.contrib import admin

from post.models import Post
from utils.admin import DreamerAdmin


@admin.register(Post)
class PostAdmin(DreamerAdmin):
    list_display = ("user", "status", "text", 'is_removed')
    list_editable = ('is_removed',)
    raw_id_fields = ("user",)
    ordering = ("-created",)
    list_filter = ("status", "is_removed")

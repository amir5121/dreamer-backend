from django.contrib import admin

from post.models import Post, Dream, Feeling, Element, FeelingDetail
from utils.admin import DreamerAdmin


@admin.register(Post)
class PostAdmin(DreamerAdmin):
    list_display = ("text", "is_removed", "created")
    list_editable = ("is_removed",)
    ordering = ("-created",)
    list_filter = ("is_removed",)


@admin.register(Dream)
class DreamAdmin(DreamerAdmin):
    list_display = (
        "user",
        "text",
        "is_removed",
        "created",
        "publication_status",
        "dream_clearance",
        "title",
        "dream_date",
    )
    list_editable = ("is_removed",)
    search_fields = ("user__username",)
    ordering = ("-created",)
    list_filter = ("is_removed",)
    raw_id_fields = ("user",)


@admin.register(Feeling)
class FeelingAdmin(DreamerAdmin):
    list_display = ("dream", "rate", "feeling")
    raw_id_fields = ("dream",)


@admin.register(FeelingDetail)
class FeelingDetailAdmin(DreamerAdmin):
    list_display = ("detailed_type", "parent_type", "description", "is_removed")
    list_editable = ("is_removed",)
    list_filter = ("is_removed",)


@admin.register(Element)
class ElementAdmin(DreamerAdmin):
    list_display = ("dream", "elements", "type")
    raw_id_fields = ("dream",)

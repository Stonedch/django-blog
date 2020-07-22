from . import models

from django.contrib import admin


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author", "publish", "status")
    list_filter = ("status", "created", "publish", "author")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title", )}
    raw_id_fields = ("author", )
    date_hierarchy = "publish"
    ordering = ("status", "publish")

from django.contrib import admin

from .models import Comment, Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "creator", "assignee", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("order", "author", "created_at")

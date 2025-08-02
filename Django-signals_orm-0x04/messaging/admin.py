from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin interface for the Message model.
    """

    list_display = ("sender", "receiver", "content", "timestamp", "is_read")
    search_fields = ("sender__username", "receiver__username")
    list_filter = ("is_read", "timestamp")
    ordering = ("-timestamp",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "created_at", "is_read")

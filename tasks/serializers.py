from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Comment
from .models import Task


User = get_user_model()

# A minimal user serializer to display nested info nicely
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")


class CommentSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "task", "author", "content", "created_at")
        read_only_fields = ("author", "created_at")


class TaskSerializer(serializers.ModelSerializer):
    # Nested serializers for reading (display names, not just IDs)
    creator = UserInfoSerializer(read_only=True)
    assignee_info = UserInfoSerializer(source="assignee", read_only=True)

    # Write-only field for inputting assignee ID
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True, write_only=True
    )

    # Show comments count
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "creator",
            "assignee",
            "assignee_info",
            "created_at",
            "updated_at",
            "comments_count",
        )
        read_only_fields = ("creator", "created_at", "updated_at")

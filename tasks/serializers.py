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


class TaskBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer with common fields for both List and Detail views.
    """

    creator = UserInfoSerializer(read_only=True)
    assignee_info = UserInfoSerializer(source="assignee", read_only=True)

    # Write-only field for inputting assignee ID
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True, write_only=True
    )

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
        )
        read_only_fields = ("creator", "created_at", "updated_at")


class TaskListSerializer(TaskBaseSerializer):
    """
    Optimized for lists: Shows count, hides actual comments.
    """

    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta(TaskBaseSerializer.Meta):
        fields = TaskBaseSerializer.Meta.fields + ("comments_count",)


class TaskDetailSerializer(TaskBaseSerializer):
    """
    Optimized for details: Shows actual comments, hides count.
    """

    comments = CommentSerializer(many=True, read_only=True)

    class Meta(TaskBaseSerializer.Meta):
        fields = TaskBaseSerializer.Meta.fields + ("comments",)

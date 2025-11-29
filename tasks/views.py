from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets

from .models import Comment
from .models import Task
from .permissions import IsEditorOrReadOnly
from .serializers import CommentSerializer
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    CRUD for Tasks.
    - Filtering: status, assignee
    - Ordering: created_at
    - Search: title, description
    """

    queryset = Task.objects.select_related("creator", "assignee").all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsEditorOrReadOnly]

    # Built-in DRF filtering tools
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "assignee"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at", "status"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        # Automatically set the creator to the current user
        serializer.save(creator=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD for Comments.
    """

    queryset = Comment.objects.select_related("author", "task").all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsEditorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["task"]  # Allow getting comments for specific task

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

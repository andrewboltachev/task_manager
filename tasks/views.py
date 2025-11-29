from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from .models import Comment, Task
from .permissions import IsEditorOrReadOnly
from .serializers import CommentSerializer, TaskDetailSerializer, TaskListSerializer


class TaskViewSet(viewsets.ModelViewSet):
    # We optimize the queryset to prefetch comments only when needed,
    # but for simplicity in get_serializer_class logic, we usually select globally
    # or override get_queryset.
    # Here we select basics.
    queryset = Task.objects.select_related("creator", "assignee").all()

    permission_classes = [permissions.IsAuthenticated, IsEditorOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "assignee"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at", "status"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        """
        Switch serializers based on the action.
        """
        if self.action == "list":
            return TaskListSerializer
        # For retrieve, create, update, etc., return the detailed view
        # so the user sees the immediate result including comments (if any)
        return TaskDetailSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        """
        Optional Optimization:
        Only prefetch comments if we are actually retrieving details.
        """
        queryset = super().get_queryset()
        if self.action == "retrieve":
            return queryset.prefetch_related("comments__author")
        return queryset


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

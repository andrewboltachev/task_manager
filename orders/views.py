from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Comment, Order
from .permissions import IsEditorOrReadOnly
from .serializers import CommentSerializer, OrderDetailSerializer, OrderListSerializer


class OrderPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class OrderViewSet(viewsets.ModelViewSet):
    # We optimize the queryset to prefetch comments only when needed,
    # but for simplicity in get_serializer_class logic, we usually select globally
    # or override get_queryset.
    # Here we select basics.
    queryset = Order.objects.select_related("creator", "assignee").all()

    permission_classes = [permissions.IsAuthenticated, IsEditorOrReadOnly]
    pagination_class = OrderPagination

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
            return OrderListSerializer
        # For retrieve, create, update, etc., return the detailed view
        # so the user sees the immediate result including comments (if any)
        return OrderDetailSerializer

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

    queryset = Comment.objects.select_related("author", "order").all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsEditorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["order"]  # Allow getting comments for specific task

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

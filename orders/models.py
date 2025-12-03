from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    # Who created the task
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_orders"
    )

    # Who is responsible for the task (Optional)
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_orders",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_editors(self):
        return [self.creator, self.assignee]


class Comment(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="order_comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.order}"

    def get_editors(self):
        return [self.author, *self.order.get_editors()]

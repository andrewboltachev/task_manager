from rest_framework.routers import DefaultRouter

from .views import CommentViewSet
from .views import TaskViewSet


router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="task")
router.register("comments", CommentViewSet, basename="comment")

urlpatterns = router.urls

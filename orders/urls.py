from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, OrderViewSet

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="order")
router.register("comments", CommentViewSet, basename="comment")

urlpatterns = router.urls

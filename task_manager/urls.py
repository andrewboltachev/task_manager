from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # 1. Django Admin
    path("admin/", admin.site.urls),
    # 2. Documentation (drf-spectacular)
    # Generates the YAML file schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # UI: Swagger (interactive)
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # UI: Redoc (static, readable)
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # 3. Authentication (SimpleJWT)
    # POST username/password -> returns Access + Refresh Token
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # POST refresh token -> returns new Access Token
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # POST token -> checks if valid (optional but useful)
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # 4. Apps (Versioned API)
    path("api/v1/users/", include("users.urls")),
    path("api/v1/tasks/", include("tasks.urls")),
    path("api/v1/orders/", include("orders.urls")),
]

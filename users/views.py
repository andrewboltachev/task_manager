from django.contrib.auth.models import User
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from .serializers import UserRegistrationSerializer


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    A ViewSet for user registration (creating a new user).
    It only implements the 'create' action (POST).
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

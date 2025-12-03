from django.core.exceptions import ImproperlyConfigured
from rest_framework import permissions


class IsEditorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow creators of an object to delete it.
    Using this assumes the model has a get_owner method
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            editors = obj.get_editors()
        except AttributeError as e:
            raise ImproperlyConfigured(
                "IsCreatorOrReadOnly should only be used with a model "
                "implementing get_editors() method"
            ) from e
        else:
            return request.user in editors

from rest_framework import permissions


class UpdateOwnBookProfile(permissions.BasePermission):
    """Allow user to edit their own book profile"""

    def has_object_permission(self, request, view, obj):
        """Check user ir trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
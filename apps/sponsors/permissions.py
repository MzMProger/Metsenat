from rest_framework.permissions import BasePermission


class SponsorPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            return True
        return bool(request.user.is_authenticated and request.user.is_superuser)

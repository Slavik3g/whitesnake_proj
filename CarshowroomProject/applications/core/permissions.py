from rest_framework import permissions


class IsEmailConfirmed(permissions.BasePermission):
    message = 'Email is not confirmed. Please verify your email first.'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_confirmed

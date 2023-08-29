from rest_framework import permissions

from contractManager.models import Role


class IsSalesUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == Role.SALES


class IsManagementUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == Role.MANAGEMENT


class IsSupportUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f"request.user.role: {request.user.role.name == 'Support'}")
        return request.user.role.name == "Support"

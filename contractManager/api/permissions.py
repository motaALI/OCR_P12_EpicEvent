from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission

from contractManager.models import Role



class IsSalesUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.SALES


class IsManagementUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.MANAGEMENT


class IsSupportUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f"request.user.role: {request.user.role.name == 'Support'}")
        return request.user.role.name == 'Support'
    
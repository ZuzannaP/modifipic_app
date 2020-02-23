from rest_framework import permissions


class GetPostOrAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'GET':
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET'or request.method == 'POST':
            return True

        return request.user and request.user.is_authenticated

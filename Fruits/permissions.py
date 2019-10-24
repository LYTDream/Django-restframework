from rest_framework.permissions import BasePermission

from Fruits.models import FruitUser


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        # print(request.user)
        return isinstance(request.user, FruitUser)

    def has_object_permission(self, request, view, obj):
        print(self)
        print(obj)
        return request.user.id == obj.id


class CartUserPermission(BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        return isinstance(request.user, FruitUser)

    def has_object_permission(self, request, view, obj):
        print(request.user)
        print(obj)
        return request.user.id == obj.c_user.id
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    This class verifies if the user is owner of the account to have
    acess to specific actions like create, update or delete a recipe.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

from rest_framework.permissions import BasePermission, SAFE_METHODS


# Custom permissions class
class CustomUserPermission(BasePermission):

    def has_permission(self, request, view):
        # Allows user creation for everyone
        if request.method == "POST" and view.action == "create":
            return True

        # For listing methods, authentication is required
        if request.method in SAFE_METHODS and view.action == "list":
            return request.user.is_authenticated

        # For other methods (PATCH, DELETE), authentication is required
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allows only read methods (GET, HEAD, OPTIONS) for authenticated users
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        # Only the owner can make changes
        return obj == request.user

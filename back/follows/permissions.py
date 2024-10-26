from rest_framework.permissions import BasePermission


class FollowPermission(BasePermission):
    """
    Permission that allows:
    - Any authenticated user to follow another user (POST).
    - Only the author of the follow to undo (DELETE) the follow.
    - Does not allow editing (PUT or PATCH), meaning it's either follow or unfollow.
    """

    def has_permission(self, request, view):
        # Allow authenticated users to make GET or POST requests
        if request.method in ["GET", "POST"]:
            return request.user.is_authenticated
        # Allow the removal of a follow
        elif request.method == "DELETE":
            return request.user.is_authenticated
        # Do not allow PUT or PATCH
        return False

    def has_object_permission(self, request, view, obj):
        # Allows only the "follower" (who is following) to delete the follow
        return obj.follower == request.user

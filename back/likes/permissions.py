from rest_framework.permissions import BasePermission


class LikePermission(BasePermission):
    """
    Permission that allows:
    - Any authenticated user to like a tweet (POST).
    - Only the author of the like can undo (DELETE) the like.
    - Does not allow editing (PUT or PATCH), meaning it is either a like or an unlike.
    """

    def has_permission(self, request, view):
        # Allow authenticated users to perform GET or POST
        if request.method in ["GET", "POST"]:
            return request.user.is_authenticated
        # Allow the removal of a like
        elif request.method == "DELETE":
            return request.user.is_authenticated
        # Do not allow PUT or PATCH
        return False

    def has_object_permission(self, request, view, obj):
        # Allows only the one who liked (the owner of the like) to delete (unlike) it
        return obj.user == request.user

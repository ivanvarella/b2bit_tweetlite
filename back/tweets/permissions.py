from rest_framework.permissions import BasePermission, SAFE_METHODS


# Custom permission class
class TweetPermission(BasePermission):
    """
    Permission that allows:
    - Any authenticated user to read any tweet. - Ok
    - Only the author of a tweet can edit, delete, or modify it.
    - A user can only create tweets in their own name.
    """

    def has_object_permission(self, request, view, obj):
        # Allows reading for any authenticated user
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        # Allows changes only if the user is the author of the tweet
        return obj.author == request.user

    def has_permission(self, request, view):
        # Allow read actions for any authenticated user
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        # Checks if it is an attempt to create a new tweet (POST)
        if request.method == "POST" and view.action == "create":
            # Attempts to get the "author" field from request.data
            author_id = request.data.get("author", None)

            if author_id is None:
                # If the "author" field is not passed, assume the author is the authenticated user
                request.data["author"] = (
                    request.user.id
                )  # Sets the author as the authenticated user

            else:
                # If the "author" field is passed, checks if the author matches the authenticated user
                if str(author_id) == str(request.user.id):
                    return True  # Allows tweet creation for the specified author
                else:
                    return False  # Denies creation if the author does not match the authenticated user

        return super().has_permission(request, view)

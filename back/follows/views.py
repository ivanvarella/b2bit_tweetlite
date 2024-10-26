# Django DRF
from rest_framework import viewsets

# Django RQL
from dj_rql.drf import RQLFilterBackend
from follows.filters import FollowFilterClass

from follows.models import Follow

# Serializers
from follows.serializers import FollowModelSerializer

# For custom permissions
from follows.permissions import FollowPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Custom actions
from rest_framework.decorators import action


# ViewSet
class FollowModelViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowModelSerializer

    # RQL configs:
    filter_backends = [RQLFilterBackend]
    rql_filter_class = FollowFilterClass

    # Permissions:
    permission_classes = [FollowPermission]

    # Custom actions to count followers and following
    @action(detail=False, methods=["get"], url_path="follow-counts")
    def follow_counts(self, request):
        self.permission_classes = [IsAuthenticated]  # More specific permissions
        self.check_permissions(request)  # Check permissions

        # Get the user_id passed in the request parameters
        user_id = request.query_params.get("user_id")
        if user_id is None:
            return Response({"error": "user_id is required."}, status=400)

        # Use the user_id passed in the request to count followers
        followers_count = Follow.get_followers_count(
            user_id
        )  # Call the function to count followers

        # Use the user_id passed in the request to count following
        following_count = Follow.get_following_count(
            user_id
        )  # Call the function to count following
        return Response(
            {
                "followers_count": followers_count,
                "following_count": following_count,
            }
        )

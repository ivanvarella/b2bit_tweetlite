# Django DRF
from rest_framework import viewsets

# Django RQL
from dj_rql.drf import RQLFilterBackend
from likes.filters import LikeFilterClass

from likes.models import Like

# Serializers
from likes.serializers import LikeModelSerializer

# For custom permissions
from likes.permissions import LikePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Custom actions
from rest_framework.decorators import action


# ViewSet
class LikeModelViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeModelSerializer

    # RQL configs:
    filter_backends = [RQLFilterBackend]
    rql_filter_class = LikeFilterClass

    # Permissions:
    permission_classes = [LikePermission]

    # Custom action to count the number of likes for a tweet
    @action(detail=False, methods=["get"], url_path="tweet-likes-count")
    def tweet_likes_count(self, request):
        self.permission_classes = [IsAuthenticated]  # More specific permissions
        self.check_permissions(request)  # Check permissions

        # Get the tweet_id passed in the request parameters
        tweet_id = request.query_params.get("tweet")
        if tweet_id is None:
            return Response({"error": "tweet is required."}, status=400)

        try:
            # Call the Like model method to count the likes
            likes_count = Like.get_likes_count(tweet_id)
            return Response({"likes_count": likes_count})
        except Like.DoesNotExist:
            return Response({"error": "Tweet not found."}, status=404)

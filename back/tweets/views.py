# Django DRF
from rest_framework import viewsets

# Django RQL
from dj_rql.drf import RQLFilterBackend
from tweets.filters import TweetFilterClass

from tweets.models import Tweet
from follows.models import Follow

# Serializers
from tweets.serializers import TweetModelSerializer

# Permissions
from tweets.permissions import TweetPermission
from rest_framework.permissions import IsAuthenticated

# Custom actions
from rest_framework.decorators import action
from rest_framework.response import Response


# ViewSet
class TweetModelViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetModelSerializer

    # RQL configs:
    filter_backends = [RQLFilterBackend]
    rql_filter_class = TweetFilterClass

    # Permissions:
    permission_classes = [TweetPermission]

    # Endpoint to get tweets from users followed by the authenticated user
    @action(detail=False, methods=["get"], url_path="user-feed")
    def user_feed(self, request):
        """
        Returns tweets from users that the authenticated user follows.
        """

        self.permission_classes = [IsAuthenticated]  # More specific permissions
        self.check_permissions(request)  # Check permissions

        # Get the authenticated user
        user = request.user

        # Get IDs of users that the authenticated user follows
        followed_users = Follow.objects.filter(follower=user).values_list(
            "following", flat=True
        )

        # Filter tweets from followed users
        tweets = Tweet.objects.filter(author__in=followed_users)

        # Paginating the queryset
        page = self.paginate_queryset(
            tweets
        )  # Use paginate_queryset to apply pagination

        if page is not None:
            serializer = TweetModelSerializer(page, many=True)
            return self.get_paginated_response(
                serializer.data
            )  # Returns the paginated response

        # If there's no pagination (in case of a short list)
        serializer = TweetModelSerializer(tweets, many=True)
        return Response(serializer.data)

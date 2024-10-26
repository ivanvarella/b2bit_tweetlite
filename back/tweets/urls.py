from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tweets.views import TweetModelViewSet

router = DefaultRouter()
router.register("tweets", TweetModelViewSet)  # Route -> endpoint


# Register for Django to use as the system path
urlpatterns = [
    path("", include(router.urls)),
]

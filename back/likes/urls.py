from django.urls import path, include
from rest_framework.routers import DefaultRouter
from likes.views import LikeModelViewSet

router = DefaultRouter()
router.register("likes", LikeModelViewSet)  # Route -> endpoint


# Register for Django to use as the system path
urlpatterns = [
    path("", include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from follows.views import FollowModelViewSet

router = DefaultRouter()
router.register("follows", FollowModelViewSet)  # Route -> endpoint


# Register for Django to use as system path
urlpatterns = [
    path("", include(router.urls)),
]

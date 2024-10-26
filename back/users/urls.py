from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import CustomUserModelViewSet

router = DefaultRouter()
router.register("users", CustomUserModelViewSet)  # Route -> endpoint


# Registers for Django to use as the system path
urlpatterns = [
    path("", include(router.urls)),
]

# Django DRF
from rest_framework import viewsets

# Django RQL
from dj_rql.drf import RQLFilterBackend
from users.filters import CustomUserFilterClass

from users.models import CustomUser

# Serializers
from users.serializers import CustomUserModelSerializer

# Para permissões personalizadas
from users.permissions import CustomUserPermission


# ViewSet
class CustomUserModelViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserModelSerializer

    # RQL:
    filter_backends = [RQLFilterBackend]
    rql_filter_class = CustomUserFilterClass

    # Permissions:
    permission_classes = [CustomUserPermission]

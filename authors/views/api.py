from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..serializers import AuthorSerializer


class AuthorViewSet(ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated,]
    http_method_names = ['get']

    def get_queryset(self):
        user = get_user_model()
        queryset = user.objects.filter(username=self.request.user.username)

        return queryset

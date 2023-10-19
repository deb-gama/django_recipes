from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "email", "last_name"]

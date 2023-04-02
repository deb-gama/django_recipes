from rest_framework import serializers
from django.contrib.auth.models import User

class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    category_name = serializers.StringRelatedField(source='category')
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

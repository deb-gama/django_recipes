from rest_framework import serializers
from recipes.models import Category

class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    category_name = serializers.StringRelatedField(source='category')

from rest_framework import serializers
from django.contrib.auth.models import User
from recipes.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model =Recipe
        fields = ['id','title','description','category_name','author', 'public']

    category_name = serializers.StringRelatedField(source='category')
    public = serializers.BooleanField(
        source='is_published',
        read_only=True,
    )


from collections import defaultdict
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

    def validate(self, attrs):
        super_validate = super().validate(attrs)
        title = attrs.get('title')
        description = attrs.get('description')

        if title == description:
            raise serializers.ValidationError(
                {
                "title": ["Cannot be equal to description", "Please give another title"],
                "description": ["Cannot be equal to title", "Please try another description"]
                }
            )

        return super_validate


    def validate_title(self, value):
        title = value

        if len(title) < 5:
            raise serializers.ValidationError('Must have at least 5 chars.')
        return title


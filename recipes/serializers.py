from rest_framework import serializers
from django.contrib.auth.models import User
from recipes.models import Recipe
from authors.validators import AuthorCreateRecipeValidator

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
        AuthorCreateRecipeValidator(data=attrs, error_class=serializers.ValidationError)

        return super_validate





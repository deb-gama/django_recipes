
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer

@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(instance=recipes, many=True, context={'request':request})

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )



@api_view()
def recipe_api_detail(request, pk):
    recipe = Recipe.objects.get_published().filter(pk=pk).first()

    if recipe:
        serializer = RecipeSerializer(instance=recipe, many=False)
        return Response(serializer.data)
    else:
        return Response({
            'detail': 'Sorry. This recipe don´t exist. Try another id.'
        }, status= status.HTTP_404_NOT_FOUND)

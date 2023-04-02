# from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from django.shortcuts import get_object_or_404

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer

@api_view()
def recipe_api_list(request):
    recipes = Recipe.objects.get_published()[:10]
    serializer = RecipeSerializer(instance=recipes, many=True)

    return Response(serializer.data)

@api_view()
def recipe_api_detail(request, pk):
    recipe = Recipe.objects.get_published().filter(pk=pk).first()

    if recipe:
        serializer = RecipeSerializer(instance=recipe, many=False)
        return Response(serializer.data)
    else:
        return Response({
            'detail': 'Sorry. This recipe don´t exist. Try another id.'
        }, status= HTTP_404_NOT_FOUND)

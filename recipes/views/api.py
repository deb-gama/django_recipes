
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


class RecipeAPIv1Pagination(PageNumberPagination):
    page_size = 3


class RecipeAPIv1ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv1Pagination


# This code block was replaced by ViewSet for avoid duplication
# class RecipesAPIv1List(ListCreateAPIView):
#     """
#     View that contains the get and post methods and have the same url without a pk in it.
#     The 'get' method list recipes and the 'post' method create a new recipe.
#     """
#     queryset = Recipe.objects.get_published()
#     serializer_class = RecipeSerializer
#     pagination_class = RecipeAPIv1Pagination

# class RecipeAPIv1Detail(RetrieveUpdateDestroyAPIView):
#     """
#     View that contains the read, patch and delete methods and have the same url with a pk in it.
#     The 'get' method list recipes and the 'post' method create a new recipe.
#     """
#     queryset = Recipe.objects.get_published()
#     serializer_class = RecipeSerializer
#     pagination_class = RecipeAPIv1Pagination

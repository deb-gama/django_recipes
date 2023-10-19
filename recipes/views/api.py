from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from recipes.models import Recipe
from recipes.permissions import IsOwner
from recipes.serializers import RecipeSerializer

from ..permissions import IsOwner

# from rest_framework.decorators import api_view
# from rest_framework.generics import (ListCreateAPIView,


class RecipeAPIv1Pagination(PageNumberPagination):
    page_size = 3


class RecipeAPIv1ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv1Pagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    http_method_names = ["get", "options", "head", "patch", "post", "delete"]

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get("category_id", "")

        if category_id != "" and category_id.isnumeric():
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_object(self):
        pk = self.kwargs.get("pk", "")
        obj = get_object_or_404(self.get_queryset(), pk=pk)

        self.check_object_permissions(self.request, obj)

        return obj

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [
                IsOwner(),
            ]

        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


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

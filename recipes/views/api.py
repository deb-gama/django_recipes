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

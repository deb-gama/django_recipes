
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


class RecipesAPIv1List(APIView):
    """
    View that contains the get anmd post methods and have the same url without a pk in it.
    The 'get' method list recipes and the 'post' method create a new recipe.
    """
    def get(self, request):
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(instance=recipes, many=True, context={'request':request})

        return Response(serializer.data)

    def post(self, request):
        serializer = RecipeSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save(
            # author_id=1, category_id=1
        )

        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )


class RecipeAPIv1Detail(APIView):
    def get_recipe(self, pk):
        recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)

        return recipe

    def get(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            context={'request':request},
        )
        return Response(serializer.data)

    def patch(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(
            instance=recipe,
            data = request.data,
            many=False,
            context={'request':request},
            partial = True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
        )

    def delete(self, request, pk):
        recipe = self.get_recipe(pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




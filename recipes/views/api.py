
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer

@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request):
    """
    View that contains the get anmd post methods and have the same url without a pk in it.
    The 'get' method list recipes and the 'post' method create a new recipe.
    """
    if request.method == 'GET':
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(instance=recipes, many=True, context={'request':request})

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RecipeSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save(
            # author_id=1, category_id=1
        )

        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )



@api_view(http_method_names=['get', 'patch', 'delete'])
def recipe_api_detail(request, pk):
    """
    View that container all the methods that needs a ph to be finished. Read,
    delete or update an specific recipe.
    """
    recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk)

    if request.method == 'GET':
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            context={'request':request},
        )
        return Response(serializer.data)

    elif request.method == 'PATCH':
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

    elif request.method == 'DELETE':
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



    # else:
    #     return Response({
    #         'detail': 'Sorry. This recipe don´t exist. Try another id.'
    #     }, status= status.HTTP_404_NOT_FOUND)

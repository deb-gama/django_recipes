from django.shortcuts import get_list_or_404, get_object_or_404, render

from recipes.models import Recipe


def home(request):
    title = 'Home | Recipes'
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(
        request,
        'recipes/pages/home.html',
        context={'title': title, 'recipes': recipes}
    )


def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, is_published=True)
    title = f"{recipe.title} | Recipes'"
    return render(
        request,
        'recipes/pages/recipe_detail.html',
        context={'title': title, 'recipe': recipe, 'is_detail_page': True}
    )


def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_id).order_by('-id'))
    title = f"{recipes[0].category.name} - Category | Recipes'"
    return render(
        request,
        'recipes/pages/category.html',
        context={'title': title, 'recipes': recipes}
    )

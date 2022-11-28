from django.shortcuts import render
from django.http import HttpResponse
from recipes.utils.factory import make_recipe
from recipes.models import Recipe

def home(request):
    title = 'Home | Recipes'
    recipes = Recipe.objects.all().order_by('-id')
    return render(request, 'recipes/pages/home.html', {'title': title, 'recipes': recipes })

def recipe(request, recipe_id):
    title = 'Details | Recipes'
    return render(request, 'recipes/pages/recipe_detail.html', {'title': title, 'recipe': make_recipe(), 'is_detail_page': True})


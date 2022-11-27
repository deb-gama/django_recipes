from django.shortcuts import render
from django.http import HttpResponse
from recipes.utils.factory import make_recipe

def home(request):
    title = 'Home | Recipes'
    return render(request, 'recipes/pages/home.html', {'title': title, 'recipes': [make_recipe() for _ in range(10) ] })

def recipe(request, recipe_id):
    title = 'Details | Recipes'
    return render(request, 'recipes/pages/recipe_detail.html', {'title': title, 'recipe': make_recipe(), 'is_detail_page': True})


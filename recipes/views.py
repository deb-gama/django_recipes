from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from recipes.models import Recipe

from .utils.pagination import make_pagination_range


def home(request):
    title = 'Home | Recipes'
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(recipes, 9)
    page_object = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page
    )

    return render(
        request,
        'recipes/pages/home.html',
        context={'title': title, 'recipes': page_object,
                 'pagination_range': pagination_range}
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
    title = f"{recipes[0].category.name} - Category | Recipes"
    return render(
        request,
        'recipes/pages/category.html',
        context={'title': title, 'recipes': recipes}
    )


def search(request):
    # strip tira espaços da string
    search_term = request.GET.get('q', '').strip()
    title = f'Search for "{search_term}" | Recipes'

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(Q(title__icontains=search_term) | Q(
            description__icontains=search_term)), is_published=True,
    ).order_by('-id')

    return render(
        request,
        'recipes/pages/search_page.html',
        context={
            'title': title,
            'search_term': search_term,
            'recipes': recipes},
    )

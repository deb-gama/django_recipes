import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import ListView

from recipes.models import Recipe

from .utils.pagination import make_pagination

PER_PAGES = int(os.environ.get('PER_PAGE', 6))

class RecipesListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering =  ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args,**kwargs):
        query_set = super().get_queryset(*args,**kwargs)
        query_set = query_set.filter(
            is_published=True,
        )
        return query_set

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)

        page_object, pagination_range = make_pagination(
            self.request,
            context.get('recipes'),
            PER_PAGES
        )

        context.update(
            {
                'recipes': page_object,
                'pagination_range': pagination_range
            }
        )

        return context


class RecipesListViewHome(RecipesListViewBase):
    template_name = 'recipes/pages/home.html'




#These methods below are no longer being used. We refactored the home method using CBV,
# but this code snippet is still here for teaching purposes only
def home(request):
    title = 'Home | Recipes'
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_object, pagination_range = make_pagination(
        request, recipes, PER_PAGES)

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

    page_object, pagination_range = make_pagination(
        request, recipes, PER_PAGES)

    return render(
        request,
        'recipes/pages/category.html',
        context={'title': title, 'recipes': page_object,
                 'pagination_range': pagination_range}
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

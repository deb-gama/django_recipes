import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import ListView

from recipes.models import Recipe

from ..utils.pagination import make_pagination

PER_PAGES = int(os.environ.get("PER_PAGE", 6))


class RecipesListViewBase(ListView):
    model = Recipe
    context_object_name = "recipes"
    paginate_by = None
    ordering = ["-id"]
    template_name = "recipes/pages/home.html"

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            is_published=True,
        )
        return query_set

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        page_object, pagination_range = make_pagination(
            self.request, context.get("recipes"), PER_PAGES
        )

        context.update({"recipes": page_object, "pagination_range": pagination_range})

        return context


class RecipesListViewHome(RecipesListViewBase):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        title = "Home | Recipes"

        context.update({"title": title})
        return context


class RecipesListCategory(RecipesListViewBase):
    template_name = "recipes/pages/category.html"

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)

        query_set.filter(category__id=self.kwargs.get("category_id"))

        return query_set

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        recipes = get_list_or_404(
            Recipe.objects.filter(category__id=self.kwargs.get("category_id")).order_by(
                "-id"
            )
        )
        title = f"{recipes[0].category.name} - Category | Recipes"
        page_object, pagination_range = make_pagination(
            self.request, recipes, PER_PAGES
        )

        context.update(
            {
                "title": title,
                "recipes": page_object,
                "pagination_range": pagination_range,
            }
        )
        return context


class RecipesListSearch(RecipesListViewBase):
    template_name = "recipes/pages/search_page.html"

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get("q", "").strip()
        if not search_term:
            raise Http404()

        query_set = super().get_queryset(*args, **kwargs)
        query_set = query_set.filter(
            Q(Q(title__icontains=search_term) | Q(description__icontains=search_term))
        ).order_by("-id")

        return query_set

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get("q", "").strip()
        title = f'Search for "{search_term}" | Recipes'

        context.update(
            {
                "title": title,
                "search_term": search_term,
            }
        )
        return context

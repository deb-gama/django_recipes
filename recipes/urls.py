from django.urls import path

from recipes.views import site

app_name = 'recipes'

urlpatterns = [
    path("", site.RecipesListViewHome.as_view(), name="home"),
    path("recipes/search/", site.RecipesListSearch.as_view(), name="search"),
    path(
        "recipes/category/<int:category_id>/",
        site.RecipesListCategory.as_view(), name="category"
    ),
    path("recipes/<int:recipe_id>/", site.recipe, name="recipe"),

]

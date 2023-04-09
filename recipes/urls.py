from django.urls import path

from recipes import views

app_name = 'recipes'

urlpatterns = [
    path("", views.RecipesListViewHome.as_view(), name="home"),
    path("recipes/search/", views.RecipesListSearch.as_view(), name="search"),
    path(
        "recipes/category/<int:category_id>/",
        views.RecipesListCategory.as_view(), name="category"
    ),
    path("recipes/<int:recipe_id>/", views.recipe, name="recipe"),
    path("recipes/api/v1/", views.RecipesAPIv1List.as_view(), name="recipe_api_v1"),
    path("recipes/api/v1/<int:pk>", views.RecipeAPIv1Detail.as_view(), name="recipe_api_v1_detail"),
]

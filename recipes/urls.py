from django.urls import path

from recipes import views

app_name = 'recipes'

urlpatterns = [
    path("", views.RecipesListViewHome.as_view(), name="home"),
    path("recipes/search/", views.search, name="search"),
    path(
        "recipes/category/<int:category_id>/",
        views.category, name="category"
    ),
    path("recipes/<int:recipe_id>/", views.recipe, name="recipe"),

]

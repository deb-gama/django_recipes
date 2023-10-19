from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from recipes import views

app_name = "recipes"

recipes_api_v1_router = SimpleRouter()
recipes_api_v1_router.register(
    "recipes/api/v1",
    views.RecipeAPIv1ViewSet,
)

urlpatterns = [
    path("", views.RecipesListViewHome.as_view(), name="home"),
    path("recipes/search/", views.RecipesListSearch.as_view(), name="search"),
    path(
        "recipes/category/<int:category_id>/",
        views.RecipesListCategory.as_view(),
        name="category",
    ),
    path("recipes/<int:recipe_id>/", views.recipe, name="recipe"),
    path("recipes/api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "recipes/api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("recipes/api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # This code block was replaced by simpleRouter definitions that create the detail and list urls
    # automactilly
    # path("recipes/api/v1/", views.RecipeAPIv1ViewSet.as_view(
    #     {'get': 'list',
    #      'post': 'create',
    #      }
    # ), name="recipe_api_v1"),
    # path("recipes/api/v1/<int:pk>", views.RecipeAPIv1ViewSet.as_view(
    #     {
    #         'get': 'retrieve',
    #         'patch': '',
    #         'delete': 'destroy',
    #     }
    # ), name="recipe_api_v1_detail"),
]

urlpatterns += recipes_api_v1_router.urls

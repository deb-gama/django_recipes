from django.urls import path, include
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
    path("recipes/<int:pk>/", views.RecipeDetailView.as_view(), name="recipe"),
    path("recipes/api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "recipes/api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("recipes/api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("", include(recipes_api_v1_router.urls)),
]

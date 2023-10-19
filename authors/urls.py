from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

app_name = "authors"
author_api_router = SimpleRouter()
author_api_router.register("api", views.AuthorViewSet, basename="author-api")

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("register/create/", views.register_create, name="register_create"),
    path("login/", views.login_view, name="login"),
    path("login/create/", views.login_create, name="login_create"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path(
        "dashboard/recipe/create",
        views.DashboardRecipe.as_view(),
        name="dashboard_recipe_create",
    ),
    path(
        "dashboard/recipe/delete/",
        views.DashboardRecipeDelete.as_view(),
        name="dashboard_recipe_delete",
    ),
    path(
        "dashboard/recipe/<int:recipe_id>/edit/",
        views.DashboardRecipe.as_view(),
        name="dashboard_recipe_edit",
    ),
]

urlpatterns += author_api_router.urls

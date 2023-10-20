from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from authors.forms import AuthorRecipeForm, AuthorCreateRecipeForm
from recipes.models import Recipe


# decorating dispatch method of generic View
@method_decorator(
    login_required(login_url="authors:login", redirect_field_name=next), name="dispatch"
)
class DashboardRecipe(View):
    def render_recipe(self, form, title, recipe, is_dashboard):
        return render(
            self.request,
            "authors/pages/dashboard_recipe.html",
            context={
                "title": title,
                "recipe": recipe,
                "form": form,
                "is_dashboard_page": is_dashboard,
            },
        )

    def get_recipe(self, recipe_id=None):
        recipe = None

        if recipe_id is not None:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=recipe_id,
            ).first()

            if not recipe:
                raise Http404()

        return recipe

    def get(self, request, recipe_id=None):
        recipe = self.get_recipe(recipe_id)
        title = "Authors | Dashboard Edit Recipe"
        form = AuthorRecipeForm(instance=recipe)
        is_dashboard = True

        return self.render_recipe(form, title, recipe, is_dashboard)

    def post(self, request, recipe_id=None):
        recipe = self.get_recipe(recipe_id)
        title = "Authors | Dashboard Edit Recipe"
        form = AuthorCreateRecipeForm(
            data=request.POST or None, files=request.FILES or None, instance=recipe
        )

        if form.is_valid():
            # salvando os dados na variável antes de salvar na base de dados
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_step_is_html = False
            recipe.is_published = False

            # salvando na base de dados após verifcações feitas acima
            recipe.save()
            messages.success(request, "Your recipe was saved!")
            return redirect(reverse("authors:dashboard_recipe_edit", args=(recipe.id,)))

        return self.render_recipe(form, title, recipe,is_dashboard)


@method_decorator(
    login_required(login_url="authors:login", redirect_field_name=next), name="dispatch"
)
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get("id"))
        recipe.delete()

        messages.success(self.request, "Deleted successfully")
        return redirect("authors:dashboard")

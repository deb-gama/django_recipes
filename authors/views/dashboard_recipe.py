from django.views import View
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from recipes.models import Recipe
from authors.forms import AuthorRecipeForm


class DashboardRecipe(View):
    def render_recipe(self,form,title,recipe):
        return render(
            self.request,
            'authors/pages/dashboard_recipe.html',
            context= {
                'title': title,
                'recipe': recipe,
                'form': form,
            }
        )

    def get_recipe(self, recipe_id):
        recipe = None

        if recipe_id:
            recipe = Recipe.objects.filter(
                is_published=False,
                author = self.request.user,
                pk = recipe_id,
            ).first()

            if not recipe:
                raise Http404()

        return recipe

    def get(self,request, recipe_id):
        recipe = self.get_recipe(recipe_id)
        title = 'Authors | Dashboard Edit Recipe'
        form = AuthorRecipeForm(instance=recipe)

        return self.render_recipe( form, title, recipe)


    def post(self, request, recipe_id):
        recipe = self.get_recipe(recipe_id)
        title = 'Authors | Dashboard Edit Recipe'
        form = AuthorRecipeForm(request.POST or None,files=request.FILES or None, instance=recipe)

        if form.is_valid():
            # salvando os dados na variável antes de salvar na base de dados
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_step_is_html = False
            recipe.is_published = False

            # salvando na base de dados após verifcações feitas acima
            recipe.save()
            messages.success(request, 'Your recipe was saved!')
            return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe_id,)))

        return self.render_recipe(form, title, recipe)



from django.urls import resolve, reverse
from recipes.views import site
from .recipe_base_test import RecipeTestBase


class RecipeDetailViewsTest(RecipeTestBase):
    def test_recipe_view_function(self):
        """
        Test must confirm if the correct view has been executed in recipe url
        """
        view = resolve(reverse("recipes:recipe", kwargs={"pk": 2}))
        self.assertIs(view.func.view_class, site.RecipeDetailView)

    def test_recipe_view_return_404_if_not_recipes_found(self):
        """
        Tests if recipe url returns a 'not found' status code when
        the recipe_id doesnt exists
        """

        response = self.client.get(reverse("recipes:recipe", kwargs={"pk": 2000}))
        self.assertEqual(response.status_code, 404)

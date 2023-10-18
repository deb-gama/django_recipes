from django.urls import resolve, reverse

from recipes.views import site

from .recipe_base_test import RecipeTestBase


class RecipeDetailViewsTest(RecipeTestBase):

    def test_recipe_view_function(self):
        """
        Test must confirm if the correct view has been executed in recipe url
        """
        view = resolve(self.recipe_url)
        (view.func, site.recipe)

    def test_recipe_view_return_404_if_not_recipes_found(self):
        """
        Tests if recipe url returns a 'not found' status code when
        the recipe_id doesnt exists
        """
        recipe_url = reverse(
            'recipes:recipe',
            kwargs={'recipe_id': 10000000000}
        )
        response = self.client.get(recipe_url)
        self.assertEqual(response.status_code, 404)

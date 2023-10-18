from django.urls import resolve, reverse

from recipes.views import site

from .recipe_base_test import RecipeTestBase


class RecipeCategoryViewsTest(RecipeTestBase):

    # def test_recipe_category_view_function(self):
    #     """
    #     Test must confirm if the correct view has been executed in category url
    #     """
    #     view = resolve(self.category_url)
    #     self.assertIs(view.func, views.category)

    def test_recipe_category_template_loads_the_correct_recipe(self):
        """
        Tests if the title is in html in the category url template
        """
        title = 'This is a category test'
        self.make_recipe(title=title)

        response = self.client.get(self.category_url)
        html_to_string = response.content.decode('utf-8')
        self.assertIn(title, html_to_string)

    def test_category_view_return_404_if_not_recipes_found(self):
        """
        Tests if category url returns a 'not found' status code when
        the category_id doesnt exists
        """
        category_url = reverse(
            'recipes:category',
            kwargs={'category_id': 10000000000}
        )
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, 404)

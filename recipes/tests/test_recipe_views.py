from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views


class RecipeViewsTest(TestCase):

    def setUp(self):
        self.id_category = 1
        self.category_url = reverse(
            'recipes:category',
            kwargs={'category_id': self.id_category}
        )
        self.recipe_id = 2
        self.recipe_url = reverse('recipes:recipe',
                                  kwargs={'recipe_id': self.recipe_id}
                                  )
        self.home_url = reverse('recipes:home')
        self.response_home = self.client.get(self.home_url)
        self.response_category = self.client.get(self.category_url)
        self.response_recipe = self.client.get(self.recipe_url)

    def test_recipe_home_view_function(self):
        """
        Test must confirm if the correct view has been executed in home url
        """
        # alternativa não dinâmica: resolve('/')
        view = resolve(self.home_url)
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function(self):
        """
        Test must confirm if the correct view has been executed in category url
        """
        view = resolve(self.category_url)
        self.assertIs(view.func, views.category)

    def test_recipe_view_function(self):
        """
        Test must confirm if the correct view has been executed in recipe url
        """
        view = resolve(self.recipe_url)
        self.assertIs(view.func, views.recipe)

    def test_home_view_return_status_code_200(self):
        """
        Tests if home url returns a 'ok' status code
        """
        self.assertEqual(self.response_home.status_code, 200)

    def test_home_view_render_correct_template(self):
        """
        Tests if home url render the correct template
        """
        self.assertTemplateUsed(self.response_home, 'recipes/pages/home.html')

    def test_recipe_home_view_with_no_recipes_found(self):
        """
        Tests if no recipes message appears in home page when there are not recipes to show
        """
        html_to_string = self.response_home.content.decode('utf-8')
        self.assertIn('No recipes here', html_to_string)

from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views


class RecipesURLsTest(TestCase):

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

    def test_recipe_home_url_is_correct(self):
        """
        Test must confirm wich url its been resolve for home
        """
        url = self.home_url
        self.assertEqual(url, '/')

    def test_recipe_category_url_is_correct(self):
        """
        Test must confirm wich url its been resolve for category
        """
        url = self.category_url
        self.assertEqual(url, f'/recipes/category/{self.id_category}/')

    def test_recipe_url_is_correct(self):
        """
        Test must confirm wich url its been resolve for recipe
        """
        url = self.recipe_url
        self.assertEqual(url, f'/recipes/{self.recipe_id}/')


class RecipeViewsTest(RecipesURLsTest):

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

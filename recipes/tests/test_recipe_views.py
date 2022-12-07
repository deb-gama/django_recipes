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

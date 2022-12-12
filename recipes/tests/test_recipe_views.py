from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views

from .recipe_base_test import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):

    def test_recipe_home_view_function(self):
        """
        Test must confirm if the correct view has been executed in home url
        """
        # alternativa não dinâmica: resolve('/')
        view = resolve(self.home_url)
        self.assertIs(view.func, views.home)

    def test_home_view_render_correct_template(self):
        """
        Tests if home url render the correct template
        """
        self.assertTemplateUsed(self.response_home, 'recipes/pages/home.html')

    def test_recipe_home_view_with_no_recipes_found(self):
        """
        Tests if no recipes message appears in home page when there are not
        recipes to show
        """
        html_to_string = self.response_home.content.decode('utf-8')
        self.assertIn('No recipes here', html_to_string)

    def test_recipe_home_view_is_rendering_the_recipe_posted(self):
        """
        Tests if recipe posted is in template that view has rendered
        """
        self.make_recipe()
        response = self.client.get(self.home_url)
        html_to_string = response.content.decode('utf-8')
        self.assertIn('some title', html_to_string)

    def test_home_view_return_status_code_200(self):
        """
        Tests if home url returns a 'ok' status code
        """
        self.assertEqual(self.response_home.status_code, 200)

    def test_home_view_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(self.home_url)
        query = response.context['recipes']
        self.assertEqual(query.count(), 1)

    def test_recipe_category_view_function(self):
        """
        Test must confirm if the correct view has been executed in category url
        """
        view = resolve(self.category_url)
        self.assertIs(view.func, views.category)

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

    def test_recipe_view_function(self):
        """
        Test must confirm if the correct view has been executed in recipe url
        """
        view = resolve(self.recipe_url)
        (view.func, views.recipe)

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

    def test_recipes_not_published_are_not_appearing_in_home_view(self):
        """
        Tests if recipes not published dont appear in home page.
        """
        title = 'Some recipe not published yet'
        self.make_recipe(
            is_published=False,
            title='Some recipe not published yet'
        )

        response = self.client.get(self.home_url)
        html_to_string = response.content.decode('utf-8')
        self.assertNotIn(title, html_to_string)
        self.assertIn('No recipes here', html_to_string)

    # TODO criar teste para receita não publicada nas views recipe e category

    def test_recipe_search_view_function(self):
        """
        Test must confirm if the correct view has been executed in search url
        """
        # alternativa não dinâmica: resolve('/')
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)

    def test_search_view_render_correct_template(self):
        """
        Tests if search url render the correct template
        """
        response = self.client.get(reverse('recipes:search'))
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

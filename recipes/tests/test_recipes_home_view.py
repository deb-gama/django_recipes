from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .recipe_base_test import RecipeTestBase


class RecipeHomeViewsTest(RecipeTestBase):

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

    # def test_home_view_template_loads_recipes(self):
    #     self.make_recipe()
    #     response = self.client.get(self.home_url)
    #     query = response.context['recipes']

    #     self.assertEqual(query.count(), 1)

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

    @patch('recipes.views.PER_PAGES', new='3')
    def test_recipe_home_is_paginated(self):

        for i in range(8):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
        self.assertEqual(len(paginator.get_page(3)), 2)

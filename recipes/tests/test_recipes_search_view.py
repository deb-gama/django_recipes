from django.urls import resolve, reverse

from recipes.views import site

from .recipe_base_test import RecipeTestBase


class RecipeSeacrhViewsTest(RecipeTestBase):
    # def test_recipe_search_view_function(self):
    #     """
    #     Test must confirm if the correct view has been executed in search url
    #     """
    #     # alternativa não dinâmica: resolve('/')
    #     view = resolve(self.search_url)
    #     self.assertIs(view.func, views.search)

    def test_search_view_render_correct_template(self):
        """
        Tests if search url render the correct template
        """
        response = self.client.get(reverse("recipes:search") + "?q=teste")
        self.assertTemplateUsed(response, "recipes/pages/search_page.html")

    def test_recipe_search_view_return_404_if_query_dont_exists(self):
        """
        Tests if recipe url returns a 'not found' status code when
        the value of the query was not found
        """
        url = self.search_url
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = self.search_url + "?q=Test"
        response = self.client.get(url)

        self.assertIn("Search for &quot;Test&quot;", response.content.decode("utf-8"))

    # def test_recipe_search_can_find_recipe_by_title(self):
    #     title_1 = 'This is recipe one'
    #     title_2 = 'This is recipe two'

    #     recipe_1 = self.make_recipe(
    #         slug='one',
    #         title=title_1,
    #         author_data={'username': 'one'}
    #     )

    #     recipe_2 = self.make_recipe(
    #         slug='two',
    #         title=title_2,
    #         author_data={'username': 'two'}
    #     )

    #     response_1 = self.client.get(f'{self.search_url}?q={title_1}')
    #     response_2 = self.client.get(f'{self.search_url}?q={title_2}')
    #     response_both = self.client.get(f'{self.search_url}?q=this')

    #     self.assertIn(recipe_1,
    #                   response_1.context['recipes'])

    #     self.assertNotIn(recipe_1,
    #                      response_2.context['recipes'])

    #     self.assertIn(recipe_2,
    #                   response_2.context['recipes'])

    #     self.assertNotIn(recipe_2,
    #                      response_1.context['recipes'])

    #     self.assertIn(recipe_2,
    #                   response_both.context['recipes'])

    #     self.assertIn(recipe_1,
    #                   response_both.context['recipes'])

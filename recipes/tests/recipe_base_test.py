from django.test import TestCase
from django.urls import reverse

from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    def setUp(self) -> None:
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

        return super().setUp()

    def make_recipe_category(self, name='category_test'):
        """
        Create a recipe category with name set by default value if the method
        dont get an argument.
        """
        return Category.objects.create(name=name)

    def make_recipe_author(
        self,
        first_name='John',
        last_name='Doe',
        username='john_doe',
        password='1234',
        email='john_doe@email.com'
    ):
        """
        Create a django user author with data set by default values if the
        method dont get any arguments
        """
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='some title',
        description='some description',
        slug='some-slug',
        preparation_time=10,
        preperation_time_unit='Minutos',
        servings=1,
        cover='https://some-image.com',
        servings_unit='Porções',
        preparation_step='some preparation step',
        preparation_step_is_html=False,
        is_published=True,
    ):
        """
        Create a recipe with data set by default values if the
        method dont get any arguments
        This method can be called in tests where recipes are necessary
        """

        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_recipe_category(**category_data),
            author=self.make_recipe_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preperation_time_unit=preperation_time_unit,
            servings=servings,
            cover=cover,
            servings_unit=servings_unit,
            preparation_step=preparation_step,
            preparation_step_is_html=preparation_step_is_html,
            is_published=is_published,
        )

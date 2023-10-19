from django.core.exceptions import ValidationError
from parameterized import parameterized

from .recipe_base_test import Category, Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_default(self):
        recipe = Recipe(
            category=self.make_recipe_category(name="Test new Category"),
            author=self.make_recipe_author(username="newuser"),
            title="some title",
            description="some description",
            slug="some-slug-1",
            preparation_time=10,
            preperation_time_unit="Minutos",
            servings=1,
            cover="https://some-image.com",
            servings_unit="Porções",
            preparation_step="some preparation step",
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    # def test_recipe_title_raises_error_if_bigger_than_field_max_length(self):
    #     """
    #     This test make the validation of recipe title max length raising a Validation Error
    #     """
    #     self.recipe.title = 'A'*70

    #     with self.assertRaises(ValidationError):
    #         self.recipe.full_clean()  # validação acontece aqui e o código
    # para

    # def test_recipe_description_raises_error_if_bigger_than_field_
    # max_length(self):
    #     """
    #     This test make the validation of recipe title max length raising a
    # Validation Error
    #     """
    #     self.recipe.description = 'A'*166
    #     self.recipe.full_clean()
    #     self.fail()

    # with self.assertRaises(ValidationError):

    @parameterized.expand(
        [
            ("title", 65),
            ("description", 165),
            ("preperation_time_unit", 10),
            ("servings_unit", 10),
        ]
    )
    def test_recipe_fields_max_length(self, field, max_length):
        """
        Testing max_length fields
        """
        # set object, campo que quer setar, valor
        setattr(self.recipe, field, "A" * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_false_by_default(self):
        """
        Test if the preparation_steps_is_html field is False by default
        """
        recipe = self.make_recipe_no_default()

        self.assertFalse(
            recipe.preparation_step_is_html,
            msg="Recipe preparation_steps_is_html is not False",
        )

    def test_recipe_is_published_false_by_default(self):
        """
        Test if the is_published field is False by default
        """
        recipe = self.make_recipe_no_default()

        self.assertFalse(recipe.is_published, msg="Recipe is_published is not False")

    def test_recipe_string_representation(self):
        """
        Testing __str__ method of recipe model.
        """
        self.recipe.title = "Testing Representation String"
        self.recipe.full_clean()
        self.recipe.save()

        self.assertEqual(
            str(self.recipe),
            "Testing Representation String",
            msg="Recipe string representation must be recipe title",
        )

    def test_recipe__category_string_representation_is_name_field(self):
        """
        Testing __str__ method of category model.
        """
        category = self.make_recipe_category(
            name="Testing Representation String Category"
        )

        self.assertEqual(
            str(category),
            "Testing Representation String Category",
            msg="Category string representation must be category name.",
        )

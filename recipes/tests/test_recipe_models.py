from django.core.exceptions import ValidationError

from .recipe_base_test import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_raises_error_if_bigger_than_field_max_length(self):
        """
        This test make the validation of recipe title max length raising a Validation Error
        """
        self.recipe.title = 'A'*70

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()  # validação acontece aqui e o código para

    # def test_recipe_description_raises_error_if_bigger_than_field_max_length(self):
    #     """
    #     This test make the validation of recipe title max length raising a Validation Error
    #     """
    #     self.recipe.description = 'A'*166
    #     self.recipe.full_clean()
    #     self.fail()

        # with self.assertRaises(ValidationError):

    def test_recipe_fields_max_length(self):
        fields = [
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 10),
            ('servings_unit', 10),
        ]
        for field, max_length in fields:
            # set object, campo que quer setar, valor
            with self.subTest(field=field, max_length=max_length):
                setattr(self.recipe, field, 'A' * (max_length + 0))
                with self.assertRaises(ValidationError):
                    self.recipe.full_clean()

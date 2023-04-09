from django import forms
from collections import defaultdict
from recipes.models import Recipe
from recipes.utils.strings import is_positive_number
from django.core.exceptions import ValidationError


class AuthorCreateRecipeValidator:
    def __init__(self, data, errors=None, error_class=None):

        self.errors = defaultdict(list) if errors is None else errors
        self.error_class = ValidationError if error_class is None else error_class
        self.data = data
        self.clean()

        model = Recipe
        fields = 'title','description','preparation_time','preperation_time_unit', 'servings', 'servings_unit','category', 'slug','preparation_step', 'cover'
        widgets = {
            'cover': forms.FileInput(
                attrs = {
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices = (
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Fatias', 'Fatias'),
                )
            ),
            'preperation_time_unit': forms.Select(
                choices = (
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
        }

    def clean(self, *args, **kwargs):
        self.clean_title()
        self.clean_servings()
        self.clean_preparation_time()

        super_clean = super().clean(*args, **kwargs)

        cleaned_data = self.data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')


        if title == description:
            self.errors['title'].append('Cannot be equal to description.')
            self.errors['description'].append('Cannot be equal to title.')


        if self.errors:
            raise self.error_class(self.errors)

        return super_clean


    def clean_title(self):
        title = self.data.get('title')

        if len(title) < 5:
            self.errors['title'].append('Title must have at least 5 chars.')

        return title

    def clean_preparation_time(self):
        field_value = self.data.get('preparation_time')

        if not is_positive_number(field_value):
            self.errors['preparation_time'].append('This field must be a positive number')

        return field_value


    def clean_servings(self):
        field_value = self.data.get('servings')

        if not is_positive_number(field_value):
            self.errors['servings'].append('This field must be a positive number')

        return field_value

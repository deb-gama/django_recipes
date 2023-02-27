from django import forms
from collections import defaultdict
from recipes.models import Recipe
from recipes.utils.django_forms import add_attr
from recipes.utils.strings import is_positive_number
from django.core.exceptions import ValidationError


class AuthorCreateRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._recipe_create_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_step'), 'class', 'span-2')
        add_attr(self.fields.get('cover'), 'class', 'span-2')

    class Meta:
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
        super_clean = super().clean(*args, **kwargs)

        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')


        if title == description:
            self._recipe_create_errors['title'].append('Cannot be equal to description.')
            self._recipe_create_errors['description'].append('Cannot be equal to title.')


        if self._recipe_create_errors:
            raise ValidationError(self._recipe_create_errors)

        return super_clean


    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._recipe_create_errors['title'].append('Title must have at least 5 chars.')

        return title

    def clean_preparation_time(self):
        field_value = self.cleaned_data.get('preparation_time')

        if not is_positive_number(field_value):
            self._recipe_create_errors['preparation_time'].append('This field must be a positive number')

        return field_value


    def clean_servings(self):
        field_value = self.cleaned_data.get('servings')

        if not is_positive_number(field_value):
            self._recipe_create_errors['servings'].append('This field must be a positive number')

        return field_value

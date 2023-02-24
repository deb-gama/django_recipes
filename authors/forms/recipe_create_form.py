from django import forms
from recipes.models import Recipe
from recipes.utils.django_forms import add_attr

class AuthorCreateRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
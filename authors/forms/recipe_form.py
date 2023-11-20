from django import forms
from recipes.models import Recipe
from recipes.utils.django_forms import add_attr


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Recipe
        fields = (
            "title",
            "description",
            "preparation_time",
            "preperation_time_unit",
            "servings",
            "servings_unit",
            "preparation_step",
            "cover",
        )
        widgets = {
            "servings_unit": forms.Select(
                choices=(
                    ("Porções", "Porções"),
                    ("Pedaços", "Pedaços"),
                    ("Fatias", "Fatias"),
                )
            ),
            "preperation_time_unit": forms.Select(
                choices=(
                    ("Minutos", "Minutos"),
                    ("Horas", "Horas"),
                )
            ),
        }

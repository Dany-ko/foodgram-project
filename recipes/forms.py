from django import forms
from django.forms import inlineformset_factory

from recipes.models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = (
            'title', 'time_cooking', 'text',
            'image', 'tags',
        )
        labels = {
            'title': 'Название',
            'text': 'Текст',
            'ingredient': 'Ингредиенты',
            'time_cooking': 'Время приготовления',
            'tags': 'Теги',
        }
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

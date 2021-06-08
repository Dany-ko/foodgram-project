from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('title', 'unit',)

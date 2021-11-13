from rest_framework import serializers

from .models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')

    def get_image_url(self, obj):
        return obj.image.url

    class Meta:
        fields = ('__all__', 'image_url')
        model = Recipe


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = IngredientInRecipe

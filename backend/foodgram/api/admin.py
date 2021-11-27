from django.contrib import admin

from .models import Tag, Ingredient, Recipe, IngredientInRecipe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id',  'author',
                    #'is_favorited', 'is_in_shopping_cart',
                    'name', 'image', 'text', 'cooking_time')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id","recipe_id","ingredient_id", "amount")
    search_fields = ('name',)
    empty_value_display = '-пусто-'
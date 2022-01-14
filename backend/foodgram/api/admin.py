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
    list_filter = ('name', 'measurement_unit',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author',
                    'name', 'image', 'text', 'cooking_time')
    search_fields = ('author', 'name', 'tags')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    def save_model(self, request, obj, form, change):
        image_name, image_format = str(obj.image).split(".")
        obj.image.name = str(obj.name) + "." + image_format
        return super().save_model(request, obj, form, change)


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'recipe', 'ingredient', 'amount')
    search_fields = ('name',)
    empty_value_display = '-пусто-'

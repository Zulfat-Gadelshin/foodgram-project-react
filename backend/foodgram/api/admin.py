from django.contrib import admin

from .models import Tag, Ingredient


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id","name","measurement_unit")
    search_fields = ('name',)
    empty_value_display = '-пусто-'

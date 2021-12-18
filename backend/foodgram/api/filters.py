import django_filters
from django.contrib.auth import get_user_model
from .models import Ingredient, Recipe

User = get_user_model()


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ['name', ]


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(field_name='tags__slug', lookup_expr='exact')

    class Meta:
        model = Recipe
        fields = ['author', 'tags', ]
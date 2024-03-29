import django_filters
from django.contrib.auth import get_user_model

from .models import Ingredient, Recipe, Tag

User = get_user_model()


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name',
                                     lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ['name', ]


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )
    is_favorited = django_filters.BooleanFilter(method="get_is_favorited")

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value is True:
            return queryset.filter(
                id__in=self.request.user.cards_recipes.all())
        elif value is False:
            return queryset.exclude(
                id__in=self.request.user.cards_recipes.all())
        else:
            return queryset

    def get_is_favorited(self, queryset, name, value):
        if value is True:
            return queryset.filter(
                id__in=self.request.user.favorite_recipes.all())
        elif value is False:
            return queryset.exclude(
                id__in=self.request.user.favorite_recipes.all())
        else:
            return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_in_shopping_cart', 'is_favorited']

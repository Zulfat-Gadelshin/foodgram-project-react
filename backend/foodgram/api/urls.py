from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('tags', views.TagViewSet, basename='tags')
router.register(
    'ingredients',
    views.IngredientViewSet,
    basename='ingredients')
router.register('recipes', views.RecipeViewSet, basename='recipes')
router.register('recipes/(?P<recipe_id>[0-9]+)/favorite',
                views.FavoriteViewSet, basename='favorite')
router.register('recipes/(?P<recipe_id>[0-9]+)/shopping_cart',
                views.ShoppingCartViewSet, basename='shopping_cart')

urlpatterns = [

    path('', include(router.urls)),
]

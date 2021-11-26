from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('tags/', views.TagViewSet, basename='tags')
router.register(
    'ingredients/',
    views.IngredientViewSet,
    basename='ingredients')
router.register('recipes/', views.RecipeViewSet, basename='recipes')

"""router.register(
    r'recipes/(?P<recipes_id>[0-9]+)/shopping_cart',
    views.Shopping_cartViewSet, 'shopping_cart')
router.register(
    r'recipes/(?P<recipes_id>[0-9]+)/favorite',
    views.FavoriteViewSet, 'favorite')
router.register(
    'users/subscriptions',
    views.SubscriptionsViewSet,
    basename='subscriptions')
router.register(
    r'users/(?P<user_id>[0-9]+)/subscribe',
    views.SubscribeViewSet, 'subscribe')
router.register(
    'ingredients',
    views.IngredientsViewSet,
    basename='ingredients')
"""

urlpatterns = [
    path('', include(router.urls)),
]
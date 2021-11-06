from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('auth/email', views.AuthEmailViewSet, basename='email')
router.register('auth/token', views.AuthTokenViewSet, basename='token')
router.register('users', views.UserViewSet, basename='user')
router.register('users/<int:id>',viewset= )#, views.UserViewSet, basename='user_id')
router.register('tags', views.TagsViewSet, basename='tags')
router.register('recipes', views.RecipesViewSet, basename='recipes')
router.register(
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

# router.register(
#     r'titles/(?P<title_id>[0-9]+)/reviews',
#     views.ReviewViewSet, 'Reviews')

urlpatterns = [
    path('', include(router.urls)),
]
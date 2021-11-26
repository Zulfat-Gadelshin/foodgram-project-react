from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.views import TokenCreateView, TokenDestroyView


from . import views

router = DefaultRouter()

router.register('users/(?P<user_id>[0-9]+)/subscribe', views.SubscribeViewSet, basename='subscribe')
router.register('users', views.UserViewSet, basename='user')



urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
    ]

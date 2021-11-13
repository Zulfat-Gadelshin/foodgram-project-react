from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
#router.register('auth/email', views.AuthEmailViewSet, basename='email')
#router.register('auth/token', views.AuthTokenViewSet, basename='token')
router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token', include('djoser.urls.jwt')),
    ]

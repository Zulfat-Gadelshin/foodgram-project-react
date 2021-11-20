from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.views import TokenCreateView, TokenDestroyView


from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/token/login/', views.AuthTokenViewSet, name="login"),
    path('auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
    #path('auth/token/', views_for_token.TokenRefreshView.as_view(), name="jwt-refresh"),
    #path(r"^jwt/verify/?", views_for_token.TokenVerifyView.as_view(), name="jwt-verify"),
    ]

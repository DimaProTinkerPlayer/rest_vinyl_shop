from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CurrentUserAPIView, RegisterAPIView

urlpatterns = [
    path("auth/register", RegisterAPIView.as_view(), name="auth-register"),
    path("auth/login", TokenObtainPairView.as_view(), name="auth-login"),
    path("auth/refresh", TokenRefreshView.as_view(), name="auth-refresh"),
    path("auth/me", CurrentUserAPIView.as_view(), name="auth-me"),
]
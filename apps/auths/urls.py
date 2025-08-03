from django.urls import path
from apps.auths import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('signup/', views.UserSignupAPIView.as_view(), name='auth-signup'),
    path('login/', TokenObtainPairView.as_view(), name='auth-login'),
    path('logout/', views.UserLogoutAPIView.as_view(), name='auth-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh')
]

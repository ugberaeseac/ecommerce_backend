from django.urls import path, include
from apps.users import views



urlpatterns = [
    path('', views.UserListCreateAPIView.as_view(), name='user-list'),
    path('me/', views.UserMeAPIView.as_view(), name='user-me'),
    path('<uuid:user_id>/', views.UserDetailAPIView.as_view(), name='user-detail'),
]
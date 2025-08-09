from django.urls import path
from apps.orders import views



urlpatterns = [
    path('', views.OrderListAPIView.as_view(), name='order-list'),
    path('my-orders/', views.MyOrderAPIView.as_view(), name='order-me'),
    path('<uuid:order_id>/', views.OrderDetailAPIView.as_view(), name='order-detail'),
    path('<uuid:order_id>/status/', views.OrderStatusAPIView.as_view(), name='order-status'),
]
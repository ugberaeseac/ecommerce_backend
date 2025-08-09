from django.urls import path
from apps.orders import views



urlpatterns = [
    #path('', views.CartListCreateAPIView.as_view(), name='cart-list'),
    path('my-cart/', views.MyCartAPIView.as_view(), name='cart-me'),
    path('<uuid:cart_id>/', views.CartDetailAPIView.as_view(), name='cart-detail'),

    path('items/', views.CartItemListCreateAPIView.as_view(), name='cart_item-list'),
    path('items/<uuid:item_id>/', views.CartItemDetailAPIView.as_view(), name='cart_item-detail'),
    path('checkout/', views.CartCheckoutAPIView.as_view(), name='cart-checkout'),
]
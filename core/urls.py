from django.urls import path, include
from apps.products import views



urlpatterns = [
    path('auth/', include('apps.auths.urls')),
    path('users/', include('apps.users.urls')),
    path('products/', views.ProductListCreateAPIView.as_view(), name='product-list'),
    path('products/<slug:slug>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
    path('categories/', views.CategoryListCreateAPIView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', views.CategoryDetailAPIView.as_view(), name='category-detail'),
    path('categories/<slug:slug>/products/', views.CategoryProductListAPIView.as_view(), name='category-product-list'),
]

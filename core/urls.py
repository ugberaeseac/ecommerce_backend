from django.urls import path, include



urlpatterns = [
    path('auth/', include('apps.auths.urls')),
    path('users/', include('apps.users.urls')),

]

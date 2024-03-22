from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users, name='members'),
    path('users/normal/', views.normal, name='members'),
    path('users/caching/', views.caching, name='members'),
    path('users/sharding/', views.sharding, name='members'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users, name='Users'),
    path('users/normal/', views.normal.as_view(), name='normal'),
    path('users/normal/<int:pk>', views.normal.as_view(), name='normalpk'),
    path('users/caching/', views.caching.as_view(), name='caching'),
    path('users/caching/<int:pk>', views.caching.as_view(), name='cachingpk'),
    path('users/sharding/', views.sharding.as_view(), name='sharding'),
]
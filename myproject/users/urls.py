from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users, name='Users'),
    path('users/normal/', views.normal.as_view(), name='normal'),
    path('users/normal/<int:pk>', views.normal.as_view(), name='normalPk'),
    path('users/caching/', views.caching.as_view(), name='caching'),
    path('users/caching/<int:pk>', views.caching.as_view(), name='cachingPk'),
    path('users/sharding/normal/', views.sharding.normal.as_view(), name='shardingNormal'),
    path('users/sharding/normal/<int:pk>', views.sharding.normal.as_view(), name='shardingNormalPk'),
    path('users/sharding/caching/', views.sharding.caching.as_view(), name='shardingCaching'),
    path('users/sharding/caching/<int:pk>', views.sharding.caching.as_view(), name='shardingCachingPk'),
]
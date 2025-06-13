from django.urls import path
from .views import (
    home,
    user_list,
    user_detail,
    userdetails_list,
    userdetails_detail,
)

urlpatterns = [
    path('', home, name='home'),

    # User APIs
    path('api/users/', user_list, name='user-list'),
    path('api/users/<int:pk>/', user_detail, name='user-detail'),

    # UserDetails APIs
    path('api/user-details/', userdetails_list, name='userdetails-list'),
    path('api/user-details/<int:pk>/', userdetails_detail, name='userdetails-detail'),
]

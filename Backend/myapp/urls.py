from django.urls import path
from .views import (
    home,
    user_create_api,
    user_list_api,
    userdetails_create_api,
    userdetails_list_api,
    userdetails_get_api,
)

urlpatterns = [
    path('', home, name='home'),

    # API endpoints
    path('api/user/create/', user_create_api, name='user-create'),
    path('api/users/', user_list_api, name='user-list'),
    path('api/user-details/create/', userdetails_create_api, name='userdetails-create'),
    path('api/user-details/', userdetails_list_api, name='userdetails-list'),
    path('api/user-details/<int:user_id>/', userdetails_get_api, name='userdetails-get'),

]

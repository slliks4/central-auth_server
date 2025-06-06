from django.urls import path
from .views import home_page, end_points
from system_auth.views.user import create_user

urlpatterns = [
    path('', home_page, name='index'),
    path('api/', end_points, name='end-points'),
    path('create-user/', create_user, name='create-users'),
]
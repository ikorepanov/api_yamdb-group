from django.urls import include, path
from rest_framework import routers

from .views import create_new_user


name_app = 'users'


router = routers.DefaultRouter()

urlpatterns = [
    path('auth/signup/', create_new_user)
]
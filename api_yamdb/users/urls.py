from django.urls import path, include
from rest_framework import routers

from .views import (
    create_new_user,
    create_token_for_user,
    UserViewSet
)


name_app = 'users'


router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('api/v1/auth/signup/', create_new_user),
    path('api/v1/auth/token/', create_token_for_user),
    path('api/v1/', include(router.urls)),
]

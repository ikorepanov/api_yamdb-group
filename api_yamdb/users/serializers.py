from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор для Users'''
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class CreateNewUserSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания нового пользователя'''
    class Meta:
        model = User
        fields = (
            'username',
            'email'
        )


class CreateTokenForUserSerializer(serializers.ModelSerializer):
    '''Сериализатор для получения token'''
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

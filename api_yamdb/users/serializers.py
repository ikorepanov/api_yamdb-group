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


class CreateNewUserSerializer(serializers.Serializer):
    '''Сериализатор для создания нового пользователя'''
    email = serializers.EmailField()
    username = serializers.CharField(max_length=250)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if (
            User.objects.filter(username=username).exists()
            and User.objects.get(username=username).email != email
        ):
            raise serializers.ValidationError(
                f'Пользователь {username} существует с другой почтой.'
            )
        if (
            User.objects.filter(email=email).exists()
            and User.objects.get(email=email).username != username
        ):
            raise serializers.ValidationError(
                f'Почта {email} принадлежит другому пользователю.'
            )
        return data

class CreateTokenForUserSerializer(serializers.Serializer):
    '''Сериализатор для получения token'''
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

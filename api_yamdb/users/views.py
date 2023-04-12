from django.shortcuts import render, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import CreateNewUserSerializer


@api_view(['POST'])
def create_new_user(request):
    '''Создание нового пользователя'''
    serializer = CreateNewUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    if any((
        User.objects.filter(username=username).exists(),
        User.objects.filter(email=email).exists()
    )):
        return Response(
            {f'Пользователь {username} или {email} уже используются.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        User.objects.create(username=username, email=email)
    user = get_object_or_404(User, email=email)
    confirmation_code = default_token_generator.make_token(user)
    message = f'Код подтверждения: {confirmation_code}'
    mail_subject = 'Код подтверждения на YaMDb'
    send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )

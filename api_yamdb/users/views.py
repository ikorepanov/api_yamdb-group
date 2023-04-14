import datetime

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets


from .models import User
from .serializers import CreateNewUserSerializer, CreateTokenForUserSerializer, UserSerializer
from .permissions import IsAdminOrSuperUser


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_new_user(request):
    '''Создание нового пользователя'''
    serializer = CreateNewUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    confirmation_code = datetime.datetime.now().timestamp()
    User.objects.get_or_create(
        **serializer.validated_data
    )
    User.objects.filter(
        username=username,
        email=email).update(confirmation_code=confirmation_code)
    message = (f'Добрый день, пользователь {username}.\n\n'
               f'Вы зарегистрировались в учебном проекте 86 группы.\n'
               f'Код подтверждение email: {confirmation_code}\n')
    mail_subject = 'Wellcome to YaMDb by 86 group'
    send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_token_for_user(request):
    '''Создаем токен для пользователя'''
    serializer = CreateTokenForUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if confirmation_code != user.confirmation_code:
        return Response(
            {'confirmation_code': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )
    token = AccessToken.for_user(user)
    message = (
        f'Добрый день, {username}.\n'
        f'Ваш token для настройки API: {str(token)}\n'
    )
    mail_subject = 'API token'
    send_mail(
        mail_subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    return Response(
        {"token": str(token)},
        status=status.HTTP_200_OK
    )


class UserViewSet(viewsets.ModelViewSet):
    '''Вьюсет для пользователей'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperUser]
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated],
        url_path='me'
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

import random
import string

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets, filters
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitleWriteSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    CreateNewUserSerializer,
    CreateTokenForUserSerializer,
    UserSerializer
)
from reviews.pagination import CommentsPagination, ReviewsPagination
from reviews.models import User, Comment, Review, Title, Category, Genre
from reviews.permissions import IsSuperUserIsAdminIsModeratorIsAuthor
from .mixins import CreateListDestroyViewSet
from .permissions import IsAdminOrReadOnly, IsAdminOrSuperUser
from .filters import TitleFilter


def create_confirm_code():
    '''Создание кода подтвердления'''
    confirm_code = string.ascii_uppercase + string.digits
    return (
        ''.join(random.choices(confirm_code, k=5))
        + '-'
        + ''.join(random.choices(confirm_code, k=5))
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_new_user(request):
    '''Создание нового пользователя'''
    serializer = CreateNewUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    confirmation_code = create_confirm_code()
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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

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


class AllReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения из БД обьектов класса Review."""
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса Review."""
    serializer_class = ReviewSerializer
    pagination_class = ReviewsPagination
    permission_classes = [IsSuperUserIsAdminIsModeratorIsAuthor]

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class AllCommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения из БД обьектов класса Comment."""
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса Comment."""
    serializer_class = CommentSerializer
    pagination_class = CommentsPagination
    permission_classes = [IsSuperUserIsAdminIsModeratorIsAuthor]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review_obj = get_object_or_404(Review, pk=review_id, title=title_id)
        return Comment.objects.filter(review=review_obj)

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def perform_create(self, serializer):
        review = self.get_review()
        title = self.get_title()
        if title != review.title:
            raise NotFound()
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для создания обьектов класса Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для создания обьектов класса Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса Title."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleWriteSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer

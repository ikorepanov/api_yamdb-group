from api.views import (
    TitleViewSet,
    ReviewViewSet,
    AllCommentViewSet,
    CommentViewSet,
    AllReviewViewSet,
    GenreViewSet,
    CategoryViewSet
)
from .views import (
    create_new_user,
    create_token_for_user,
    UserViewSet
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'reviews', AllReviewViewSet, basename='all_reviews')
router_v1.register(r'comments', AllCommentViewSet, basename='all_comments')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'titles', TitleViewSet, basename='title')

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path('v1/auth/signup/', create_new_user),
    path('v1/auth/token/', create_token_for_user),
]

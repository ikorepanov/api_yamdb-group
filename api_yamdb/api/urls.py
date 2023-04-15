from api.views import TitleViewSet, ReviewViewSet, AllCommentViewSet, CommentViewSet, AllReviewViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register(r'v1/titles', TitleViewSet)
router.register(r'v1/reviews', AllReviewViewSet, basename='all_reviews')
router.register(r'v1/comments', AllCommentViewSet, basename='all_comments')

router.register(r'v1/titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]

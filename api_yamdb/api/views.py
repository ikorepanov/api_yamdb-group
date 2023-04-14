from reviews.models import Title, Review, Comment
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .serializers import TitleSerializer, ReviewSerializer, CommentSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class AllReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        title = self.get_title()
        reviews = title.reviews.all()
        return reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # @api_view(['POST'])
    # def create_review(self, request):
    #     try:
    #         title = self.get_title()
    #     except Title.DoesNotExist:
    #         return Response({'error': 'Title not found'}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = ReviewSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(title=title)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        review = self.get_review()
        comments = review.comments.all()
        return comments

    # def get_queryset(self):
    #     title_id = self.kwargs.get('title_id')
    #     review_id = self.kwargs.get('review_id')
    #     return Comment.objects.filter(review__id=review_id, review__title__id=title_id)

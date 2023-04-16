from rest_framework import serializers
from reviews.models import Title, Review, Comment


class TitleSerializer(serializers.ModelSerializer):
    reviews = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        # fields = ('id', 'name', 'year', 'category', 'reviews')
        model = Title


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        # fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    # comments = serializers.StringRelatedField(many=True, read_only=True)
    # comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        # fields = ('id', 'text', 'author', 'score', 'pub_date', 'comments')
        model = Review

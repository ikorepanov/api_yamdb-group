from django.contrib import admin
from .models import Title, Review, Comment


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'category',
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title_id',
        'text',
        'author',
        'score',
        'pub_date',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'review_id',
        'text',
        'author',
        'pub_date',
    )


admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
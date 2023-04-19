from django.urls import path
from loaders.views import (
    load_titles_view,
    load_reviews_view,
    load_users_view,
    load_comments_view
)

app_name = 'loaders'

urlpatterns = [
    path('load_titles/', load_titles_view, name='load_titles_view'),
    path('load_reviews/', load_reviews_view, name='load_titles_view'),
    path('load_users/', load_users_view, name='load_users_view'),
    path('load_comments/', load_comments_view, name='load_comments_view'),
]

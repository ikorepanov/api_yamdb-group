from django.http import HttpResponse
from loaders.load_titles import run_title
from loaders.load_reviews import run_review
from loaders.load_users import run_user
from loaders.load_comments import run_comment


def load_titles_view(request):
    run_title()
    return HttpResponse("Данные в таблицу Title загружены")


def load_reviews_view(request):
    run_review()
    return HttpResponse("Данные в таблицу Review загружены")


def load_users_view(request):
    run_user()
    return HttpResponse("Данные в таблицу User загружены")


def load_comments_view(request):
    run_comment()
    return HttpResponse("Данные в таблицу Comment загружены")
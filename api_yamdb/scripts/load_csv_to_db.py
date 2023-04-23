import csv
from reviews.models import Genre, Category, Title, Review, Comment
from users.models import User


def genre(row):
    genre = Genre(id=row[0], name=row[1], slug=row[2])
    genre.save()


def category(row):
    category = Category(id=row[0], name=row[1], slug=row[2])
    category.save()


def user(row):
    user = User(id=row[0], username=row[1], email=row[2], role=row[3],
                bio=row[4], first_name=row[5], last_name=row[6])
    user.save()


def title(row):
    category = row[3]
    category_instance, created = Category.objects.get_or_create(id=category)
    if created:
        print('В Title добавлен новый объект: ', category_instance)
    title = Title(id=row[0], name=row[1], year=row[2],
                  category=category_instance)
    title.save()


def review(row):
    title = row[1]
    author = row[3]
    title_instance, created = Title.objects.get_or_create(id=title)
    if created:
        print('В Review добавлен новый объект: ', title_instance)
    user_instance, created = User.objects.get_or_create(id=author)
    if created:
        print('В User добавлен новый объект: ', user_instance)
    review = Review(id=row[0], title=title_instance, text=row[2],
                    author=user_instance, score=row[4], pub_date=row[5])
    review.save()


def comments(row):
    review = row[1]
    author = row[3]
    review_instance, created = Review.objects.get_or_create(id=review)
    if created:
        print('В Review добавлен новый объект: ', review_instance)
    user_instance, created = User.objects.get_or_create(id=author)
    if created:
        print('В User добавлен новый объект: ', user_instance)
    comments = Comment(id=row[0], review=review_instance, text=row[2],
                       author=user_instance, pub_date=row[4])
    comments.save()


csv_files = [
    'genre',
    'category',
    'users',
    'titles',
    'review',
    'comments'
]

models = [
    Genre,
    Category,
    User,
    Title,
    Review,
    Comment
]

functions = [
    genre,
    category,
    user,
    title,
    review,
    comments,
]


def run():
    for file, model, func in zip(csv_files, models, functions):
        fhand = open(f'static/data/{file}.csv', encoding="utf-8")
        reader = csv.reader(fhand)
        next(reader)

        model.objects.all().delete()

        for row in reader:
            print(row)
            func(row)

import csv
from reviews.models import Review, Title
from users.models import User


def run_review():
    fhand = open('static/data/review.csv', encoding="utf-8")
    reader = csv.reader(fhand)

    Review.objects.all().delete()

    next(reader)
    for row in reader:
        title = row[1]
        author = row[3]
        title_instance = Title.objects.get(id=title)
        user_instance = User.objects.get(id=author)
        data = Review(
            id=row[0],
            title=title_instance,
            text=row[2],
            author=user_instance,
            score=row[4],
            pub_date=row[5]
        )
        data.save()

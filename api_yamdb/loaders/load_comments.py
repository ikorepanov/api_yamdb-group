import csv
from reviews.models import Review, Comment
from users.models import User


def run_comment():
    fhand = open('static/data/comments.csv', encoding="utf-8")
    reader = csv.reader(fhand)

    Comment.objects.all().delete()

    next(reader)
    for row in reader:
        review = row[1]
        author = row[3]
        review_instance = Review.objects.get(id=review)
        user_instance = User.objects.get(id=author)
        data = Comment(
            id=row[0],
            review=review_instance,
            text=row[2],
            author=user_instance,
            pub_date=row[4]
        )
        data.save()

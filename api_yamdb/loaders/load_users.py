import csv
from users.models import User


def run_user():
    fhand = open('static/data/users.csv', encoding="utf-8")
    reader = csv.reader(fhand)

    # User.objects.all().delete()
    
    next(reader)
    for row in reader:
        print(row)
        data = User(id=row[0], username=row[1], email=row[2], role=row[3], bio=row[4], first_name=row[5], last_name=row[6])
        data.save()

# Generated by Django 3.2 on 2023-04-13 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='user',
            name='unique_username',
        ),
    ]

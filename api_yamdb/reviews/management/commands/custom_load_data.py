import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User

models_file = {
    Category: 'category.csv',
    User: 'users.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Title.genre.through: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    help = 'Загрузка данных.'

    def handle(self, *args, **options):
        for model, file in models_file.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{file}',
                'r',
                encoding='utf-8',
            ) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    model.objects.get_or_create(**row)

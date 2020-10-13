import csv
from api.models import Genre
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('data/genre.csv', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile)
            for id, row in enumerate(spamreader):
                if id == 0:
                    continue
                genre = Genre(id=row[0], name=row[1], slug=row[2])
                genre.save()
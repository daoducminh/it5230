from django.core.management.base import BaseCommand
from django.db import connection

SCHEMA = 'public'
DATA = 'data.json'


class Command(BaseCommand):
    help = 'Resets the database'

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                cursor.execute('DROP SCHEMA {} CASCADE;'.format(SCHEMA))
                cursor.execute('CREATE SCHEMA {} CASCADE;'.format(SCHEMA))
        except Exception as e:
            print(e)

from django.contrib.postgres.search import SearchVector
from django.core.management.base import BaseCommand, CommandError

from foods.models import Recipe, Menu


class Command(BaseCommand):
    help = 'Update recipe average score'

    def handle(self, *args, **options):
        try:
            common_vector = SearchVector('description', weight='C')
            recipe_tsv = SearchVector('recipe_name', weight='A') + common_vector
            Recipe.objects.update(tsv=recipe_tsv)
            menu_tsv = SearchVector('menu_name', weight='A') + common_vector
            Menu.objects.update(tsv=menu_tsv)
        except Exception as e:
            raise CommandError(str(e))

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg

from foods.models import Recipe, Rating


class Command(BaseCommand):
    help = 'Update recipe average score'

    def handle(self, *args, **options):
        recipes = Recipe.objects.all()
        if recipes:
            for d in recipes:
                ratings = Rating.objects.filter(recipe=d)
                if ratings:
                    avg = ratings.aggregate(Avg('score'))
                    d.score = avg['score__avg']
                    d.save()
            self.stdout.write(self.style.SUCCESS('Update recipe score successfully.'))
        else:
            raise CommandError('No public recipe found.')

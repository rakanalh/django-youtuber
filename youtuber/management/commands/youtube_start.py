from django.core.management.base import BaseCommand
from youtuber.tasks import youtuber_start


class Command(BaseCommand):
    def handle(self, *args, **options):
        youtuber_start.delay()

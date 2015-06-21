from django.core.management.base import BaseCommand
from youtuber.models import YoutubeSource
from youtuber.tasks import youtuber_scrape


class Command(BaseCommand):
    def handle(self, *args, **options):
        youtube_sources = YoutubeSource.objects.all()

        for source in youtube_sources:
            youtuber_scrape(source_id=source.id)

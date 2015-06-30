from django.conf import settings
from celery import shared_task
from celery.utils.log import get_task_logger

from youtuber.client import YoutubeApi
from youtuber.exceptions import ClientConfigError
from youtuber.models import YoutubeSource
from youtuber.utils import get_pipeline_instances


try:
    developer_key = settings.YOUTUBE_DEVELOPER_KEY
except AttributeError:
    raise ClientConfigError('YOUTUBE_DEVELOPER_KEY is not defined')

max_results = getattr(settings, 'YOUTUBE_MAX_RESULTS')
follow_pagination = getattr(settings, 'YOUTUBE_FOLLOW_PAGINATION', False)
max_pagination = getattr(settings, 'YOUTUBE_MAX_PAGINATION', 1)

client = YoutubeApi(developer_key)

@shared_task()
def youtuber_start():
    youtube_sources = YoutubeSource.objects.all()

    logger = get_task_logger(__name__)

    for source in youtube_sources:
        logger.info('Processing youtube source %s' % source.name.encode('utf-8'))

        playlist_id = source.identifier
        if source.type == YoutubeSource.TYPE_CHANNEL:
            playlists = client.get_username_playlists(source.identifier)

            if 'uploads' in playlists:
                playlist_id = playlists['uploads']
            else:
                logger.info('No uploads channel found')
                return

        youtuber_scrape.delay(source_id=source.id, playlist_id=playlist_id)


@shared_task()
def youtuber_scrape(source_id, playlist_id, page_token=None):
    logger = get_task_logger(__name__)

    pipeline_instances = get_pipeline_instances()
    logger.info('Got %d pipelines' % len(pipeline_instances))

    youtube_source = YoutubeSource.objects.get(pk=source_id)

    for _ in range(max_pagination):
        videos = client.get_videos_from_playlist(playlist_id, page_token, max_results)

        if not videos:
            break

        logger.info('Extracted %d videos' % len(videos.items))

        for video in videos.items:
            for instance in pipeline_instances:
                logger.info('Calling %s pipeline for video %s' % (instance.__class__, video.title))
                instance.process(youtube_source, video)

        if not follow_pagination or not videos.next_page_token:
            break

        page_token = videos.next_page_token

    return

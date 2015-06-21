from celery import shared_task
from celery.utils.log import get_task_logger

from youtuber.client import YoutubeApi
from youtuber.models import YoutubeSource
from youtuber.utils import get_pipeline_instances


@shared_task()
def youtuber_start():
    youtube_sources = YoutubeSource.objects.all()

    logger = get_task_logger(__name__)

    for source in youtube_sources:
        logger.info('Processing youtube source %s' % source.name.encode('utf-8'))
        youtuber_scrape.delay(source_id=source.id)


@shared_task()
def youtuber_scrape(source_id):
    client = YoutubeApi()
    logger = get_task_logger(__name__)

    pipeline_instances = get_pipeline_instances()
    logger.info('Got %d pipelines' % len(pipeline_instances))

    youtube_source = YoutubeSource.objects.get(pk=source_id)

    if youtube_source.type == YoutubeSource.TYPE_CHANNEL:
        videos = client.get_videos_by_username(youtube_source.identifier)
    else:
        videos = client.get_videos_from_playlist(youtube_source.identifier)

    logger.info('Extracted %d videos' % len(videos))

    for video in videos:
        for instance in pipeline_instances:
            logger.info('Calling %s pipeline for video %s' % (instance.__class__, video['snippet']['title']))
            instance.process(youtube_source, video)

    return

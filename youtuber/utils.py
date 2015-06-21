from django.conf import settings
from youtuber.exceptions import NoPipelinesError
from youtuber.pipelines import BasePipeline


def get_pipeline_instances():
    try:
        pipeline_classes = settings.YOUTUBE_ENTRY_PIPELINES
    except AttributeError:
        raise NoPipelinesError('No pipelines are configured')

    pipeline_instances = []
    for pipeline_class in pipeline_classes:
        components = pipeline_class.split('.')
        module_name = '.'.join(components[:-1])
        class_name = components[-1]

        module = __import__(module_name, fromlist=[class_name])
        class_ = getattr(module, class_name)
        instance = class_()
        if isinstance(instance, BasePipeline):
            pipeline_instances.append(instance)
    return pipeline_instances

class BasePipeline(object):
    def process(self, youtube_source, video):
        raise NotImplementedError()

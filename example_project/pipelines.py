from youtuber.pipelines import BasePipeline


class YoutubePipeline(BasePipeline):
    def process(self, youtube_source, video):
        print video.title

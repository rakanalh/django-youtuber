Django Youtuber
===============

A tiny app that goes through the list of channels/playlists from youtube.
This app enables you to add as many entries as you need through the admin panel and it will scrape the video data you 
need from youtube.

How to use
----------
Simply add the following configuration values to your settings.py file:

    YOUTUBE_DEVELOPER_KEY = '<YOUR_APP_ID>'
    YOUTUBE_MAX_RESULTS = 10 # default is 10
    YOUTUBE_FOLLOW_PAGINATION = True # Default is false
    YOUTUBE_MAX_PAGINATION = 10 # default is 10
    YOUTUBE_ENTRY_PIPELINES = [
        'example_project.pipelines.YoutubePipeline'
    ]

As you've noticed, This app does not provide a model/table that saves the video info for you. Instead, you have to
write your own pipeline (Inspired by scrapy) to save the data manually.

Pipeline looks as follows:

    from youtuber.pipelines import BasePipeline
    
    
    class YoutubePipeline(BasePipeline):
        def process(self, youtube_source, video):
            print video.title

You can pretty much do whatever you like in the pipeline with the video instance.

The youtube_source instance is a [YoutubeSource](django-youtuber/tree/master/youtuber/models.py) instance provided by 
django_youtuber to identify where the video came from. The video instance is a [YoutubeFeedItem](django-youtuber/tree/master/youtuber/client.py)
that contains the list of attributes extracted for a single youtube video.

License
-------

The MIT License (MIT)

Copyright (c) 2015 Rakan Alhneiti

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
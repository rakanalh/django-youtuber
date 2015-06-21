import requests
from django.conf import settings
from youtuber.exceptions import ClientConfigError


class YoutubeApi(object):
    youtube_api_url = 'https://www.googleapis.com/youtube/v3'

    def __init__(self):
        try:
            self.developer_key = settings.YOUTUBE_DEVELOPER_KEY
        except AttributeError:
            raise ClientConfigError('YOUTUBE_DEVELOPER_KEY is not defined')

    def get_videos_by_username(self, username):
        parameters = {
            'forUsername': username,
            'part': 'contentDetails'
        }
        uri = 'channels'
        content = self._fetch_content(uri, parameters)

        videos = []

        for item in content['items']:
            playlist_id = item['contentDetails']['relatedPlaylists']['uploads']
            videos.extend(self.get_videos_from_playlist(playlist_id))

        return videos

    def get_videos_from_playlist(self, playlist_id):
        parameters = {
            'part': 'snippet',
            'playlistId': playlist_id
        }
        uri = 'playlistItems'
        content = self._fetch_content(uri, parameters)

        return content['items']

    def _fetch_content(self, uri, parameters):
        parameters['key'] = self.developer_key
        response = requests.get('%s/%s' % (self.youtube_api_url, uri), parameters)
        if response.status_code == 200:
            return response.json()
        else:
            print response.content

        return None

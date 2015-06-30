import requests
from django.conf import settings
from youtuber.exceptions import PlaylistException, ChannelNotFoundException, ClientConfigError


class YoutubeApi(object):
    youtube_api_url = 'https://www.googleapis.com/youtube/v3'

    def __init__(self, developer_key):
        self.developer_key = developer_key

        self.follow_pagination = getattr(settings, 'YOUTUBE_FOLLOW_PAGINATION', False)
        self.max_results = getattr(settings, 'YOUTUBE_MAX_RESULTS', 10)

    def get_username_playlists(self, username):
        parameters = {
            'forUsername': username,
            'part': 'contentDetails'
        }
        uri = 'channels'
        content = self._fetch_content(uri, parameters)

        if 'error' in content:
            raise ClientConfigError(content['error']['message'])

        if content['pageInfo']['totalResults'] == 0:
            raise ChannelNotFoundException()

        if content['items'][0] and content['items'][0]['contentDetails']['relatedPlaylists']:
            return content['items'][0]['contentDetails']['relatedPlaylists']

        return {}

    def get_videos_from_playlist(self, playlist_id, page_token=None, max_results=10):
        parameters = {
            'part': 'snippet',
            'playlistId': playlist_id
        }

        if page_token:
            parameters['pageToken'] = page_token

        if max_results > 0:
            parameters['maxResults'] = max_results
        uri = 'playlistItems'
        response = self._fetch_content(uri, parameters)
        if not response:
            return None

        if 'error' in response:
            raise PlaylistException(response['error']['errors'][0]['message'])

        content = YoutubeFeedResult(response)

        return content

    def _fetch_content(self, uri, parameters):
        parameters['key'] = self.developer_key
        parameters['maxResults'] = self.max_results

        # Retry connections
        for _ in range(3):
            try:
                response = requests.get('%s/%s' % (self.youtube_api_url, uri), parameters)
                return response.json()
            except requests.exceptions.ConnectionError:
                pass
        return None


class YoutubeFeedResult(object):
    def __init__(self, response):
        if 'nextPageToken' in response:
            self.next_page_token = response['nextPageToken']
        else:
            self.next_page_token = None

        if 'prevPageToken' in response:
            self.prev_page_token = response['prevPageToken']
        else:
            self.prev_page_token = None

        if 'pageInfo' in response:
            self.total_results = response['pageInfo']['totalResults']
            self.results_per_page = response['pageInfo']['resultsPerPage']

        self.items = []
        for item in response['items']:
            self.items.append(YoutubeFeedItem(item['snippet']))


class YoutubeFeedItem(object):
    def __init__(self, item):
        self.title = item['title']
        self.description = item['description']
        self.channel_id = item['channelId']
        self.channel_title = item['channelTitle']
        self.playlist_id = item['playlistId']
        self.position = item['position']
        self.published_at = item['publishedAt']
        self.video_id = item['resourceId']['videoId']
        self.images = {}
        if 'thumbnails' in item:
            self.images.update(item['thumbnails'])

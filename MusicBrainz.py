import requests


class MusicBrainz:
    def __init__(self):
        self.default_headers = {
            'Content-Type': 'application/json'
        }

    def get_spotify_id(self, musicbrainz_id):
        artist_url = f'http://musicbrainz.org/ws/2/artist/{musicbrainz_id}?inc=url-rels&fmt=json'
        response = requests.get(artist_url, headers=self.default_headers).json()
        for item in response.get('relations'):
            if 'spotify' in item['url']['resource']:
                return item['url']['resource'].split('/')[-1]
        return None

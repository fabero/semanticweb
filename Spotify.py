import requests
from base64 import b64encode as _b64encode
import os

CLIENT_ID = 'acbabb4dfeb642f090a34cce20cfabc1'
CLIENT_SECRET = '9cbb51fba6d84ebc860694051a5336d8'


class Spotify:
    """Interacts with the Spotify API"""

    def __init__(self):
        if os.path.exists('token'):
            f = open('token', 'r')
            token = f.readline()
            if self.is_token_expired(token):
                f.close()
                token = self.get_token()
        else:
            token = self.get_token()

        self.default_headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def get_token(self):
        token_url = 'https://accounts.spotify.com/api/token'
        auth = b64encode(CLIENT_ID + ':' + CLIENT_SECRET)
        headers = {"Authorization": f'Basic {auth}'}
        data = {'grant_type': 'client_credentials'}

        response = requests.post(token_url, data=data, headers=headers).json()
        token = response['access_token']

        with open('token', 'w') as f:
            f.write(token)

        return token

    def is_token_expired(self, token):
        test_url = 'https://api.spotify.com/v1/artists/'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(test_url, headers=headers).json()

        if response.get('error') and response.get('error').get('status') == 401:
            return True
        else:
            return False

    def get_artist(self, artist_id):
        artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'
        response = requests.get(
            artist_url, headers=self.default_headers).json()
        return response

    def get_artist_albums(self, artist_id):
        albums_url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
        response = requests.get(
            albums_url, headers=self.default_headers).json().get('items')
        if response is not None:
            album_titles = list(set([album['name'] for album in response]))
            return album_titles
        return None

    def get_top_tracks(self, artist_id):
        tracks_url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=NL'
        response = requests.get(
            tracks_url, headers=self.default_headers).json().get('tracks')
        if response is not None:
            tracks = [[track['name'], track['id'],
                       track['external_urls']['spotify']] for track in response]
            return tracks
        return None

    def get_related_artists(self, artist_id):
        artists_url = f'https://api.spotify.com/v1/artists/{artist_id}/related-artists'
        response = requests.get(
            artists_url, headers=self.default_headers).json().get('artists')
        if response is not None:
            artist_names = list(set([artist['name'] for artist in response]))
            return artist_names
        return None

    def get_artist_features(self, track_ids):
        id_list = ','.join(track_ids)
        features_url = f'https://api.spotify.com/v1/audio-features/?ids={id_list}'
        response = requests.get(
            features_url, headers=self.default_headers).json()
        if response is not None:
            features = {
                'danceability': [],
                'energy': []
            }
            for track in response.get('audio_features'):
                features['danceability'].append(track.get('danceability'))
                features['energy'].append(track.get('energy'))

            return sum(features.get('danceability'))/len(features.get('danceability')),\
                sum(features.get('energy'))/len(features.get('energy'))

    def search(self, query):
        query_transformed = query.replace(' ', '%20')
        search_url = f'https://api.spotify.com/v1/search?q={query_transformed}*&type=artist&limit=10'
        response = requests.get(
            search_url, headers=self.default_headers).json()
        filtered_artists = []
        if response is not None:
            artists = response.get('artists').get('items')
            for artist in artists:
                if artist.get('popularity') > 50:
                    filtered_artists.append(artist.get('name'))
        if len(filtered_artists) > 0:
            return filtered_artists
        return None


def b64encode(msg: str) -> str:
    """
    Base 64 encoding for Unicode strings.
    """
    return _b64encode(msg.encode()).decode()

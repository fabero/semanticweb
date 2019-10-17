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
        response = requests.get(artist_url, headers=self.default_headers).json()
        return response

    def get_artist_albums(self, artist_id):
        albums_url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
        response = requests.get(albums_url, headers=self.default_headers).json().get('items')
        album_titles = list(set([album['name'] for album in response]))
        return album_titles

    def get_top_tracks(self, artist_id):
        tracks_url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=NL'
        response = requests.get(tracks_url, headers=self.default_headers).json().get('tracks')
        track_names = list(set([track['name'] for track in response]))
        return track_names


def b64encode(msg: str) -> str:
    """
    Base 64 encoding for Unicode strings.
    """
    return _b64encode(msg.encode()).decode()

from spotipy.scope import every
import requests
from base64 import b64encode as _b64encode
from spotipy import Spotify as SpotifyAPI
import os

CLIENT_ID = 'acbabb4dfeb642f090a34cce20cfabc1'
CLIENT_SECRET = '9cbb51fba6d84ebc860694051a5336d8'


class Spotify:
    """Interacts with Spotify API"""
    def __init__(self):
        if os.path.exists('token'):
            with open('token', 'r') as f:
                print('found existing token')
                token = f.readline()
        else:
            token = self.get_token()
        self.s = SpotifyAPI(token)

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

    def get_artist(self, artist_id):
        try:
            return self.s.artist(artist_id)
        except:
            return None



def b64encode(msg: str) -> str:
    """
    Base 64 encoding for Unicode strings.
    """
    return _b64encode(msg.encode()).decode()

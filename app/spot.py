import random

import requests
from typing import Any, Dict

import config


class SpotifyAPI:

    def __init__(self) -> None:
        self.token: str = self.authorize_request()

    def authorize_request(self) -> str:
        """Requests Client Credentials authorization from Spotify Web API.

        :return String: if successful, the Spotify-provided OAuth access token. else none TODO
        """
        auth_params = {'grant_type': 'client_credentials'}
        print(config.spotify_client_id())
        print(config.spotify_client_secret())
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            data=auth_params,
            auth=(config.spotify_client_id(), config.spotify_client_secret()))

        return response.json().get('access_token')

    def verify_valid_artist(self, artist_name: str):
        """
        Performs a Search query on the Spotify API with the given artist name
        and returns the associated artist ID, if such an artist is found.

        :param String artist_name: name of artist to be found
        :return Tuple: information for artist given as (id:String, name:String, popularity:int) or (None, None, None, None, None)
                       if artist not valid TODO
        """
        search_params = {'q': artist_name, 'type': 'artist', 'market': 'US', 'limit': '1'}
        search_headers = {'Authorization': 'Bearer {}'.format(self.token)}
        response = requests.get('https://api.spotify.com/v1/search',
                                headers=search_headers, params=search_params)

        if response.json().get('artists'):
            return response.json().get('artists').get('items')[0]
        else:
            return {}

    def get_related_artists(self, artist_id: str) -> Dict:
        """ """
        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        response = requests.get(
            'https://api.spotify.com/v1/artists/{}/related-artists'.format(artist_id),
            headers=headers,
            params={'id': artist_id})

        return response.json().get('artists')

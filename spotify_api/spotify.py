from django.http import HttpRequest
from spotipy.oauth2 import SpotifyOAuth
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import os
import time
import spotipy
import random
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
HOST_URL = str(os.environ.get('HOST_URL'))  # url to redirect
SCOPE = """playlist-modify-private,playlist-modify-public"""

def get_token(request: HttpRequest) -> SpotifyOAuth:
    """Generates a token if is expired

    Args:
        request (HttpRequest): _description_

    Returns:
        SpotifyOAuth: _description_
    """
    token_info = request.session.get('token_auth', None)
    if not token_info:
        return None
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth(request)
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


def create_spotify_oauth() -> SpotifyOAuth:
    """Creates an SpotifyOAuth object with SCOPE = playlist-modify-private and redirects to the home page

    Args:
        request (HttpRequest):

    Returns:
        SpotifyOAuth:
    """
    redir_url = os.path.join(HOST_URL, "callback")
    return SpotifyOAuth(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, redirect_uri=redir_url)


def is_expired(request: HttpRequest) -> bool:
    """Checks if the token has expired

    Args:
        request (HttpRequest):

    Returns:
        bool: Returns True if token has expired
    """
    token_info = request.session.get('token_auth', None)
    if not token_info:
        return True
    now = int(time.time())
    return token_info['expires_at'] - now < 30


def create_spotify_playlist(sp: spotipy.Spotify, name: str, public: bool, collaborative: bool, desc: str) -> int:
    """Creates an empty spotify playlist.

    Args:
        sp (SpotifyOAuth): Object with the current user to be able to connect spotify's api.
        name (str): Name of the playlist
        public (bool): True if playlist is public, False if playlist is private
        collaborative (bool): True if is collaborative, False if is not collaborative
        desc (str): playlist's Description

    Returns:
        int: playlist's id
    """
    user = sp.current_user()
    user_id = user['id']
    playlist_id = sp.user_playlist_create(user=user_id, name=name, public=public,
                                          collaborative=collaborative, description=desc)['id']  # Creates the spotify playlist and return the playlist id.
    return playlist_id


# def add_tracks_to(sp: spotipy.Spotify, playlist_id: int, raw_artists: list) -> None:
#     """Add top 10 songs of the artists given to the playlist.

#     Args:
#         sp (spotipy.Spotify): Object with the current user to be able to connect spotify's API.
#         id (int): Playlist's ID
#         raw_artists (list): Artists's list like ["Bad Bunny", "The Whistlers"]
#     """
#     tracks = []
#     for artist in raw_artists:
#         # Search for the artist
#         search_artist = sp.search(artist, type='artist')
#         # look at the first id result
#         artist_id = search_artist['artists']['items'][0]['id']
#         top_tracks = sp.artist_top_tracks(artist_id=artist_id)['tracks']
#         for track in top_tracks:
#             tracks.append(track['id'])
#         # add the tracks to the spotify playlist
#         sp.playlist_add_items(playlist_id=playlist_id, items=tracks)

def add_tracks_to(sp: spotipy.Spotify, playlist_id: int, artists_ids: list) -> None:
    """Add top 10 songs of the artists given to the playlist.

    Args:
        sp (spotipy.Spotify): Object with the current user to be able to connect spotify's API.
        id (int): Playlist's ID
        raw_artists (list): Artists's list like ['1b62AO1IzcVr5SOgoguc9o', '4jhHaLksdP8DJZzxYAjOSz']
    """
    tracks = []
    for artist_id in artists_ids:
        # Search for the artist
        # look at the first id result
        top_tracks = sp.artist_top_tracks(artist_id=artist_id)['tracks']
        top_tracks.sort(key=lambda track: track['popularity'], reverse=True)
        for track in top_tracks:
            tracks.append(track['id'])
    tracks_set = set(tracks)
    tracks = list(tracks_set)
    max_len = 0
    new_tracks = []
    for track in tracks:
        if max_len != 100:  # The max tracks we can append in a playlist in a single request is 100,
            new_tracks.append(track)
            max_len += 1
        else:
            sp.playlist_add_items(
                playlist_id=playlist_id, items=new_tracks)
            new_tracks = []
            max_len = 0
    if len(new_tracks) > 0:
        sp.playlist_add_items(playlist_id=playlist_id, items=new_tracks)


def reorder_playlist(sp: spotipy.Spotify, playlist_id: int):
    """Reorder randomly the playlist

    Args:
        sp (spotipy.Spotify): Object with the current user to be able to connect spotify's API.
        playlist_id (_type_): Playlist's ID
    """
    tracks = sp.playlist_tracks(playlist_id)
    # Get the number of tracks in the playlist
    num_tracks = len(tracks['items']) - 1
    for i in range(len(tracks)):
        sp.playlist_reorder_items(playlist_id=playlist_id, range_start=random.randint(
            0, num_tracks), insert_before=random.randint(0, num_tracks))


def get_playlist_url(sp: spotipy.Spotify, playlist_id: int) -> str:
    """Gets the public url of the playlist

    Args:
        sp (spotipy.Spotify): Object with the current user to be able to connect spotify's API.
        playlist_id (int): Playlist's ID

    Returns:
        str: URL
    """
    playlist = sp.playlist(playlist_id)
    playlist_url = playlist["external_urls"]["spotify"]
    return playlist_url

from django.http import HttpRequest
from spotipy.oauth2 import SpotifyOAuth
import os
import time
import spotipy
import random
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings

CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")


def get_token(request: HttpRequest) -> SpotifyOAuth:
    """Generates a token if is expired

    Args:
        request (HttpRequest): _description_

    Returns:
        SpotifyOAuth: _description_
    """
    token_info = request.session.get("token_auth", None)
    if not token_info:
        return None
    now = int(time.time())
    is_expired = token_info["expires_at"] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth(request)
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    return token_info


def create_spotify_oauth() -> SpotifyOAuth:
    """Creates an SpotifyOAuth object with SCOPE

    Args:
        request (HttpRequest):

    Returns:
        SpotifyOAuth:
    """
    redir_url = settings.WEBSITE_HOSTURL + "/callback"
    print(redir_url)
    SCOPE = """playlist-modify-public"""
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope=SCOPE,
        redirect_uri=redir_url,
    )


def check_logged_in(request) -> bool:
    """If the user is logged in, returns true

    Args:
        request (HttpRequest):

    Returns:
        bool: logged in
    """
    return "token_auth" in request.session and not is_expired(request)

def search_item(str: str, type: str):
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    results = sp.search(str, type=type)
    return results


def is_expired(request: HttpRequest) -> bool:
    """Checks if the token has expired

    Args:
        request (HttpRequest):

    Returns:
        bool: Returns True if token has expired
    """
    token_info = request.session.get("token_auth", None)
    if not token_info:
        return True
    now = int(time.time())
    return token_info["expires_at"] - now < 30


def create_spotify_playlist(
    sp: spotipy.Spotify, name: str, public: bool, collaborative: bool, desc: str
) -> int:
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
    user_id = user["id"]
    playlist_id = sp.user_playlist_create(
        user=user_id,
        name=name,
        public=public,
        collaborative=collaborative,
        description=desc,
    )[
        "id"
    ]  # Creates the spotify playlist and return the playlist id.
    return playlist_id


def add_tracks_to(sp: spotipy.Spotify, playlist_id: int, track_ids: list):
    tracks_set = set(track_ids)  # eliminate repited
    tracks = list(tracks_set)
    max_len = 0
    new_tracks = []
    for track in tracks:
        if (
            max_len != 100
        ):  # The max tracks we can append in a playlist in a single request is 100,
            new_tracks.append(track)
            max_len += 1
        else:
            sp.playlist_add_items(playlist_id=playlist_id, items=new_tracks)
            new_tracks = []
            max_len = 0
    if len(new_tracks) > 0:
        sp.playlist_add_items(playlist_id=playlist_id, items=new_tracks)


def get_top_tracks(artist_id: str):
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    tracks = []
    top_tracks = sp.artist_top_tracks(artist_id=artist_id)["tracks"]
    for track in top_tracks:
        tracks.append(track)
    return tracks


def get_all_tracks_from_artist(artist_id: str):
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    fetch_albums = sp.artist_albums(artist_id=artist_id)
    albums = fetch_albums["items"]
    tracks = []
    for album in albums:
        album_id = album["id"]
        album_tracks = sp.album_tracks(limit=50, album_id=album_id)["items"]
        for track in album_tracks:
            # item.album.images.0.url
            track["album"] = album
            artist_in_track = False
            for artist in track["artists"]:
                if artist["id"] == artist_id:
                    artist_in_track = True
            if artist_in_track:
                tracks.append(track)
    return tracks


def get_all_tracks_from_album(album_id: str):
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    tracks = []
    album_tracks = sp.album_tracks(album_id=album_id, limit=50)["items"]
    album = sp.album(album_id=album_id)
    for track in album_tracks:
        track["album"] = album
        tracks.append(track)
    return tracks


def get_track(track_id: str):
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    result = sp.track(track_id=track_id)
    return result


def get_similar_tracks(track_id: dict):
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    seed_genres = []
    seed_artists = []
    seed_tracks = [track_id]

    tracks_ids = []
    raw_track = sp.track(track_id=track_id)

    for artist in raw_track["artists"]:
        main_artist = sp.artist(artist_id=artist["id"])
        seed_genres.extend(main_artist["genres"])
        seed_artists.append(artist["id"])
    result = sp.recommendations(
        seed_artists=seed_artists[:2],
        seed_genres=seed_genres[:2],
        seed_tracks=seed_tracks,
        limit=10,
    )
    for track in result["tracks"]:
        tracks_ids.append(track)
    return tracks_ids[:10]


def reorder_playlist(sp: spotipy.Spotify, playlist_id: int):
    """Reorder randomly the playlist

    Args:
        sp (spotipy.Spotify): Object with the current user to be able to connect spotify's API.
        playlist_id (int): Playlist's ID
    """
    tracks = sp.playlist_tracks(playlist_id)
    # Get the number of tracks in the playlist
    num_tracks = len(tracks["items"]) - 1
    for i in range(len(tracks)):
        start = random.randint(0, num_tracks)
        insert_before = random.randint(0, num_tracks)
        sp.playlist_reorder_items(
            playlist_id=playlist_id, range_start=start, insert_before=insert_before
        )


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


def add_image_to_item(item: dict) -> str:
    if item["type"] != "track":
        return item
    item["images"] = []
    item["images"] = item["album"]["images"]
    return item

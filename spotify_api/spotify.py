from django.http import HttpRequest
from spotipy.oauth2 import SpotifyOAuth
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import os

CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

def create_spotify_oauth(request: HttpRequest) -> SpotifyOAuth:
    """Creates an SpotifyOAuth object with SCOPE = playlist-modify-private and redirects to the home page

    Args:
        request (HttpRequest): 

    Returns:
        SpotifyOAuth:
    """
    path = reverse('callback') #path of callback view
    site = get_current_site(request) #current host
    protocol = request.scheme #Protocol, http/https
    url = f'{protocol}://{site.domain}{path}' #url to redirect
    SCOPE = """
    playlist-modify-private,
    playlist-modify-public
    """
    return SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, redirect_uri =  url)
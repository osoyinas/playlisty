import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.shortcuts import render,redirect
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.http import HttpRequest, HttpResponse

CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')



def home(request : HttpRequest) -> HttpResponse:
    """
    Index page view. Checks if the user is logged in and passes that information to the template.
    """
    logged_in = False
    if 'auth_token' in request.session:
        logged_in = True
    context = {'logged_in': logged_in}
    return render(request,"home.html", context)

def auth(request : HttpRequest) -> HttpResponse:
    """
    Generates the API token to connect to Spotify's API, redirects to /callback with the token

    """
    sp_oauth = create_spotify_oauth(request)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def callback(request : HttpRequest) -> HttpResponse:
    """
    Saves the token in auth_token and redirects to /home
    """
    auth_token = request.GET.get('code','')
    request.session['auth_token'] = auth_token
    return redirect('home')

def logout(request : HttpRequest) -> HttpResponse:
    """
    Deletes the auth token
    """
    if 'auth_token' in request.session:
        request.session.pop('auth_token')
    return redirect('home')

def create_playlist(request : HttpRequest) -> HttpResponse:
    """
    Renders create_playlist.html
    """
    return render(request, 'create_playlist.html')

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
    SCOPE = 'playlist-modify-private'
    return SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, redirect_uri =  url)

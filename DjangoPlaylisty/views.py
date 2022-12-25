import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.shortcuts import render,redirect
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


CLIENT_ID = '5dcef726e59a47318b36c7965f61c9f1'
CLIENT_SECRET = '1c1956e8b13247549621d0b9cfdf9a2d'

def home(request):
    """Index page view. Checks if the user is logged in and passes that information to the template."""
    logged_in = False
    if 'auth_token' in request.session:
        logged_in = True
    context = {'logged_in': logged_in}
    return render(request,"home.html", context)

def auth(request):
    """Generates the API token to connect to Spotify's API, redirects to /callback with the token"""
    sp_oauth = create_spotify_oauth(request)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def callback(request):
    """Saves the token in auth_token and redirects to /home"""
    auth_token = request.GET.get('code','')
    request.session['auth_token'] = auth_token
    return redirect('home')

def logout(request):
    """Deletes the auth token"""
    if 'auth_token' in request.session:
        request.session.pop('auth_token')
    return redirect('home')

def create_playlist(request):
    return render(request, 'create_playlist.html')



def create_spotify_oauth(request):
    path = reverse('callback') #path of callback view
    site = get_current_site(request) #current host
    if request.scheme == 'http':
        url = f'http://{site.domain}{path}' #url to redirect
    else:
        url = f'https://{site.domain}{path}' #url to redirect
    SCOPE = 'playlist-modify-private'
    return SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, redirect_uri =  url)

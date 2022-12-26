import os
from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from spotify_api.spotify import create_spotify_oauth
import spotipy
import json
import random
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
    sp = create_spotify_oauth(request)
    request.session.clear()
    code = request.GET.get('code','')
    token_info = sp.get_access_token(code)
    request.session['auth_token'] = token_info
    return redirect('home')

def logout(request : HttpRequest) -> HttpResponse:
    """
    Deletes the auth token
    """
    if 'auth_token' in request.session:
        request.session.pop('auth_token')
    return redirect('home')
def generate_playlist(request: HttpRequest) -> HttpResponse:
    if 'auth_token' in request.session:
        token_info = get_token(request)
        sp = spotipy.Spotify(auth=token_info['access_token'])
        user = sp.current_user()
        user_id = user['id']
        playlist_id =sp.user_playlist_create(user=user_id,name="Playlisty", public=False, collaborative=False, description="A playlist created with Playlisty" )['id']
        raw_artists = ["Twenty One Pilots", "The Whistlers", "Remzcore"]
        tracks = []
        for artist in raw_artists:
            search_artist = sp.search(artist,type='artist') #Search for the artist
            artist_id = search_artist['artists']['items'][0]['id'] #look at the first result
            top_tracks = sp.artist_top_tracks(artist_id=artist_id)['tracks'] #
            
            for track in top_tracks:
                tracks.append(track['id'])
        sp.playlist_add_items(playlist_id=playlist_id, items=tracks)
        for i in range(len(tracks)):
            sp.playlist_reorder_items(playlist_id=playlist_id, range_start=random.randint(0,len(tracks)), insert_before=random.randint(0,len(tracks)))
        return render(request, 'create_playlist.html')
def create_playlist(request : HttpRequest) -> HttpResponse:
    """
    Renders create_playlist.html
    """

    return render(request, 'create_playlist.html')


import time


def get_token(request: HttpRequest):
    token_info = request.session.get('auth_token', None)
    if not token_info:
        print("No token info")
    now =int(time.time())
    is_expired =token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth(request)
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

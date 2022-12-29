import os
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from spotify_api.spotify import *
import spotipy
import spotipy.oauth2 as oauth2
import random
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
URL = str(os.environ.get('HOST_URL'))  # url to redirect
SCOPE = """
    playlist-modify-private,
    playlist-modify-public
    """

def home(request: HttpRequest) -> HttpResponse:
    """
    Index page view. Checks if the user is logged in and passes that information to the template.
    """
    print("HOME  VIEW")
    logged_in = False
    if 'token_auth' in request.session:
        logged_in = True
    context = {'logged_in': logged_in}
    return render(request, "home.html", context)


def auth(request: HttpRequest) -> HttpResponse:
    """
    Generates the API token to connect to Spotify's API, redirects to /callback with the token
    """
    print("AUTH VIEW")

    auth_manager = oauth2.SpotifyOAuth(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, redirect_uri=URL)
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)


def callback(request: HttpRequest) -> HttpResponse:
    """
    Saves the token in auth_token and redirects to /home
    """
    print("CALLBACK VIEW")

    auth_manager = oauth2.SpotifyOAuth(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, redirect_uri=URL)
    code = request.GET.get('code')
    print("Code:")
    print(code)
    token = auth_manager.get_access_token(code)
    request.session['token_auth'] = token
    print("TOKEN ASIGNADO:")
    print(request.session['token_auth'])
    return redirect('home')


def logout(request: HttpRequest) -> HttpResponse:
    """
    Deletes the auth token
    """
    if 'token_auth' in request.session:
        del request.session['token_auth']
    return redirect('home')


def generate_playlist(request: HttpRequest) -> HttpResponse:
    print("GENERATE PLAYLIST VIEW")
    logged_in = False
    if 'token_auth' in request.session:
        logged_in = True
        print("GENERATED PLAYLIST:")
        print(request.session['token_auth'])
    context = {'logged_in': logged_in}
    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['desc']
        public = False
        if 'public' in request.POST:
            public = True
        collab = False
        artists_ids = request.POST['artists'].split(",")
        artists_ids.pop()
        token_info = request.session['token_auth']
        sp = spotipy.Spotify(auth=token_info['access_token'])
        playlist_id = create_spotify_playlist(sp, name, public, collab, desc)
        add_tracks_to(sp, playlist_id, artists_ids)
        reorder_playlist(sp, playlist_id)
        context = {'playlist_id': playlist_id, 'logged_in': logged_in}
        return render(request, 'generate_playlist.html', context)


def create_playlist(request: HttpRequest) -> HttpResponse:
    """
    Renders create_playlist.html
    """
    print("CREATE PLAYLIST VIEW")
    logged_in = False
    if 'token_auth' in request.session:
        print("create_playlist:")
        print(request.session['token_auth'])
        logged_in = True
    context = {'logged_in': logged_in}
    return render(request, 'create_playlist.html', context)


def get_artists(request: HttpRequest, artist_str: str) -> JsonResponse:
    if artist_str == "undefined":
        return JsonResponse({'message': "Not Found"})
    token_info = request.session['token_auth']
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.search(artist_str, type='artist')
    artists = results['artists']['items']
    artists_list = []
    for artist in artists:
        if artist_str.lower().strip() in artist['name'].lower():
            artists_list.append(artist)
    data = {'message': "Success", 'artists': artists_list[:4]}
    return JsonResponse(data)

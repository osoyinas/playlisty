import os
import string
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from spotify_api.spotify import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
SCOPE = """playlist-modify-private,playlist-modify-public"""


def home(request: HttpRequest) -> HttpResponse:
    """
    Index page view. Checks if the user is logged in and passes that information to the template.
    """

    logged_in = False
    if 'token_auth' in request.session:
        logged_in = True
    context = {'logged_in': logged_in}
    return render(request, "home.html", context)


def auth(request: HttpRequest) -> HttpResponse:
    """
    Generates the API token to connect to Spotify's API, redirects to /callback with the token
    """
    auth_manager = create_spotify_oauth()
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)


def callback(request: HttpRequest) -> HttpResponse:
    """
    Saves the token in auth_token and redirects to /home
    """
    code = request.GET.get('code')
    auth_manager = create_spotify_oauth()
    token = auth_manager.get_access_token(code=code, check_cache=False)
    request.session['token_auth'] = token
    return redirect('home')


def logout(request: HttpRequest) -> HttpResponse:
    """
    Deletes the auth token
    """
    if 'token_auth' in request.session:
        del request.session['token_auth']
        request.session.clear()
    return redirect('home')


def generate_playlist(request: HttpRequest) -> HttpResponse:
    logged_in = False
    if 'token_auth' in request.session:
        token_info = get_token(request)
        logged_in = True
    else:
        context = {'logged_in': logged_in}
        return render(request, 'create_playlist.html', context)
    name = request.POST['name']
    desc = request.POST['desc']
    public = 'public' in request.POST
    collab = False
    artists_ids = request.POST['artists'].split(",") #list of artists IDS
    artists_ids.pop() #the last element is ''
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
    logged_in = False
    if 'token_auth' in request.session:
        logged_in = True
    context = {'logged_in': logged_in}
    return render(request, 'create_playlist.html', context)


def get_artists(request: HttpRequest, artist_str: str) -> JsonResponse:
    if artist_str == "undefined":
        return JsonResponse({'message': "Not Found"})
    token_info = get_token(request)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.search(artist_str, type='artist')
    artists = results['artists']['items']
    artists_list = []
    for artist in artists:
        if artist_str.lower().strip() in artist['name'].lower():
            artists_list.append(artist)
    data = {'message': "Success", 'artists': artists_list[:4]}
    return JsonResponse(data)

import os
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from spotify_api.spotify import *
import spotipy
import json
import random
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')


def home(request: HttpRequest) -> HttpResponse:
    """
    Index page view. Checks if the user is logged in and passes that information to the template.
    """
    logged_in = False
    if 'auth_token' in request.session:
        logged_in = True
    context = {'logged_in': logged_in}
    return render(request, "home.html", context)


def auth(request: HttpRequest) -> HttpResponse:
    """
    Generates the API token to connect to Spotify's API, redirects to /callback with the token
    """
    sp_oauth = create_spotify_oauth(request)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


def callback(request: HttpRequest) -> HttpResponse:
    """
    Saves the token in auth_token and redirects to /home
    """
    sp = create_spotify_oauth(request)
    request.session.clear()
    code = request.GET.get('code', '')
    token_info = sp.get_access_token(code)
    request.session['auth_token'] = token_info
    return redirect('home')


def logout(request: HttpRequest) -> HttpResponse:
    """
    Deletes the auth token
    """
    if 'auth_token' in request.session:
        request.session.pop('auth_token')
    return redirect('home')


def generate_playlist(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        name = request.POST['name']
        desc = request.POST['desc']
        raw_artists = request.POST['artists'].split(",")
        artists = []
        for raw_artist in raw_artists:
            artists.append(raw_artist.strip())
        if len(artists) == 0:
            artists = ["Bad Bunny"]
        token_info = request.session.get('auth_token')
        sp = spotipy.Spotify(auth=token_info['access_token'])
        public = False
        collab = False
        playlist_id = create_spotify_playlist(
            sp, name, public, collab, desc)
        add_tracks_to(sp, playlist_id, artists)
        reorder_playlist(sp, playlist_id)
        playlist_url = get_playlist_url(sp, playlist_id)
        return render(request, 'generate_playlist.html', {'playlist_id': playlist_id})


def create_playlist(request: HttpRequest) -> HttpResponse:
    """
    Renders create_playlist.html
    """
    logged_in = False
    if 'auth_token' in request.session:
        logged_in = True
    context = {'logged_in': logged_in}
    return render(request, 'create_playlist.html', context)


def get_artists(request: HttpRequest) -> JsonResponse:
    str = request.POST['artist_name']
    print(str)
    token_info = request.session.get('auth_token')
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.search(str, type='artist')
    artists = results['artists']['items'][:5]
    artists_list = []
    for artist in artists:
        artists_list.append(artist)
    print(artists_list)
    data = {'message': "Success", 'artists': artists_list}
    return JsonResponse(data)

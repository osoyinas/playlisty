import os
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from spotify_api.spotify import *
import spotipy
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
    print("RANDOM NUMBER in HOME:")
    request.session["random"] = random.randint(0, 100)
    print(request.session["random"])
    return render(request, "home.html", context)


def auth(request: HttpRequest) -> HttpResponse:
    """
    Generates the API token to connect to Spotify's API, redirects to /callback with the token
    """
    sp_oauth = create_spotify_oauth(request)
    auth_url = sp_oauth.get_authorize_url()
    print("URL:")
    print(auth_url)
    print("------------------------------")
    return redirect(auth_url)


def callback(request: HttpRequest) -> HttpResponse:
    """
    Saves the token in auth_token and redirects to /home
    """
    sp = create_spotify_oauth(request)
    request.session.clear()
    request.session.delete()
    request.session.flush()
    code = request.GET.get('code', '')
    token_info = sp.get_access_token(code)
    request.session['auth_token'] = token_info
    print("TOKEN ASIGNADO:")
    print(request.session['auth_token'])
    print("------------------------------")

    return redirect('home')


def logout(request: HttpRequest) -> HttpResponse:
    """
    Deletes the auth token
    """
    if 'auth_token' in request.session:
        request.session.pop('auth_token')
        request.session.clear()
        request.session.delete()
        request.session.flush()
        print("LOGGED OUT")
    return redirect('home')


def generate_playlist(request: HttpRequest) -> HttpResponse:
    logged_in = False
    if 'auth_token' in request.session:
        logged_in = True
        print("GENERATED PLAYLIST:")
        print(request.session['auth_token'])
        print("------------------------------")
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
        token_info = request.session['auth_token']
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
    print("RANDOM NUMBER in CREATE PLAYLIST:")
    print(request.session["random"])
    logged_in = False
    if 'auth_token' in request.session:
        print("create_playlist:")
        print(request.session['auth_token'])
        print("------------------------------")
        logged_in = True
    context = {'logged_in': logged_in}
    return render(request, 'create_playlist.html', context)


def get_artists(request: HttpRequest, artist_str: str) -> JsonResponse:
    if artist_str == "undefined":
        return JsonResponse({'message': "Not Found"})
    token_info = get_auth_token(request)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.search(artist_str, type='artist')
    artists = results['artists']['items']
    artists_list = []
    for artist in artists:
        if artist_str.lower().strip() in artist['name'].lower():
            artists_list.append(artist)
    data = {'message': "Success", 'artists': artists_list[:4]}
    return JsonResponse(data)

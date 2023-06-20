import os
import json
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from DjangoPlaylisty.SpotifyAPI.spotify import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.http import Http404


CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')


def home(request: HttpRequest) -> HttpResponse:
    """
    Index page view. Checks if the user is logged in and passes that information to the template.
    """
    logged_in = check_logged_in(request)
    print(logged_in)
    # store the current page
    set_prepath(request)
    context = {'logged_in': logged_in}
    return render(request, "home.html", context)


def auth(request: HttpRequest) -> HttpResponse:
    """
    Generates the API token to connect to Spotify's API, redirects to /callback with the token
    """
    try:
        auth_manager = create_spotify_oauth()
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)
    except:
        previus = request.session['pre_path']
        return redirect(previus)


def callback(request: HttpRequest) -> HttpResponse:
    """
    Saves the token in auth_token and redirects to /home
    """
    previus = request.session['pre_path']
    code = request.GET.get('code')
    auth_manager = create_spotify_oauth()
    token = auth_manager.get_access_token(code=code, check_cache=False)
    request.session['token_auth'] = token
    return redirect(previus)


def logout(request: HttpRequest) -> HttpResponse:
    """
    Deletes the auth token
    """
    previus = request.session['pre_path']
    if 'token_auth' in request.session:
        del request.session['token_auth']
        request.session.clear()
    return redirect(previus)


def create_playlist(request: HttpRequest) -> HttpResponse:
    """
    Renders create_playlist.html
    """
    logged_in = check_logged_in(request)
    set_prepath(request)
    context = {'logged_in': logged_in}
    return render(request, 'create_playlist.html', context)


def get_playlist(request: HttpRequest) -> HttpResponse:
    """Generates de playlist

    Args:
        request (HttpRequest): request

    Returns:
        HttpResponse: response
    """

    logged_in = check_logged_in(request)

    if not logged_in or request.session['pre_path'] == request.resolver_match.url_name:
        return redirect('createplaylist')

    set_prepath(request)

    if request.method == 'POST':
        try:
            token_info = get_token(request)
            data = json.loads(request.body.decode('utf-8'))
            sp = spotipy.Spotify(auth=token_info['access_token'])
            name = data['name']
            desc = "A playlists generated with playlisty.app"
            public = True
            collab = False
            playlist_id = create_spotify_playlist(
                sp, name, public, collab, desc)
            artists_ids = list(data['list'])
            add_tracks_to(sp, playlist_id, artists_ids)
            reorder_playlist(sp, playlist_id)
            url = get_playlist_url(sp, playlist_id)
            data = {'message': "Success", 'url': url}
        except ValueError as v:
            data = {'message': "Failed"}
        return JsonResponse(data)

    elif (request.method == 'GET'):
        data = json.loads(request.body.decode('utf-8'))
        url = data['url']
        context = {'url': url, 'logged_in': logged_in}
        return render(request, 'generate_playlist.html', context)
    else:
        raise Http404


def get_artists(request: HttpRequest, artist_str: str) -> JsonResponse:
    """Returns a JSON with N artists name by inputing a str.
        INPUT: Bad
        JSON: Bad Bunny, Bad Gyal, Bad Omen, Klaus Badelt

    Args:
        request (HttpRequest): request
        artist_str (str): search string

    Returns:
        JsonResponse: JSON
    """
    logged_in = check_logged_in(request)
    if artist_str == "undefined" or not logged_in:
        return JsonResponse({'status': "not found"})
    token_info = get_token(request)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.search(artist_str, type='artist')
    artists = results['artists']['items']
    artists_list = []
    artists_number = 6
    for artist in artists:
        if artist_str.lower().strip() in artist['name'].lower():
            artists_list.append(artist)
    data = {'status': "success", 'results': artists_list[:artists_number]}
    return JsonResponse(data)


def getLoginStatus(request: HttpRequest):
    data = {'status': check_logged_in(request)}
    return JsonResponse(data=data)

# Aux functions


def set_prepath(request: HttpRequest):
    """
    Saves the current web page to control redirects. If i am in /createplaylist and i logout, I will be redirected to /createplaylist 

    Args:
        request (HttpRequest): request
    """
    request.session['pre_path'] = request.resolver_match.url_name


def check_logged_in(request) -> bool:
    """If the user is logged in, returns true

    Args:
        request (HttpRequest):

    Returns:
        bool: logged in
    """
    return 'token_auth' in request.session and not is_expired(request)

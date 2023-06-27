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
    # store the current page
    set_prepath(request)
    context = {'logged_in': logged_in}
    print("HOME",logged_in)
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
    return redirect('/createplaylist')


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
    print(logged_in)
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
            name = "playlisty playlist"
            desc = "A playlists generated with playlisty.app"
            public = True
            collab = False

            items = list(data['items'])
            
            artists = []
            tracks = []
            albums = []
            for item in items:
                if (item['type'] == "track"):
                    tracks.append(item)
                elif (item['type'] == "artist"):
                    artists.append(item)
                elif (item['type'] == "album"):
                    albums.append(item)
            playlist_id = create_spotify_playlist(sp,"prueba5",public,collab,desc)
            tracks_to_add= []
            for artist in artists:
                artist_tracks = []
                if artist['option'] == "top-tracks":
                    artist_tracks = get_top_tracks(sp=sp,artist_id=artist['id'])
                elif artist['option'] == "all-tracks":
                    artist_tracks = get_all_tracks_from_artist(sp=sp,artist_id=artist['id'])
                tracks_to_add.extend(artist_tracks)
            for album in albums:
                album_tracks = get_all_tracks_from_album(sp=sp, album_id=album['id'])
                tracks_to_add.extend(album_tracks)
            for track in tracks:
                if (track['option'] == 'just-this'):
                    tracks_to_add.append(track['id'])
                elif track['option'] == 'similar-tracks':
                    print("to do, similar songs")
                    #to do, similar songs
            url = get_playlist_url(sp=sp,playlist_id=playlist_id)
            add_tracks_to(sp=sp, playlist_id=playlist_id, track_ids=tracks_to_add)
            data = {'message': "Success", 'url': url}
        except ValueError as v:
            data = {'message': "failed"}
    return JsonResponse(data)



def get_item(request: HttpRequest, item_str: str, item_type:str) -> JsonResponse:
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
    if item_str == "undefined" or not logged_in:
        return JsonResponse({'status': "not found"})
    token_info = get_token(request)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.search(item_str, type=item_type)
    items = results[item_type +"s"]['items']
    items_list = []
    max_items = 6
    for item in items:
        items_list.append(item)
    data = {'status': "success", 'results': items_list[:max_items]}
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

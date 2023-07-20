import json
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from .api.spotify import *
import spotipy
import urllib.parse

def create_playlist(request: HttpRequest) -> HttpResponse:
    """
    Renders create_playlist.html
    """
    if request.method != 'GET':
        return Http404
    query_string = request.GET.get("data", "")
    if query_string:
        decoded_query = urllib.parse.unquote(query_string)
        data = json.loads(decoded_query)
        try:
            data = json.loads(decoded_query)
            items = list(data["items"])
            artists = list(
                filter(lambda item: item["type"] == "artist", items))
            tracks = list(filter(lambda item: item["type"] == "track", items))
            albums = list(filter(lambda item: item["type"] == "album", items))
            tracks_to_add = []

            for artist in artists:
                artist_tracks = []
                if artist["option"] == "top-tracks":
                    artist_tracks = get_top_tracks(artist_id=artist["id"])
                elif artist["option"] == "all-tracks":
                    artist_tracks = get_all_tracks_from_artist(
                        artist_id=artist["id"])
                tracks_to_add.extend(artist_tracks)

            for album in albums:
                album_tracks = get_all_tracks_from_album(album_id=album["id"])
                tracks_to_add.extend(album_tracks)

            for track in tracks:
                tracks_to_add.append(get_track(track_id=track['id']))
                if track["option"] == "similar-tracks":
                    tracks_to_add.extend(
                        get_similar_tracks(track_id=track["id"]))

            duration = 0
            for track in tracks_to_add:
                duration += track["duration_ms"]
            duration_secs = int((duration / 1000) % 60)
            duration_mins = int((duration / 1000) // 60)
        except ValueError as v:
            data = {"message": "failed"}
        return render(
            request,
            "custom_playlist.html",
            {
                "data": tracks_to_add,
                "length": len(tracks_to_add),
                "duration_mins": duration_mins,
                "duration_secs": duration_secs,
            },
        )
    return render(request, "create_playlist.html", {})


def get_playlist(request: HttpRequest) -> HttpResponse:
    """Generates de playlist

    Args:
        request (HttpRequest): request

    Returns:
        HttpResponse: response
    """

    if request.method != "POST":
        return
    logged_in = check_logged_in(request=request)
    data = {"message": ""}
    if not logged_in:
        data = {"message": "not logged in"}
        return JsonResponse(data)
    try:
        token_info = get_token(request)  # get token api
        data = json.loads(request.body.decode("utf-8"))  # get body data
        sp = spotipy.Spotify(auth=token_info["access_token"])
        name = str(data["name"])
        if name == "":
            name = "A playlist created with Playlisty app"

        desc = "A playlists generated with playlisty.app"
        public = True
        collab = False
        items = list(data["items"])
        playlist_id = create_spotify_playlist(sp, name, public, collab,
                                              desc)
        tracks_to_add = list(data["items"])
        url = get_playlist_url(sp=sp, playlist_id=playlist_id)
        add_tracks_to(sp=sp, playlist_id=playlist_id, track_ids=tracks_to_add)
        data = {"message": "Success", "url": url, "id": playlist_id}
    except ValueError as v:
        data = {"message": "failed"}
    return JsonResponse(data)


def generated_playlist(request: HttpRequest) -> JsonResponse:
    if request.method != "GET":
        return Http404
    query_string = request.GET.get("data", "")
    if query_string:
        decoded_query = urllib.parse.unquote(query_string)
        data = json.loads(decoded_query)
        print(data)
        return render(
            request,
            "generated_playlist.html",
            {"id": data["id"]},
        )


def get_item(request: HttpRequest, item_str: str, item_type: str) -> JsonResponse:
    """Returns a JSON with N artists name by inputing a str.
        INPUT: Bad
        JSON: Bad Bunny, Bad Gyal, Bad Omen, Klaus Badelt

    Args:
        request (HttpRequest): request
        artist_str (str): search string

    Returns:
        JsonResponse: JSON
    """
    try:
        results = search_item(item_str, item_type)
    except:
        return Http404
    items = results[item_type + "s"]["items"]
    items_list = []
    max_items = 6
    for item in items:
        items_list.append(add_image_to_item(item))
    data = {"status": "success", "results": items_list[:max_items]}
    return JsonResponse(data=data)

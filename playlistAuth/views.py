import json
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from playlistGeneration.api.spotify import check_logged_in, create_spotify_oauth


def auth(request: HttpRequest) -> HttpResponse:
    """
    Generates the API token to connect to Spotify's API, redirects to /callback with the token
    """
    try:
        auth_manager = create_spotify_oauth()
        auth_url = auth_manager.get_authorize_url()
        if request.method == 'POST':
            back_url = json.loads(request.body.decode("utf-8"))
            request.session['back_url'] = back_url
            return JsonResponse({'auth_url': auth_url})

        return redirect(auth_url)
    except:
        previus = request.session["pre_path"]
        return redirect('home')


def callback(request: HttpRequest) -> HttpResponse:
    """
    Saves the token in auth_token and redirects to /home
    """
    previus = request.session["pre_path"]
    code = request.GET.get("code")
    auth_manager = create_spotify_oauth()
    token = auth_manager.get_access_token(code=code, check_cache=False)
    request.session["token_auth"] = token
    if 'back_url' in request.session:
        back_url = request.session['back_url']
        del request.session['back_url']
        return redirect(back_url)
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


def get_login_status(request: HttpRequest):
    data = {"status": check_logged_in(request)}
    return JsonResponse(data=data)

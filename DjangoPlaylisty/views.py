from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from playlistGeneration.api.spotify import check_logged_in


def home(request: HttpRequest) -> HttpResponse:
    """
    Index page view. Checks if the user is logged in and passes that information to the template.
    """

    set_prepath(request)
    logged_in = check_logged_in(request)
    # store the current page
    set_prepath(request)
    context = {"logged_in": logged_in}
    return render(request, "home.html", context)


def not_white_listed(request: HttpRequest):
    return render(request, "not_whitelisted.html")


def why_login(request: HttpRequest):
    return render(request, "why_log_in.html")

# Aux functions


def set_prepath(request: HttpRequest):
    """
    Saves the current web page to control redirects. If i am in /createplaylist and i logout, I will be redirected to /createplaylist

    Args:
        request (HttpRequest): request
    """
    request.session["pre_path"] = request.resolver_match.url_name

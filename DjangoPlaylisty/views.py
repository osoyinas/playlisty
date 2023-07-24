"""
Django home views.

"""
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from playlistGeneration.api.spotify import check_logged_in


def home(request: HttpRequest) -> HttpResponse:
    """
    Index page view. Checks if the user is logged in and passes that information to the template.
    """

    logged_in = check_logged_in(request)
    # store the current page
    context = {"logged_in": logged_in}
    return render(request, "home.html", context)


def not_white_listed(request: HttpRequest):
    """not_white_listed

    Args:
        request (HttpRequest): _description_

    Returns:
        _type_: _description_
    """
    return render(request, "not_whitelisted.html")


def why_login(request: HttpRequest):
    """why_login

    Args:
        request (HttpRequest): _description_

    Returns:
        _type_: _description_
    """
    return render(request, "why_log_in.html")

from django.shortcuts import render
import json
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404


def feedback_view(request: HttpRequest) -> HttpResponse:
    data = {"Feedback": "Esto es feedback!!"}
    return JsonResponse(data)

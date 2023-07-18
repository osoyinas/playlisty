from django.shortcuts import render
import json
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def feedback_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        print()
    return JsonResponse({'eyyy':'aaa'})

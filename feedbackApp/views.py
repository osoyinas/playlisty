from django.shortcuts import render
import json
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def feedback_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
    return JsonResponse(data)

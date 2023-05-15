from django.shortcuts import render, HttpResponse
import requests

def index(request):
    return render(request, 'form.html')

def subtitleView(request, *args, **kwargs):
    rsp =  requests.get('http://localhost:8000/api/subtitle/'+str(kwargs['id']))
    rsp.json()
    return render(request, 'subtitles.html', context={'subtitles':rsp.json()})
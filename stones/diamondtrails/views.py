from django.shortcuts import render
from django.http import HttpResponse
from stones import secrets
import requests
# Create your views here.

# def index(request):
#     return HttpResponse("Hello, world. This is diamond3trails")

def index(request):
    url = 'https://www.hikingproject.com/data/get-trails'

    payload = {
        'key': secrets.HP_API_KEY,
        'lat': '47.62',
        'lon': '-122.19', 
        'maxDistance': '20',
    }

    r = requests.get(url, params=payload).json()
    # print(r)

    context = {'trails_data': r}
    # print(r.json())
    # return HttpResponse("Hello, world. This is diamond3trails")
    return render(request, 'diamondtrails/trails.html', context)


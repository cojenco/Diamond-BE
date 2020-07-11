from django.shortcuts import render
from django.http import HttpResponse
from stones import secrets
import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

# def index(request):
#     return HttpResponse("Hello, world. This is diamond3trails")

# def index(request):
#     url = 'https://www.hikingproject.com/data/get-trails'

#     payload = {
#         'key': secrets.HP_API_KEY,
#         'lat': '47.62',
#         'lon': '-122.19', 
#         'maxDistance': '20',
#         'maxResults': '500',
#     }

#     r = requests.get(url, params=payload).json()
#     # print(r)

#     context = {'trails_data': r}
#     # print(r.json())
#     # return HttpResponse("Hello, world. This is diamond3trails")
#     return render(request, 'diamondtrails/trails.html', context)


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
      'Index': 'all-trails',
      'Show': 'trail/<str:external_id>/',
    }

    return Response(api_urls)

@api_view(['GET'])
def trailDetail(request, external_id):
      url = 'https://www.hikingproject.com/data/get-trails-by-id'


      payload = {
          'key': secrets.HP_API_KEY,
          'id': external_id,
      }

      r = requests.get(url, params=payload).json()
      print(r)

      return Response(r)


@api_view(['GET'])
def allTrails(request):
    url = 'https://www.hikingproject.com/data/get-trails'

    payload = {
        'key': secrets.HP_API_KEY,
        'lat': '47.62',
        'lon': '-122.19', 
        'maxDistance': '20',
        # 'maxResults': '500',
    }

    external_results = requests.get(url, params=payload).json()
    print(external_results)
    print('YAY! Successfully called Django API')

    return Response(external_results)    
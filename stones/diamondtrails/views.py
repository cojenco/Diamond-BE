from django.shortcuts import render
from django.http import HttpResponse
from stones import secrets
from .models import StatusUpdate
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
    'apiOverview': '',
    'allTrails': 'all-trails/<str:state_name>',
    'trailDetail': 'trail/<str:external_id>/',
    'liveUpdate': 'trail/<str:external_id>/live-update',
  }

  return Response(api_urls)

@api_view(['GET'])
def trailDetail(request, external_id):
  url = 'https://www.hikingproject.com/data/get-trails-by-id'


  payload = {
      'key': secrets.HP_API_KEY,
      'ids': external_id,
  }

  r = requests.get(url, params=payload).json()
  print(r)

  r['updates'] = [
    {
      'category': 'parking',
      'message': '100%',
    },
    {
      'category': 'visitors',
      'message': '0-5 people',
    },
    {
      'category': 'weather',
      'message': 'hail',
    }
  ]

  print(r)

  return Response(r)


@api_view(['GET'])
def allTrails(request, state_name):
  url = 'https://www.hikingproject.com/data/get-trails'
  print()

  payload = {
      'key': secrets.HP_API_KEY,
      'lat': COORDINATES[state_name]['lat'],
      'lon': COORDINATES[state_name]['lng'], 
      'maxDistance': '200',
      'maxResults': '500',
  }

  external_results = requests.get(url, params=payload).json()
  # print(external_results)
  print('YAY! Successfully called Django API')

  return Response(external_results)    


@api_view(['POST'])
def liveUpdate(request, external_id):
  # create a StatusUpdate instance and save
  print('Yay! Made it here!')
  print(request.data)

  category = request.data["category"]
  message = request.data["message"]

  new_status = StatusUpdate(
  external_id = external_id,
  category = category,
  message = message 
  )

  # new_status.save()

  print(new_status)
  print(new_status.external_id)

  # also filter Subscriptions with that trail (external_id == external_id)
  # make API request to send out SMS


  return Response(request.data)

COORDINATES = {
  'WA' : {
    'lat' : 47.751074,
    'lng' : -120.740139,
  },
  'WI' : {
    'lat' : 43.78444,
    'lng' : -88.787868,
  },
  'WV' : {
    'lat' : 38.597626,
    'lng' : -80.454903,
  },
  'WY' : {
    'lat' : 43.075968,
    'lng' : -107.290284,
  },
}

####### Quick Easy SMS ##########
# import requests

# url = "https://quick-easy-sms.p.rapidapi.com/send"

# payload = "ipnUrl=https%3A%2F%2Fexample.com%2Fabcd&message=message%20content%20from%20RapidAPI&toNumber=1xxxxxxxxxx"
# headers = {
#     'x-rapidapi-host': "quick-easy-sms.p.rapidapi.com",
#     'x-rapidapi-key': "4d112384e9msh3c6d3fb7238549fp126b15jsncd90b141438f",
#     'content-type': "application/x-www-form-urlencoded"
#     }

# response = requests.request("POST", url, data=payload, headers=headers)

# print(response.text)

######payload includes required fields: message and toNumber


#############################




# @api_view(['GET'])
# def allTrails(request):
#     url = 'https://www.hikingproject.com/data/get-trails'

#     payload = {
#         'key': secrets.HP_API_KEY,
#         'lat': '47.62',
#         'lon': '-122.19', 
#         'maxDistance': '20',
#         # 'maxResults': '500',
#     }

#     external_results = requests.get(url, params=payload).json()
#     print(external_results)
#     print('YAY! Successfully called Django API')

#     return Response(external_results)    


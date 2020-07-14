from django.shortcuts import render
from django.http import HttpResponse
from stones import secrets
from .models import StatusUpdate, Subscription, USstate
from .serializers import UpdateSerializer
import requests
import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

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

  # Filter DB to get subscribers 
  ### YET: FILTER CREATED AT WITHIN 72 HOURS
  subs = Subscription.objects.filter(external_id = external_id).count()
  # Filter DB to get weather udpates
  weather_updates = StatusUpdate.objects.filter(external_id = external_id, category = 'weather').order_by('-created_at')
  weather_serializers = UpdateSerializer(weather_updates, many=True)
  weather_stats = weather_serializers.data[:]
  # Filter DB to get parking udpates
  parking_updates = StatusUpdate.objects.filter(external_id = external_id, category = 'parking').order_by('-created_at')
  parking_serializers = UpdateSerializer(parking_updates, many=True)
  parking_stats = parking_serializers.data[:]
  # Filter DB to get visitor udpates
  visitor_updates = StatusUpdate.objects.filter(external_id = external_id, category = 'visitor').order_by('-created_at')
  visitor_serializers = UpdateSerializer(visitor_updates, many=True)
  visitor_stats = visitor_serializers.data[:]

  # Add data to the json response
  r['subscriptions'] = subs
  r['weather_updates'] = weather_stats
  r['parking_updates'] = parking_stats
  r['visitor_updates'] = visitor_stats


  # for update in weather_stats:
  #   print(update['category'])
  #   print(update['message'])
  #   print(update['created_at'])


  # r['updates'] = [
  #   {
  #     'category': 'parking',
  #     'message': '100%',
  #   },
  #   {
  #     'category': 'visitors',
  #     'message': '0-5 people',
  #   },
  #   {
  #     'category': 'weather',
  #     'message': 'hail',
  #   }
  # ]

  print(r)

  return Response(r)


@api_view(['GET'])
def allTrails(request, state_name):
  url = 'https://www.hikingproject.com/data/get-trails'

  state = USstate.objects.get(abbr=state_name)
  print(state.abbr)
  lat = state.lat
  lng = state.lng

  payload = {
      'key': secrets.HP_API_KEY,
      'lat': lat,
      'lon': lng, 
      'maxDistance': '200',
      'maxResults': '500',
  }

  external_results = requests.get(url, params=payload).json()
  print('YAY! Successfully called Django API')

  return Response(external_results)    


@api_view(['POST'])
def liveUpdate(request, external_id):
  # create a StatusUpdate instance and save
  print('Yay! Made it here!')
  print(request.data)

  category = request.data["category"]
  message = request.data["message"]
  current_time = datetime.datetime.now()
  now = str(current_time)

  new_status = StatusUpdate(
  external_id = external_id,
  category = category,
  message = message 
  )

  # new_status.save()

  # Filter DB: Subscriptions with that trail (external_id == external_id)
  # YET TO DO: FILTER SUBSCRIBERS FOR THE LAST 72 HOURS
  # make API request to send out SMS
  subs = Subscription.objects.filter(external_id = external_id)
  print('Looking for subscribers')

  for sub in subs:
    print(sub.phone)
    # IMPORTANT DO NOT DELETE
    # phone = sub.phone
    # content = "TRAIL MIX LIVE! " + category + ": " + message + ". Last updated: " + now
    # url = "https://quick-easy-sms.p.rapidapi.com/send"

    # payload = {
    #   'message': content,
    #   'toNumber': phone,
    # }

    # headers = {
    #     'x-rapidapi-host': "quick-easy-sms.p.rapidapi.com",
    #     'x-rapidapi-key': secrets.SMS_KEY,
    #     'content-type': "application/x-www-form-urlencoded"
    #     }

    # sms_response = requests.post(url, params=payload, headers=headers)
    # print(sms_response.text)
    # IMPORTANT DO NOT DELETE

  return Response(request.data)


@api_view(['POST'])
def subscribe(request, external_id):
  # create a StatusUpdate instance and save
  print('Yay! Made it here!')
  print(request.data)

  phone = "1" + request.data["phone"]

  new_sub = Subscription(
  external_id = external_id,
  phone = phone
  )

  new_sub.save()

  print(new_sub)
  print(new_sub.external_id)

  # also filter StatusUpdates with that trail (external_id == external_id)
  # make API request to send out SMS with last status update
  return Response(request.data)



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

from django.shortcuts import render
from django.http import HttpResponse
from stones import secrets
from .models import StatusUpdate, Subscription, USstate
from .serializers import UpdateSerializer
import requests
import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response


##### Overview of Endpoints #####
@api_view(['GET'])
def apiOverview(request):
  api_urls = {
    'apiOverview': '',
    'allTrails': 'all-trails/<str:state_name>',
    'trailDetail': 'trail/<str:external_id>/',
    'liveUpdate': 'trail/<str:external_id>/live-update',
    'subscribe': 'trail/<str:external_id>/subscribe',
  }

  return Response(api_urls)


##### SHOW: Get One Single Trail #####
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
  weather_updates = StatusUpdate.objects.filter(external_id = external_id, category = 'Weather').order_by('-created_at')
  weather_serializers = UpdateSerializer(weather_updates, many=True)
  weather_stats = weather_serializers.data[:]
  # Filter DB to get parking udpates
  parking_updates = StatusUpdate.objects.filter(external_id = external_id, category = 'Parking').order_by('-created_at')
  parking_serializers = UpdateSerializer(parking_updates, many=True)
  parking_stats = parking_serializers.data[:]
  # Filter DB to get visitor udpates
  visitor_updates = StatusUpdate.objects.filter(external_id = external_id, category = 'Visitor').order_by('-created_at')
  visitor_serializers = UpdateSerializer(visitor_updates, many=True)
  visitor_stats = visitor_serializers.data[:]

  # Add data to the json response
  r['subscriptions'] = subs
  r['weather_updates'] = weather_stats
  r['parking_updates'] = parking_stats
  r['visitor_updates'] = visitor_stats

  print(r)

  return Response(r)


##### INDEX: Retrieve initial 500 trails from coordinates #####
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


##### LiveUpdate: post a new status update #####
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

  new_status.save()

  # Filter DB: Subscriptions with that trail (external_id == external_id)
  # YET TO DO: FILTER SUBSCRIBERS FOR THE LAST 72 HOURS
  subs = Subscription.objects.filter(external_id = external_id)
  print('Looking for subscribers')

  # Send out text messages to alert subscribers
  for sub in subs:
    print(sub.phone)
    print(sub.trail)
    # IMPORTANT DO NOT DELETE
    # phone = sub.phone
    # trail = sub.trail
    # content = "TRAIL MIX LIVE! " + category + ": " + message + ". Location: " + trail + ". Last updated: " + now
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


##### Subscribe: to subscribe to a trail #####
@api_view(['POST'])
def subscribe(request, external_id):
  # create a StatusUpdate instance and save
  print('Yay! Made it here!')
  print(request.data)

  phone = "1" + request.data['phone']
  trail = request.data['trail']

  new_sub = Subscription(
  external_id = external_id,
  phone = phone,
  trail = trail
  )

  new_sub.save()

  return Response(request.data)

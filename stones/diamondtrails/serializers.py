from rest_framework import serializers
from .models import StatusUpdate, Subscription

class UpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = StatusUpdate
    fields ='__all__'
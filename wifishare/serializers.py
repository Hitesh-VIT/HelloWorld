from rest_framework import serializers
from django.contrib.auth.models import User
from models import *


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email',)


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ('SSID', 'location_x', 'location_y', 'password', 'data_limit')


class FindConnectionSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

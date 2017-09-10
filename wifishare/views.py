# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt

from serializers import *
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import make_password
import math
import json


# View To Register Users


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=make_password(
                serializer.validated_data['password']))
        if user is not None:
            return Response({"user": "True", "success": "true"})
        else:
            return Response({"success": "false"})
    return Response({"success": serializer.errors})


# View to create a connection request
@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated, ))
def connection_create(request):
    user = request.user
    Obj=Connection.objects.filter(user_origin=user)
    for i in Obj:
        i.delete()
    serializer = ConnectionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        obj = Connection.objects.create(**serializer.validated_data)
        obj.user_orign = user
        obj.save()
        return Response({"success": "True"})
    else:
        return Response({"success": "False"})


# view to show nearby connections
@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated, ))
def connection_list(request):
    users_nearby = []
    serializer = FindConnectionSerializer(data=request.data)
    if serializer.is_valid():
        lat1 = serializer.validated_data['latitude']
        lon1 = serializer.validated_data['longitude']
        R = 6371
        connection = Connection.objects.filter(conection_established="False")
        for i in connection:

            lat2 = i.location_x
            lon2 = i.location_y
            dlat = (lat2 - lat1) * math.pi / 180
            dlon = (lon2 - lon1) * math.pi / 180
            a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(lat1 * math.pi / 180) * \
                math.cos(lat2 * math.pi / 180) * math.sin(dlon / 2) * math.sin(dlon / 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = R * c
            distance = distance * 1000

            if distance < 50:
                d = {
                    "user": i.user_orign.username,
                    "data_limit": i.data_limit,
                    "distance": distance,
                    "id": i.id}
                users_nearby.append(d)
        ret = {"Nodes":users_nearby}
        return Response(ret)

    return Response({"success": "False"})



# polling url
@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated, ))
def connection_checker(request):
    user = request.user
    obj = Connection.objects.filter(user_orign_id=user.id).first()
    if obj is None:
        return Response({"success": "False"}, status=404)
    if obj.conection_established is True:
        return Response({"success": "True"})
    else:
        return Response({"success": "False"}, status=404)




# Connect to a network
@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated, ))
def connection_establish(request, id):
    user = request.user
    if Profile.objects.get(user=user).credits == 0 :
        return Response({"success": "False"},status=400)
    try:
        obj = Connection.objects.get(id=id)
        obj.user_connection = user
        obj.conection_established = True
        obj.save()
    except :
        return Response({"success": "False"},status=400)

    return Response({ "success": "True", "SSID": obj.SSID,
                     "password": obj.password,"data_limit":obj.data_limit })




# delete a network
@api_view(['POST', 'GET'])
def delete_connection(request):
    user = request.user
    obj = Connection.objects.get(user_orign_id=user.id).delete()
    return Response({"success": "True"})



# Subtracting Ten
@api_view(['GET','POST'])
@permission_classes((IsAuthenticated, ))
def subten(request):
    user = request.user
    obj=Connection.objects.get(user_connection=user)
    user_origin=obj.user_orign
    credits_inc = Profile.objects.get(user=user_origin)
    credits_dec = Profile.objects.get(user=user)
    if credits_dec.credits < 12 :
        credits_dec.credits=0
        credits_dec.save()
        return Response({"success":"True"})
    credits_inc.credits = credits_inc.credits + 10
    credits_inc.save()
    credits_dec.credits = credits_dec.credits - 10
    credits_dec.save()
    return Response({"success":"True"})



#View to get Credits of a user
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def creditsview(request):
    credits = Profile.objects.get(user=request.user).credits
    return Response({"credits":credits})






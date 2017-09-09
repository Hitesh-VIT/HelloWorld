# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt

from serializers import *
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
import math



#View To Register Users

@api_view(['POST'])
def register(request):
    serializer=RegisterSerializer(data= request.data)
    if serializer.is_valid():
        user=User.objects.create(username=serializer.validated_data['username'],email=serializer.validated_data['email'],password=make_password(serializer.validated_data['password']))
        if user is not None:
            return Response({"user":"True","success":"true"})
        else :
            return Response({"success":"false"})
    return Response({"success":serializer.errors})

#View to create a connection request

@api_view(['POST','GET'])
def connection_create(request):
    user=request.user
    serializer =ConnectionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        obj=Connection.objects.create(**serializer.validated_data)
        obj.user_orign = user
        obj.save()
        return Response({"success":"True"})
    else :
        return Response({"success":"False"})


#view to show nearby connections
@api_view(['POST','GET'])
def connection_list(request):
    users_nearby=[]
    serializer = FindConnectionSerializer(data = request.data)
    if serializer.is_valid():
        lat1 = serializer.validated_data['latitude']
        lon1 = serializer.validated_data['longitude']
        R=6371
        connection=Connection.objects.filter(connection_established="False").values('id','loaction_x','location_y','user_orign','data_limit','user_orign_id')
        for i in connection :

            lat2=i['location_x']
            lon2=i['location_y']
            dlat = (lat2 - lat1) * math.pi / 180
            dlon = (lon2 - lon1) * math.pi / 180
            a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(lat1 * math.pi / 180) * math.cos(
                lat2 * math.pi / 180) * math.sin(dlon / 2) * math.sin(dlon / 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = R * c
            distance = distance * 1000
            if distance < 50 :
                list_input = [i['user_orign'],i['data_limit'],distance,i['id']]
                users_nearby.append(list_input)
        return Response({"data":users_nearby})

    return Response({"success":"False"})

# polling url
@api_view(['POST','GET'])
def connection_checker(request):
    user= request.user
    obj=Connection.objects.filter(user_orign_id=user.id).first()
    if obj is None:
        return Response({"success":"False"})
    if obj.conection_established :
        return Response ({"success":"True"})
    else:
        return Response({"success":"False"})


# Connect to a network
@api_view(['POST','GET'])
def connection_establish(request):
    user=request.user
    try:
        obj=Connection.objects.get(id=request.POST['id'])
        obj.user_connection = user
        obj.conection_established = "True"
    except:
        return Response ({"success":"False"})
    return  Response({"success":"True"})



# delete a network
@api_view(['POST','GET'])
def delete_connection(request):
    user = request.user
    obj=Connection.objects.get(user_orign_id=user.id).delete()
    return Response({"success":"True"})





















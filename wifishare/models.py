# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


#Signal to Create a token after creating user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Connection(models.Model):
    SSID=models.CharField(max_length=144)
    password=models.CharField(max_length=250)
    data_limit=models.IntegerField()
    location_x=models.FloatField()
    location_y=models.FloatField()
    user_orign=models.ForeignKey(User,unique=False,blank=True,related_name="origin",null=True)
    user_connection=models.ForeignKey(User,unique=False,blank=True,related_name="destination",null=True)
    conection_established=models.BooleanField(default=False)



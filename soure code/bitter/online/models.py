# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.python manage.py syncdb



class User(models.Model):
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    mail = models.CharField(max_length=50,default = '')
    fullname = models.CharField(max_length=50,default = '')
    #unique = True
    def __str__(self):
        return self.username
class UserRelationship(models.Model):
    selfname=models.CharField(max_length=50)
    friendname=models.CharField(max_length=50)
class UserBlocked(models.Model):
    selfname=models.CharField(max_length=50)
    blockname=models.CharField(max_length=50)


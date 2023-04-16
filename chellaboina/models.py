from django.db import models
# Create your models here.

class Employee(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class USER_details(models.Model):
    NORMAL_USER = 'Normal User'
    USER_TYPES = [
        (NORMAL_USER, 'Normal User'),
    ]
    usertype = models.CharField(max_length=20,choices=USER_TYPES,default=NORMAL_USER,editable=False)
    username = models.CharField(max_length=138)
    email = models.EmailField()
    password = models.CharField(max_length=138)

   

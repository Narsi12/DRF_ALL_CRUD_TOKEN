from django.db import models
# Create your models here.

class Employee(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class USER_details(models.Model):
    username = models.CharField(max_length=138)
    email = models.EmailField()
    password = models.CharField(max_length=138)

   

from django.contrib.auth.models import User
from django.db import models

class Message(models.Model):
    firstname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField(default=0)
    subject = models.CharField(max_length=1000)
    message = models.TextField(max_length=10000)
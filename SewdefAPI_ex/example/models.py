from django.db import models
import datetime

# Create your models here.


class SewDefToken(models.Model):
    expireDate = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(hours=1))
    token = models.TextField()
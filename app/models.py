from django.db import models

# Create your models here.

class Device(models.Model):
    device_id = models.CharField(max_length=64)
    
    #"android", "ios", ...
    type = models.CharField(max_length=16)

    appKey = models.CharField(max_length=32)

    added_date = models.DateTimeField(auto_now_add=True, blank=True)

class PushService(models.Model):

	name = models.CharField(max_length=128)
	app_type = models.CharField(max_length=16)

	app_key = models.CharField(max_length=32)
	app_secret = models.CharField(max_length=32)

	is_production = models.BooleanField(default=False)


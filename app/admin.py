from django.contrib import admin
from models import Device, PushService, Payload

# Register your models here.
admin.site.register(Device)
admin.site.register(PushService)
admin.site.register(Payload)
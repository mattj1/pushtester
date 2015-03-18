from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import datetime

import json
# Create your views here.
import re

from django.core import serializers

from models import *

import requests

from requests.auth import HTTPBasicAuth

def test(request):
    return HttpResponse('This is a test')

def get_recent(request):
	recent = Payload.objects.all().order_by('-added_date')[:10]
# 
	j = []
	for r in recent:
		o = { "text": r.text }
		j.append(o)

	return HttpResponse(json.dumps(j), content_type="application/json")



def add_apid(request):

	response = HttpResponse()

	apid = request.GET.get('apid')
	app_type = request.GET.get('app_type')
	app_appkey = request.GET.get('app_key')

	if not apid:
		response.status_code = 400
		response.write("apid not found")
		return response

	if app_type == None or app_type != "android":
		response.status_code = 400
		response.write("app_type missing or invalid")
		return response

	if app_appkey == None:
		response.status_code = 400
		response.write("app_key missing")
		return response

	pattern = "[0-9a-f]{8}(-[0-9a-f]{4}){2}-[0-9a-f]{4}-[0-9a-f]{12}"
	m = re.match(pattern, apid)
		
	if m == None:
		response.status_code = 400
		response.write("apid invalid")
		return response

	# make sure m.group(0) is equal to the original string
	apid = m.group(0)
	# response.write("m is " + apid + "<br>")
	
	devices = Device.objects.filter(device_id=apid, type=app_type, appKey=app_appkey)

	if devices.count() != 0:
		response.status_code = 200
		response.write("already added")
		return response;


	device = Device(device_id=apid, type=app_type, appKey=app_appkey)
	device.save()

	# output = serializers.serialize("json", Device.objects.filter(id=device.id))

	response.write("Device saved.")
	# response.write(output);

	return response

@csrf_exempt
def add_pushservice(request):
	
	response = HttpResponse()

	name = request.POST.get('name')
	app_type = request.POST.get('app_type')
	app_key = request.POST.get('app_key')
	app_secret = request.POST.get('app_secret')
	is_production = request.POST.get('is_production')

	# for key, value in request.POST.iteritems():
	# 	response.write(key + ":" + value + "<br>")

	if not name:
		response.status_code = 400
		response.write("name not found")
		return response

	if not app_type or app_type != "android":
		response.status_code = 400
		response.write("app_type missing or invalid")
		return response

	if not app_key:
		response.status_code = 400
		response.write("app_key not found")
		return response

	if not app_secret:
		response.status_code = 400
		response.write("app_secret not found")
		return response

	if not is_production:
		response.status_code = 400
		response.write("is_production not found")
		return response

	if is_production == "1":
		is_production = 1
	else:
		is_production = 0

	objs = PushService.objects.filter(name=name, app_key=app_key, app_secret=app_secret, app_type=app_type)
	if objs.count() != 0:
		response.write("already added")
		return response;	

	pushservice = PushService(name=name, app_type=app_type, app_key=app_key, app_secret=app_secret, is_production=is_production)
	pushservice.save()
	
	output = serializers.serialize("json", PushService.objects.filter(id=pushservice.id))

	response.write("Push Service saved.<br>")
	response.write(output + "<br>");

	return response

def send_devices_by_service(service, response, payload_text):
	devices = Device.objects.filter(appKey=service.app_key, type=service.app_type)

	j = {}

	arr_devices = []
	for device in devices:
		arr_devices.append( { 'apid' : device.device_id } )

	response.write("Number of devices: %d<br>" % + devices.count())

	j["notification"] = json.loads("{" + payload_text + "}")
	j["audience"] = { 'OR' : arr_devices }
	j["device_types"] = [service.app_type]

	payload = json.dumps(j)

	headers = {'Content-Type':'application/json', 'Accept' : 'application/vnd.urbanairship+json; version=3;'}

	r = requests.post("https://go.urbanairship.com/api/push/", data=payload, headers=headers, auth=HTTPBasicAuth(service.app_key, service.app_secret))

	if r.status_code != 200:
		response.status_code = 400
		response.write("Error: " + r.text)
	else:
		response.write("Done<br>")

	return response

# send to devices for this given audience type and app key


# requires app key and app type
@csrf_exempt
def send_devices(request):
	response = HttpResponse()

	app_type = request.POST.get('app_type')
	app_key = request.POST.get('app_key')
	payload = request.POST.get('payload')

	if not app_key:
		response.status_code = 400
		response.write("app_key not found")
		return response

	if not app_type:
		response.status_code = 400
		response.write("app_type missing")
		return response
	
	if not payload:
		response.status_code = 400
		response.write("payload missing")
		return response

	services = PushService.objects.filter(app_key=app_key, app_type=app_type)

	if services.count() == 0:
		response.status_code = 400
		response.write("no service found")
		return response

	service = services[0]

	# If this payload is similar to the recent, bump it to the top
	p = get_recent_payload(payload)
	if p != None:
		p.added_date = timezone.now()
		p.save()
	else:
		payload_obj = Payload(text=payload)
		payload_obj.save()

	#remove old payloads
	objs_to_delete = Payload.objects.all().order_by('-added_date')[10:]
	for o in objs_to_delete:
		o.delete()

	response = send_devices_by_service(service, response, payload)

	return response

def get_recent_payload(text):
	# returns the first 10 in the array...
	recent = Payload.objects.all().order_by('-added_date')[:10]

	for p in recent:
		if(p.text == text):
			return p

	return None

def recent_payload():
	return Payload.objects.latest("added_date")

def index(request):
	
	services = PushService.objects.all()
	lastpayload = recent_payload

	template = loader.get_template('app/index.html')
	context = RequestContext(request, {
		'services':services,
		'lastpayload':lastpayload
    })


    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    # return render(request, 'polls/index.html', context)

	return HttpResponse(template.render(context))
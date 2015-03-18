from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
import re

from django.core import serializers

from models import *

import requests

from requests.auth import HTTPBasicAuth

def test(request):
    return HttpResponse('This is a test')


# http://127.0.0.1:8000/app/add_apid?apid=eff29472-27e9-4f54-b047-68531dbe7a92&app_type=android&app_key=Lkm6fvwiRW6M6y5EZ2d6cg
# http://127.0.0.1:8000/app/add_apid?apid=26fd30ec-9074-45c7-9af2-db66cef9adf8&app_type=android&app_key=70b0RZIpTYe_S9wLSrHxKg


def add_apid(request):

	response = HttpResponse()

	apid = request.GET.get('apid')
	app_type = request.GET.get('app_type')
	app_appkey = request.GET.get('app_key')

	if not apid:
		response.code = 400
		response.write("apid not found")
		return response

	if app_type == None or app_type != "android":
		response.code = 400
		response.write("app_type missing or invalid")
		return response

	if app_appkey == None:
		response.code = 400
		response.write("app_key missing")
		return response

	pattern = "[0-9a-f]{8}(-[0-9a-f]{4}){2}-[0-9a-f]{4}-[0-9a-f]{12}"
	m = re.match(pattern, apid)
		
	if m == None:
		response.code = 400
		response.write("apid invalid")
		return response

	# make sure m.group(0) is equal to the original string
	apid = m.group(0)
	# response.write("m is " + apid + "<br>")
	
	devices = Device.objects.filter(device_id=apid, type=app_type, appKey=app_appkey)

	if devices.count() != 0:
		response.code = 200
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
		response.code = 400
		response.write("name not found")
		return response

	if not app_type or app_type != "android":
		response.code = 400
		response.write("app_type missing or invalid")
		return response

	if not app_key:
		response.code = 400
		response.write("app_key not found")
		return response

	if not app_secret:
		response.code = 400
		response.write("app_secret not found")
		return response

	if not is_production:
		response.code = 400
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

def getNotification():
	extras = {}
	extras["word"] = "ad hockery"
	extras["partofspeech"] = "noun"
	extras["shortdefinition"] = "excessive adulation of the mother and undue dependence on maternal care or protection."
	extras["pronunciation"] = "MOM-iz-uhm"

	android = {}
	android["alert"] = "[FREE PROD [S]] Word of the Day: ad hockery"
	android["extra"] = extras

	return { "android" : android }

def send_devices_by_service(service, response):
	devices = Device.objects.filter(appKey=service.app_key, type=service.app_type)


	j = {}

	arr_devices = []
	for device in devices:
		arr_devices.append( { 'apid' : device.device_id } )

	response.write("Number of devices: %d<br>" % + devices.count())

	j["notification"] = getNotification()
	j["audience"] = { 'OR' : arr_devices }
	j["device_types"] = [service.app_type]


	payload = json.dumps(j)

	headers = {'Content-Type':'application/json', 'Accept' : 'application/vnd.urbanairship+json; version=3;'}

	r = requests.post("https://go.urbanairship.com/api/push/", data=payload, headers=headers, auth=HTTPBasicAuth(service.app_key, service.app_secret))

	response.write("Response: " + r.text + "<br>")
	response.write("Done<br>")

# send to devices for this given audience type and app key


# requires app key and app type
def send_devices(request):
	response = HttpResponse()

	app_type = request.GET.get('app_type')
	app_key = request.GET.get('app_key')

	if not app_key:
		response.code = 400
		response.write("app_key not found")
		return response

	if not app_type:
		response.code = 400
		response.write("app_type missing")
		return response

	services = PushService.objects.filter(app_key=app_key, app_type=app_type)

	if services.count() == 0:
		response.code = 400
		response.write("no service found")
		return response

	service = services[0]

	send_devices_by_service(service, response)

	return response

def index(request):
	
	services = PushService.objects.all()

	template = loader.get_template('app/index.html')
	context = RequestContext(request, {
		'services':services
    })


    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    # return render(request, 'polls/index.html', context)

	return HttpResponse(template.render(context))
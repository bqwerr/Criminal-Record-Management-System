from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
import status
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from .decorators import police_only
from rest_framework.response import Response
import io
import base64
from PIL import Image
import os
import dlib
from .models import *
from .serializers import *
from .add_records import generate
from .train import start_train
from .find_matches import match

# API's for Implementing Face Recgnition (Criminal Identification)


@login_required(login_url='login')
@police_only
@api_view(['GET'])
def apiOverview(request):
	urls = {
		'Description': '/api/description/',
		'Get Records' : '/api/records/',
		'Add Record': '/api/add-record/',
		'Delete Record': '/api/delete-record/<str:pk>/',
		'Train Model' : '/api/train/',
		'Match Image' : '/api/match/',
	}
	return Response(urls)

@login_required(login_url='login')
@police_only
@api_view(['GET'])
def description(request):
	response = {
		'Message' : 'This is an API to check if suspected person is present in our criminal database',
	}
	return Response(response)
	
@login_required(login_url='login')
@police_only
@api_view(['GET'])
def train_model(request):
	result = start_train()
	if result:
		return Response({"detail": "Trained model."}, status=status.HTTP_201_CREATED)
	return Response({"error": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='login')
@police_only
@api_view(['POST'])
def add_record(request):

	if 'file' not in request.FILES:
		return Response({"detail" : "Please choose an image"}) 
	file = request.FILES['file']
	img = Image.open(file)
	buff = io.BytesIO()
	img.save(buff, format="JPEG")
	img_str = base64.b64encode(buff.getvalue())
	base64_image = img_str

	request.data["img"] = str(img_str)
	request.data['key_points'] = generate(img_str)
	serializer =  CrimeRecordsSerializer(data=request.data)
	if serializer.is_valid():
		print(1)
		serializer.save()
		print(2)
		Response({"detail" : "record added successfully."})
	return Response({"detail" : "something went wrong."})

@login_required(login_url='login')
@police_only
@api_view(['DELETE'])
def delete_record(request, pk):
	is_present = CrimeRecords.objects.filter(key=pk).exists()
	if not is_present:
		return Response({"error": "key doesn't exists in our database."}, status=status.HTTP_400_BAD_REQUEST)
	item = CrimeRecords.objects.get(key=pk)
	item.delete()
	return Response({"detail" : "record deleted successfully."}, status=status.HTTP_201_CREATED)

@login_required(login_url='login')
@police_only
@api_view(['POST'])
def match_image(request):
	if 'file' not in request.FILES:
		return Response({"detail" : "Please choose an image"}) 
	file = request.FILES['file']
	img = Image.open(file)
	# pwd = os.path.dirname(__file__)
	# img = Image.open(pwd + '/files/alan.jpg')
	buff = io.BytesIO()
	img.save(buff, format="JPEG")
	img_str = base64.b64encode(buff.getvalue())
	base64_image = img_str
	result = match(base64_image)
	if not result:
		return Response({"detail" : "not success"})
	response_data = {}
	data = {}
	
	for res in result:
		pk = str(res[0][0][0])
		print(pk)
		record = CrimeRecords.objects.get(key=pk)
		data['name'] = record.name
		data['against'] = record.against
		data['img'] = record.img
		response_data[pk] = data
	return Response(response_data)


@login_required(login_url='login')
@police_only
@api_view(['GET'])
def get_records(request):
	records = CrimeRecords.objects.all()
	serializer = CrimeRecordsSerializer(records, many=True)
	return Response(serializer.data)
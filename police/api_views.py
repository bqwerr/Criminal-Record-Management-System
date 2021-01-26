from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
import status
from django.contrib.auth.decorators import login_required
# rest-framework
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

# Define API's
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
	pwd = os.path.dirname(__file__)
	img = Image.open(pwd + '/files/Capture.JPG')
	buff = io.BytesIO()
	img.save(buff, format="JPEG")
	img_str = base64.b64encode(buff.getvalue())
	base64_image = img_str
	print(type(img_str))
	request.data["img"] = str(img_str)
	request.data['key_points'] = generate(img_str)
	serializer =  CrimeRecordsSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
	pwd = os.path.dirname(__file__)
	img = Image.open(pwd + '/files/Capture4.JPG')
	buff = io.BytesIO()
	img.save(buff, format="JPEG")
	img_str = base64.b64encode(buff.getvalue())
	base64_image = img_str
	result = match(base64_image)
	print(result)
	if result:
		return Response({"detail" : "success"})
	return Response({"detail" : "not success"})

@login_required(login_url='login')
@police_only
@api_view(['GET'])
def get_records(request):
	records = CrimeRecords.objects.all()
	serializer = CrimeRecordsSerializer(records, many=True)
	return Response(serializer.data)
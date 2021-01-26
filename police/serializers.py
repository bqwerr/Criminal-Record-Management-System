from rest_framework import serializers
from .models import *

# serializing models

class CrimeRecordsSerializer(serializers.ModelSerializer):
	# key = serializers.PrimaryKeyRelatedField(queryset=CrimeRecords.objects.all())
	class Meta:
		model = CrimeRecords
		fields = '__all__'
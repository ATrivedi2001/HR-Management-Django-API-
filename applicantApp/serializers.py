from rest_framework import serializers
from coreApp.models import  Applicant

class Applicantserializer(serializers.ModelSerializer):
     class Meta:  
        model = Applicant 
        fields = '__all__'
        read_only_fields = ['id']
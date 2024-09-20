from rest_framework import serializers
from coreApp.models import Department 

class Departmentserializer(serializers.ModelSerializer):
    class Meta:
        model = Department 
        fields = '__all__'
        read_only_fields = ['id']
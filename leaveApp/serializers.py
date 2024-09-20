from rest_framework import serializers
from coreApp.models import Leave  

class Leaveserializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'
        read_only_fields = ['id']
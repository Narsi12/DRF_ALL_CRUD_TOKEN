from rest_framework import serializers
from .models import Employee,USER_details

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields='__all__'

class USER_Serializer(serializers.ModelSerializer):
    class Meta:
        model = USER_details
        fields = ['username','email','password']
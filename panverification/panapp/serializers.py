from rest_framework import serializers
from panapp.models import UserData

class UserDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        fields = ('id', 'name', 'dob', 'pan')
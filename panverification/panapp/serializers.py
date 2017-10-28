from rest_framework import serializers
from panapp.models import UserData, FeedbackData

class UserDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        fields = ('id', 'name', 'dob', 'pan', 'image')

class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedbackData
        fields = ('id', 'user_data', 'feedback_for', 'details')

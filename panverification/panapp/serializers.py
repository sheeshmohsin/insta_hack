from rest_framework import serializers
from panapp.models import UserData, FeedbackData

class UserDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        fields = ('id', 'image', 'is_verified_agent', 'is_invalid_agent', 'agent')

class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedbackData
        fields = ('id', 'user_data', 'feedback_for', 'details')

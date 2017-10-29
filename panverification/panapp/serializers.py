from rest_framework import serializers
from django.contrib.auth.models import User
from panapp.models import UserData, FeedbackData


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        fields = ('id', 'image', 'is_verified_agent', 'agent', 'status')

class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedbackData
        fields = ('id', 'user_data', 'feedback_for', 'details')

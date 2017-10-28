from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from panapp.serializers import UserDataSerializer
from rest_framework import status

class UserDetails(APIView):
    """
    View to upload data of users
    """
    def post(self, request, format=None):
        """
        Save data of users with pan card image
        """
        data = {}
        name = request.data.get('name')
        dob = request.data.get('dob')
        pan_number = request.data.get('pan_number')
        pan_image = request.data.get('image')
        if name:
            data['name'] = name
        if dob:
            data['dob'] = dob

        if pan_number:
            data['pan'] = pan_number
        if pan_image:
            data['pan_image'] = pan_image

        serializer = UserDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print "here"
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


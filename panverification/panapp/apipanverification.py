from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from panapp.serializers import UserDataSerializer, FeedbackSerializer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

class UserDetails(APIView):
    parser_classes = (MultiPartParser, )
    """
    View to upload data of users
    """
    def post(self, request, format='png'):
        """
        Save data of users with pan card image
        """
        data = {}
        up_file = request.FILES['pan_image']
        data['image'] = up_file
        name = request.data.get('name')
        dob = request.data.get('dob')
        pan_number = request.data.get('pan_number')
        # pan_image = request.data.get('image')
        if name:
            data['name'] = name
        if dob:
            data['dob'] = dob

        if pan_number:
            data['pan'] = pan_number
        # if pan_image:
        #     data['pan_image'] = pan_image

        # destination = open('/tmp/' + up_file.name, 'wb+')
        # for chunk in up_file.chunks():
        #     destination.write(chunk)
        #     destination.close()
        serializer = UserDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeedbackData(APIView):
    def post(self, request, format=None):
        """
        Save feedback data from Agent
        """
        feedback_serialized_data = []
        feedback_data = request.data
        for feedback in feedback_data:
            data = {}
            data['user_data'] = feedback.get('user_data')
            data['feedback_for'] = feedback.get('feedback_for')
            data['details'] = feedback.get('details')
            serializer = FeedbackSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                feedback_serialized_data.append(serializer.data)
                print serializer.data
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(feedback_serialized_data, status=status.HTTP_201_CREATED)

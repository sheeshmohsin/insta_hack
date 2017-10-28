from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from panapp.serializers import UserDataSerializer, FeedbackSerializer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from panapp.models import Agent, UserData

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
        if up_file:
            data['image'] = up_file
        else:
            err_msg = 'Please upload a image'
            return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)
        # name = request.data.get('name')
        # dob = request.data.get('dob')
        # pan_number = request.data.get('pan_number')
        # pan_image = request.data.get('image')
        # if name:
        #     data['name'] = name
        # if dob:
        #     data['dob'] = dob

        # if pan_number:
        #     data['pan'] = pan_number
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

class VerificationDetails(APIView):
    def put(self, request, userdata_id, format=None):
        print "request.data", request.data
        user_data = UserData.objects.get(id=user_id)
        data = {}
        data['is_verified_agent'] = request.data.get('verified_agent')
        data['is_invalid_agent'] = request.data.get('invalid_agent')
        print data
        agent = Agent.objects.get(user=self.request.user)
        serializer = UserDataSerializer(user_data, data=data, partial=True)
        if serializer.is_valid():
            serializer.save(agent=agent)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

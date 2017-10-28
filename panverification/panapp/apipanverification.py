from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from panapp.serializers import UserDataSerializer, FeedbackSerializer, UserSerializer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from panapp.models import Agent, UserData
from panapp.utils import extract_text, check_if_pan_card_pic, get_data, verify_pan_number
from rest_framework.authtoken.models import Token
import json


class CreateUser(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
        print "here", request.data
        entity_type = request.data.get('entity_type')
        data = {}
        data['username'] = request.data.get('username')
        data['password'] = request.data.get('password')
        serialized = UserSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            print serialized.data
            user = User.objects.get(username=serialized.data['username'])
            # api_key = Token.objects.create(user=user)
            if entity_type == 'agent':
                Agent.objects.create(user=user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetails(APIView):
    parser_classes = (MultiPartParser, )
    """
    View to upload data of users
    """
    def post(self, request, format=None):
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
            user_data = UserData.objects.get(id=serializer.data['id'])
            extract_response = extract_text(user_data)
            if extract_response.status_code == 200:
                res_data = extract_response.json()
                if res_data['IsErroredOnProcessing']:
                    user_data.delete()
                    err_msg = "Some error occurred. Please try again"
                    return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)
                else:
                    try:
                        parsed_text = res_data['ParsedResults'][0]['ParsedText']
                        parsed_text = parsed_text.split('\r\n')
                        if not check_if_pan_card_pic(parsed_text):
                            user_data.delete()
                            err_msg = "This is not a valid PAN Card Image"
                            return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)
                        if not verify_pan_number(parsed_text):
                            user_data.delete()
                            err_msg = "This is not a valid PAN Card Number"
                            return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        user_data.delete()
                        err_msg = "Some error occurred. Please try again"
                        return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_data.delete()
                err_msg = "Problem in uploading image. Please try again"
                return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)
            name, dob, pan = get_data(parsed_text)
            user_data.extracted_name = name
            user_data.extracted_dob = dob
            user_data.extracted_pan = pan
            user_data.save()
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

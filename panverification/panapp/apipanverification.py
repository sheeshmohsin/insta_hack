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
from panapp.constants import COMPLETED, PENDING
from django.forms import model_to_dict

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

class LoginUser(APIView):
    """
    View for Login
    """
    def get(self, request, format):
        username = request.data.get('username')
        password = request.data.get('password')
        entity_type = 'user'
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            try:
                api_key = Token.objects.get(user=user)
            except:
                api_key = Token.objects.create(user=user)
            if Agent.objects.filter(user=user).exists():
                entity_type = 'agent'
            return Response({'api_key': api_key.key, 'entity_type':entity_type}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

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
        feedback_data = request.data.get(feedback_data)
        for feedback in feedback_data:
            f_data = {}
            if userdata_id:
                f_data['user_data'] = userdata_id
            if feedback.get('feedback_for'):
                f_data['feedback_for'] = feedback.get('feedback_for')
            if feedback.get('details'):
                f_data['details'] = feedback.get('details')
            f_serializer = FeedbackSerializer(data=f_data)
            if f_serializer.is_valid():
                f_serializer.save()
                feedback_serialized_data.append(f_serializer.data)
                print f_serializer.data
            else:
                return Response(f_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(feedback_serialized_data, status=status.HTTP_201_CREATED)

class VerificationDetails(APIView):
    def put(self, request, userdata_id, format=None):
        agent = None
        try:
            agent = Agent.objects.get(user=self.request.user)
        except:
            pass
        if agent:
            print "request.data", request.data
            user_data = UserData.objects.get(id=user_id)
            data = {}
            data['is_verified_agent'] = request.data.get('verified_agent')
            data['status'] = COMPLETED
            print data
            agent = Agent.objects.get(user=self.request.user)
            serializer = UserDataSerializer(user_data, data=data, partial=True)
            if serializer.is_valid():
                serializer.save(agent=agent)
                feedback_serialized_data = []
                feedback_data = request.data.get(feedback_data)
                for feedback in feedback_data:
                    f_data = {}
                    if userdata_id:
                        f_data['user_data'] = userdata_id
                    if feedback.get('feedback_for'):
                        f_data['feedback_for'] = feedback.get('feedback_for')
                    if feedback.get('details'):
                        f_data['details'] = feedback.get('details')
                    f_serializer = FeedbackSerializer(data=f_data)
                    if f_serializer.is_valid():
                        f_serializer.save()
                        feedback_serialized_data.append(f_serializer.data)
                        print f_serializer.data
                    else:
                        return Response(f_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(feedback_serialized_data, status=status.HTTP_201_CREATED)
                # return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class NextPANData(APIView):
    """
    View to get next PAN Data for verification
    """
    def get(self, request, format=None):
        agent = None
        try:
            agent = Agent.objects.get(user=self.request.user)
        except:
            pass
        if agent:
            user_dict = {}
            user_data = UserData.objects.filter(agent=agent, status=PENDING)
            if user_data.exists():
                user_data = user_data[0]
                api_key = Token.objects.get(user=agent.user)
                user_dict['extracted_name'] = user_data.extracted_name
                user_dict['extracted_dob'] = user_data.extracted_dob
                user_dict['extracted_image'] = str(user_data.image)
                user_dict['extracted_pan'] = user_data.extracted_pan
                data = {'user_data':user_dict, 'api_key':api_key.key}
                return Response(data, status=status.HTTP_200_OK)
            else:
                user_data = UserData.objects.filter(status=PENDING).first()
                user_data.agent = agent
                user_data.save()
                user_dict['extracted_name'] = user_data.extracted_name
                user_dict['extracted_dob'] = user_data.extracted_dob
                user_dict['extracted_image'] = str(user_data.image)
                user_dict['extracted_pan'] = user_data.extracted_pan
                api_key = Token.objects.get(user=agent.user)
                data = {'user_data':user_dict, 'api_key':api_key.key}
                return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)




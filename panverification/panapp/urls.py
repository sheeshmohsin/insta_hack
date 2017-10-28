
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from panapp import apipanverification, views

urlpatterns = [

url(r'^signup/$', apipanverification.CreateUser.as_view()),
url(r'^user_data/$', apipanverification.UserDetails.as_view()),
url(r'^feedback_data/$', apipanverification.FeedbackData.as_view()),
url(r'^verification_details/(?P<userdata_id>\d+)/$', apipanverification.VerificationDetails.as_view()),

]
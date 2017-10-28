
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from panapp import apipanverification

urlpatterns = [

url(r'^user_data/$', apipanverification.UserDetails.as_view()),

]
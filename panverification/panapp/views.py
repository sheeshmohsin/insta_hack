# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def user_page(request):
	return render(request, 'user.html')


def agent_page(request):
	return render(request, 'agent.html')


def login_page(request):
	return render(request, 'login.html')

def signup_agent_page(request):
	return render(request, 'signup_agent.html')

def signup_user_page(request):
	return render(request, 'signup_user.html')
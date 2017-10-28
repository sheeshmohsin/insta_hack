# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def user_page(request):
	return render(request, 'user.html')


def agent_page(request):
	return render(request, 'agent.html')

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from panapp.utils import get_upload_file_path

# Create your models here.

class Agent(models.Model):
	user = models.ForeignKey(User, blank=True, null=True)

	def __unicode__(self):
		return self.user.username


class UserData(models.Model):
	name = models.CharField(max_length=50)
	dob = models.CharField(max_length=12)
	pan = models.CharField(max_length=10)
	image = models.FileField(upload_to=get_upload_file_path)
	extracted_name = models.CharField(max_length=50, blank=True, null=True)
	extracted_dob = models.CharField(max_length=12, blank=True, null=True)
	extracted_pan = models.CharField(max_length=10, blank=True, null=True)
	feedback_name = models.CharField(max_length=50, blank=True, null=True)
	feedback_dob = models.CharField(max_length=12, blank=True, null=True)
	feedback_pan = models.CharField(max_length=10, blank=True, null=True)
	is_verified_auto = models.BooleanField(default=False)
	is_verified_agent = models.BooleanField(default=False)
	is_invalid_auto = models.BooleanField(default=False)
	is_invalid_agent = models.BooleanField(default=False)
	user = models.ForeignKey(User, blank=True, null=True)
	agent = models.ForeignKey(Agent, blank=True, null=True)

	def __unicode__(self):
		return self.user.username


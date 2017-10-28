# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from panapp.models import UserData, FailedUserData, FeedbackData

# Register your models here.
admin.site.register(UserData)
admin.site.register(FailedUserData)
admin.site.register(FeedbackData)

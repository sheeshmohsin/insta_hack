# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from panapp.models import UserData, FeedbackData

# Register your models here.

class UserDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'dob', 'pan', 'image')
    ordering = ('-id', )

class FeedbackDataAdmin(admin.ModelAdmin):
	list_display = ('id', 'user_data', 'feedback_for', 'details')
	ordering = ('-id', )

admin.site.register(UserData, UserDataAdmin)
admin.site.register(FeedbackData, FeedbackDataAdmin)

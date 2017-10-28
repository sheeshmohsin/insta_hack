# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from panapp.models import UserData, FailedUserData, FeedbackData

# Register your models here.

class UserDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
    ordering = ('-id', )

class FeedbackDataAdmin(admin.ModelAdmin):
	list_display = ('id', 'user_data', 'feedback_for', 'details')
	ordering = ('-id', )

admin.site.register(UserData, UserDataAdmin)
admin.site.register(FeedbackData, FeedbackDataAdmin)
admin.site.register(FailedUserData)



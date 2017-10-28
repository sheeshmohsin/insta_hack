from __future__ import absolute_import, unicode_literals
import requests
from celery import task
from panapp.models import UserData, FailedUserData
from panapp.utils import extract_text, check_if_pan_card_pic, \
			detect_if_not_forged, match_with_user_data
from panapp.constants import IMG_INVALID, IMG_FORGED
from django.conf import settings

@task()
def image_validation():
	unscanned_data = UserData.objects.filter(is_scanned=False)
	for data in unscanned_data:
		# data.is_scanned = True
		r = extract_text(data)
		if r.status_code != 200:
			print "continue due to status_code != 200"
			continue
		res_data = r.json()
		print res_data
		if res_data['IsErroredOnProcessing']:
			print "continue due to IsErroredOnProcessing"
			continue
		try:
			parsed_text = res_data['ParsedResults'][0]['ParsedText']
		except Exception as e:
			print e
			continue
		parsed_text = parsed_text.split('\r\n')
		if not check_if_pan_card_pic(parsed_text):
			FailedUserData.objects.create(user_data=data, invalid=IMG_INVALID)
			data.is_invalid_auto = True
			data.save()
			continue

		if not detect_if_not_forged(data.image):
			FailedUserData.objects.create(user_data=data, invalid=IMG_FORGED)
			data.is_invalid_auto = True
			data.save()
			continue

		res = match_with_user_data(parsed_text, data)
		if not res['status']:
			for reason in res['reason']:
				FailedUserData.objects.create(user_data=data, invalid=reason)
			data.is_invalid_auto = True
			data.save()
			continue


		data.is_verified_auto = True
		data.save()
		return True





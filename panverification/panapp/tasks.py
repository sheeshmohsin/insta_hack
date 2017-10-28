from __future__ import absolute_import, unicode_literals
import requests
from celery import task
from panapp.models import UserData, FailedUserData
from panapp.utils import extract_text, check_if_pan_card_pic, \
            detect_if_not_forged, match_with_user_data, verify_pan_number, get_data
from panapp.constants import IMG_INVALID, IMG_FORGED
from django.conf import settings

@task()
def image_validation(data_id):
    data = UserData.objects.get(id=data_id)
    # data.is_scanned = True
    r = extract_text(data)
    if r.status_code != 200:
        print "continue due to status_code != 200"
        data.is_invalid_auto = True
        data.is_verified_auto = False
        data.error_msg = "Some Error Occured, Please Try Again"
        data.save()
        return
    res_data = r.json()
    print res_data
    if res_data['IsErroredOnProcessing']:
        data.is_invalid_auto = True
        data.is_verified_auto = False
        data.error_msg = 'Error Occured during Image Processing'
        data.save()
        return
    try:
        parsed_text = res_data['ParsedResults'][0]['ParsedText']
    except Exception as e:
        data.is_invalid_auto = True
        data.is_verified_auto = False
        data.error_msg = 'Please upload correct image'
        data.save()
        return
    parsed_text = parsed_text.split('\r\n')
    if not check_if_pan_card_pic(parsed_text):
        data.is_invalid_auto = True
        data.is_verified_auto = False
        data.error_msg = 'Please upload correct PAN image'
        data.save()
        return

    if not detect_if_not_forged(data.image):
        data.is_invalid_auto = True
        data.is_verified_auto = False
        data.error_msg = 'Something Fishy is going on, Please Try Again'
        data.save()
        return

    if not verify_pan_number(parsed_text):
        data.is_invalid_auto = True
        data.is_verified_auto = False
        data.error_msg = 'Not a Valid Pan Number, Please Try Again'
        data.save()
        return

    name, dob, pan = get_data(parsed_text)
    data.extracted_name = name
    data.extracted_dob = dob
    data.extracted_pan = pan

    data.is_scanned = True
    data.is_verified_auto = True
    data.is_invalid_auto = False
    data.save()
    return True





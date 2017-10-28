import uuid, os, requests, re
from django.conf import settings
from panapp.constants import NAME_INVALID, DOB_INVALID, PAN_INVALID

def get_upload_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    initial_path = str(settings.BASE_DIR) + str(settings.MEDIA_URL) + 'uploads/'
    return os.path.join(initial_path, filename)

def extract_text(data):
	image_path = str(data.image)
	payload = {'apikey': settings.OCR_SPACE_API_KEY}
	with open(image_path, 'rb') as f:
		r = requests.post(settings.OCR_SPACE_API,
							files={'file': f},
							data=payload
							)
	return r

def check_if_pan_card_pic(parsed_text):
	status = False
	if len(parsed_text) >= 6:
		if 'INCOME TAX DEPARTMENT' in str(parsed_text[0]).strip().upper():
			if 'GOVT. OF INDIA' in str(parsed_text[5]).strip().upper():
				status = True
				return status
	else:
		return False
	for text in parsed_text:
		if 'INCOME TAX DEPARTMENT' in text.strip():
			status = True
		if 'GOVT. OF INDIA' in text.strip():
			status = True
	return status


def detect_if_not_forged(img_url):
	return True


def match_with_user_data(parsed_text, data):
	name_matched = False
	dob_matched = False
	pan_matched = False
	res = {'status': False, 'reason': []}
	if len(parsed_text) > 6:
		if str(parsed_text[1]).strip().upper() == str(data.name).strip().upper():
			name_matched = True
		if str(parsed_text[3]).strip().upper() == str(data.dob).strip().upper():
			dob_matched = True
		if str(parsed_text[5]).strip().upper() == str(data.pan).strip().upper():
			pan_matched = True
	if name_matched and dob_matched and pan_matched:
		res['status'] = True
		return res
	for text in parsed_text:
		if str(text).strip().upper() == str(data.name).strip().upper():
			name_matched = True
		if str(text).strip().upper() == str(data.dob).strip().upper():
			dob_matched = True
		if str(text).strip().upper() == str(data.pan).strip().upper():
			pan_matched = True
	if name_matched and dob_matched and pan_matched:
		res['status'] = True
		return res
	res['status'] = False
	if not name_matched:
		res['reason'].append(NAME_INVALID)
	if not dob_matched:
		res['reason'].append(DOB_INVALID)
	if not pan_matched:
		res['reason'].append(PAN_INVALID)
	return res


def get_data(parsed_text):
	data = (False, False, False)
	if len(parsed_text) >= 6:
		name = str(parsed_text[1]).strip().upper()
		dob = str(parsed_text[3]).strip().upper()
		pan = str(parsed_text[5]).strip().upper()
		data = (name, dob, pan)
	return data


def verify_pan_number(parsed_text):
	reg_exp = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
	fourth_char_dict = {
						'A': True, 'B': True, 'C': True, 'F': True, 'G': True,
						'H': True, 'L': True, 'J': True, 'P': True, 'T': True, 
						'K': True
						}
	fifth_char_dict = {}
	if len(parsed_text) >= 6:
		pan = str(parsed_text[5]).strip().upper()
		name = str(parsed_text[1]).strip().upper()
		for name_part in name.split():
			if name_part:
				fifth_char_dict[name_part[0]] = True
		z = re.match(reg_exp, pan)
		if z:
			if not fourth_char_dict.get(pan[3], None):
				return False
			if not fifth_char_dict.get(pan[4], None):
				return False
			return True
		else:
			return False
	else:
		return False

	

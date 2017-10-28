import uuid, os, requests
from django.conf import settings

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
	for text in parsed_text:
		if 'INCOME TAX DEPARTMENT' in text.strip():
			status = True
		if 'GOVT. OF INDIA' in text.strip():
			status = True
	return status

	

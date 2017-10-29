# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.conf import settings

# Create your tests here.
class SignupTestCase(TestCase):

	def test_signup(self):
		"""
		Positive test case for user signup
		"""
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'user'
							}
						)
		self.assertEqual(resp.status_code, 201)

	def test_duplicate_signup(self):
		"""
		Test case for user Duplicate signup
		"""
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'user'
							}
						)
		self.assertEqual(resp.status_code, 201)
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'user'
							}
						)
		self.assertEqual(resp.status_code, 400)

	def test_agent_signup(self):
		"""
		Positive test case for agent signup
		"""
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'agent'
							}
						)
		self.assertEqual(resp.status_code, 201)

	def test_duplicate_agent_signup(self):
		"""
		Test case for duplicate agent signup
		"""
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'agent'
							}
						)
		self.assertEqual(resp.status_code, 201)
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'agent'
							}
						)
		self.assertEqual(resp.status_code, 400)


class LoginTestCase(TestCase):

	def test_login(self):
		"""
		Positive Test Case for user login
		"""
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'user'
							})
		self.assertEqual(resp.status_code, 201)
		resp = self.client.post('/v1/login/', {
				'username': 'testuser', 'password': 'testuser'
			})
		self.assertEqual(resp.status_code, 200)

	def test_wrong_login_user(self):
		"""
		Test Case for user login with wrong credentials
		"""
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'user'
							})
		self.assertEqual(resp.status_code, 201)
		resp = self.client.post('/v1/login/', {
				'username': 'testuser', 'password': 'testuser1'
			})
		self.assertEqual(resp.status_code, 401)

	def test_login_agent(self):
		"""
		Positive Test Case of agent login
		"""
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'agent'
							})
		self.assertEqual(resp.status_code, 201)
		resp = self.client.post('/v1/login/', {
				'username': 'testuser', 'password': 'testuser'
			})
		self.assertEqual(resp.status_code, 200)

	def test_wrong_login_agent(self):
		"""
		Test Case of agent login with wrong credentials
		"""
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'agent'
							})
		self.assertEqual(resp.status_code, 201)
		resp = self.client.post('/v1/login/', {
				'username': 'testuser', 'password': 'testuser1'
			})
		self.assertEqual(resp.status_code, 401)


class ImageUploadTestCase(TestCase):

	def test_upload(self):
		"""
		Positive Test Case for image upload
		"""
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'user'
							})
		self.assertEqual(resp.status_code, 201)
		resp = self.client.post('/v1/login/', {
				'username': 'testuser', 'password': 'testuser'
			})
		self.assertEqual(resp.status_code, 200)
		api_key = resp.json()['api_key']
		token = 'Token ' + api_key
		auth_headers = {
    		'HTTP_AUTHORIZATION': token,
		}
		path = str(settings.BASE_DIR) + '/panapp/testimg/pan_card_sample_2.jpg'
		headers = {'Authorization': token}
		with open(path) as fp:
			resp = self.client.post('/v1/user_data/', {'pan_image': fp}, **auth_headers)
		self.assertEqual(resp.status_code, 201)

class VerificationDetailsTestCase(TestCase):

	def test_verify_details_non_agent(self):
		"""
		Negative Test case for verifying if agent is unauthorized
		"""
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'user'
							})
		self.assertEqual(resp.status_code, 201)
		resp = self.client.post('/v1/login/', {
				'username': 'testuser', 'password': 'testuser'
			})
		self.assertEqual(resp.status_code, 200)
		api_key = resp.json()['api_key']
		token = 'Token ' + api_key
		auth_headers = {
    		'HTTP_AUTHORIZATION': token,
		}
		path = str(settings.BASE_DIR) + '/panapp/testimg/pan_card_sample_2.jpg'
		headers = {'Authorization': token}
		with open(path) as fp:
			user_resp = self.client.post('/v1/user_data/', {'pan_image': fp}, **auth_headers)
		self.assertEqual(user_resp.status_code, 201)
		user_resp_id = user_resp.json()['id']

		data_val={'verified_agent':False, 'feedback_data':[{'userdata_id':user_resp_id, 'feedback_for':'1', 'details':'testuser'}]}
		r = self.client.put('/v1/verification_details/'+str(user_resp_id)+'/', data=data_val, **auth_headers)
		self.assertEqual(r.status_code, 401)

class GetPANDataTestCase(TestCase):
	def test_user_authentication_for_api(self):
		"""
		Test case for authenticating agent for getting PAN card details
		"""
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'user'
							})
		self.assertEqual(resp.status_code, 201)
		resp = self.client.post('/v1/login/', {
				'username': 'testuser', 'password': 'testuser'
			})
		self.assertEqual(resp.status_code, 200)
		api_key = resp.json()['api_key']
		token = 'Token ' + api_key
		auth_headers = {
    		'HTTP_AUTHORIZATION': token,
		}
		path = str(settings.BASE_DIR) + '/panapp/testimg/pan_card_sample_2.jpg'
		headers = {'Authorization': token}
		with open(path) as fp:
			user_resp = self.client.post('/v1/user_data/', {'pan_image': fp}, **auth_headers)
		self.assertEqual(user_resp.status_code, 201)
		user_resp_id = user_resp.json()['id']

		r = self.client.get('/v1/next_data/', **auth_headers)
		self.assertEqual(r.status_code, 401)

	def test_next_data_api(self):
		"""
		Positive test case for testing API
		"""
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'user'
							})
		self.assertEqual(resp.status_code, 201)
		resp = self.client.post('/v1/login/', {
				'username': 'testuser', 'password': 'testuser'
			})
		self.assertEqual(resp.status_code, 200)
		api_key = resp.json()['api_key']
		token = 'Token ' + api_key
		auth_headers = {
    		'HTTP_AUTHORIZATION': token,
		}
		path = str(settings.BASE_DIR) + '/panapp/testimg/pan_card_sample_2.jpg'
		headers = {'Authorization': token}
		with open(path) as fp:
			user_resp = self.client.post('/v1/user_data/', {'pan_image': fp}, **auth_headers)
		self.assertEqual(user_resp.status_code, 201)
		user_resp_id = user_resp.json()['id']

		# Agent created
		resp = self.client.post('/v1/signup/', {
							'username': 'testagent', 'password': 'testagent',
							'entity_type': 'agent'
							})
		self.assertEqual(resp.status_code, 201)
		resp = self.client.post('/v1/login/', {
				'username': 'testagent', 'password': 'testagent'
			})
		self.assertEqual(resp.status_code, 200)
		agent_api_key = resp.json()['api_key']
		agent_token = 'Token ' + agent_api_key
		auth_headers = {
    		'HTTP_AUTHORIZATION': agent_token,
		}
		r = self.client.get('/v1/next_data/', **auth_headers)
		self.assertEqual(r.status_code, 200)









# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.conf import settings

# Create your tests here.
class SignupTestCase(TestCase):

	def test_signup(self):
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'user'
							}
						)
		self.assertEqual(resp.status_code, 201)

	def test_duplicate_signup(self):
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
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'agent'
							}
						)
		self.assertEqual(resp.status_code, 201)

	def test_duplicate_agent_signup(self):
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
		resp = self.client.post('/v1/signup/', {
							'username': 'testuser', 'password': 'testuser',
							'entity_type': 'agent'
							})
		self.assertEqual(resp.status_code, 201)
		resp = self.client.post('/v1/login/', {
				'username': 'testuser', 'password': 'testuser1'
			})
		self.assertEqual(resp.status_code, 401)


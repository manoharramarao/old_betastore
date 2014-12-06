#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
web2py_path = '../../..'
sys.path.append(os.path.realpath(web2py_path))
os.chdir(web2py_path)


import unittest
from gluon.globals import Request, Response, Session
from gluon.shell import exec_environment
from gluon.storage import Storage
import cStringIO

#execfile("applications/experiment/controllers/user.py", globals())

class TestUser(unittest.TestCase):
	def setUp(self):
		#self.env = Storage()
		self.request = Request({})
		self.request.env.request_method = 'POST'
		data = {'email': 'manohar2@gmail.com', 'password':'test1234'}
		self.body = cStringIO.StringIO()
		self.body.write(str(data))
		self.request.body = self.body
		self.request.post_vars['email'] = 'manohar2@gmail'
		self.request.post_vars['password'] = 'test1234'
		self.request.headers = dict()
		self.request.headers['Content-Type'] = 'application/json'
		self.auth = Auth(globals(), db)
		session.auth = self.auth
		self.controller = exec_environment('/home/manohar/work/bisineer_store/web2py/applications/experiment/controllers/user.py', request=self.request)

	def testLogin(self):
		self.request.env.request_method = 'POST'
		self.request.body = {'email': 'manohar2@gmail.com', 'password':'test1234'}
		self.request.post_vars['email'] = 'manohar2@gmail'
		self.request.post_vars['password'] = 'test1234'
		# self.request.headers = dict()
		# self.request.headers['Content-Type'] = 'application/json'
		self.controller.login()
		self.assertTrue(session.auth.is_logged_in())


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestUser))
unittest.TextTestRunner(verbosity=2).run(suite)
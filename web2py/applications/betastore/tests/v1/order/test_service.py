#!/usr/bin/python

import sys
import os

web2py_path = '../../../../../'
sys.path.append(web2py_path + "/gluon")
# sys.path.append(web2py_path + "/applications/betastore/models")
sys.path.append("/Volumes/Data/projects/personal/betastore/betastore/web2py/applications/betastore/models")
# sys.path.append(web2py_path + "/applications/betastore/modules")
sys.path.append("/Volumes/Data/projects/personal/betastore/betastore/web2py/applications/betastore/modules")
# sys.path.append(web2py_path + "/applications/betastore/controllers")
sys.path.append("/Volumes/Data/projects/personal/betastore/betastore/web2py/applications/betastore/controllers")

import unittest
from gluon.globals import Request, Response, Storage, Session
from gluon.shell import exec_environment
# from db import *
from db import test_db
from gluon.tools import Auth
from gluon import *
import cStringIO

# execfile(web2py_path + "/applications/betastore/controllers/user.py", globals())


class TestOrderService(unittest.TestCase):

    def setUp(self):
        self.request = Request({})
        self.request.env.request_method = 'POST'
        data = {'email': 'manohar2@gmail.com', 'password': 'test1234'}
        self.body = cStringIO.StringIO()
        self.body.write(str(data))
        self.request.body = self.body
        # self.request.post_vars['email'] = 'manohar2@gmail.com'
        # self.request.post_vars['password'] = 'test1234'
        self.request.headers = dict()
        self.request.headers['Content'] = "application/json"
        db = test_db
        self.auth = Auth(globals(), db)
        current.session.auth = self.auth
        self.controller = exec_environment(web2py_path + "/applications/betastore/controllers/user.py",
                                           request=self.request)

    def testLogin(self):
        self.request.env.request_method = "POST"
        self.request.body = {'email': 'manohar2@gmail.com', 'password': 'test1234'}
        # self.request.post_vars['email'] = 'manohar2@gmail.com'
        # self.request.post_vars['password'] = 'test1234'
        # self.request.headers = dict()
        # self.request.headers['Content'] = "application/json"
        self.controller.login()
        self.assertTrue(current.session.auth.is_logged_in())

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestOrderService))
unittest.TextTestRunner(verbosity=2).run(suite)
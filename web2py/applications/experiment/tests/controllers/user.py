#!/usr/bin/python
#found when running python web2py.py -S welcome -M -R testRunner.py 

import unittest
import cPickle as pickle
from gluon import * 
from gluon.contrib.test_helpers import form_postvars
from gluon import current

class UserController(unittest.TestCase):
    def __init__(self, p):
        global auth, session, request
        unittest.TestCase.__init__(self, p)
        self.session = pickle.dumps(current.session)
        current.request.application = 'experiment'
        current.request.controller = 'user'
        self.request = current.request

    def setUp(self):
        global response, session, request, auth
        current.session = pickle.loads(self.session)
        current.request = self.request
        auth = Auth(globals(), db)
        auth.define_tables()

    def _testRedirect(self, callable, url="/index"):
        try:
            resp = callable() # auth.register() creates & submits registration form
            self.fail("%s should raise an exception\n%s" % (
                callable.__name__,
                resp.errors))
        except HTTP, e:
            self.assertTrue(e.headers['Location'] == url,
                    "Wrong redirection url for unauthenticated user on %s() : %s (%s)" %
                    (callable.__name__, e.headers['Location'],url))
        else:
            self.fail("%s should raise an HTTP exception\n%s" % (
                callable.__name__,
                e))

    def emptyUserDB(self):
        db(db.auth_user.id>0).delete()
        db.commit()

    def testLogin(self):
        self.emptyUserDB()
        # Register a user in the db
        current.request.function='login'
        # resp = auth.register() # get the form
        current.request.post_vars['email'] = 'manohar2@gmail'
        current.request.post_vars['password'] = 'test1234'

        # fields = {
        #     "email": "essai@gmail.com",
        #     "first_name": "e_first",
        #     "last_name": "e_last",
        #     "password" : "blob",
        #     "password_two": "blob",
        #     "_formkey": resp.formkey,
        #     }

        # vars = {}
        # action='create'
        # for field_name in fields:
        #     vars[field_name] = fields[field_name]
        #     if action == "create":
        #         vars["_formname"] = tablename + "_" + action
        #     elif action == "update":
        #         vars["_formname"] = tablename + "_" + str(record_id)
        #         vars["id"] = record_id
        #     elif action == "delete":
        #         vars["_formname"] = tablename + "_" + str(record_id)
        #         vars["id"] = record_id
        #         vars["delete_this_record"] = True
        #     elif action:
        #         vars["_formname"] = action
        # self._testRedirect(auth.register,'/welcome/default/index')
        # current.request.controller.login()
        self.assertTrue(auth.is_logged_in())
        # self.assertEquals(auth.user.first_name, 'e_first')
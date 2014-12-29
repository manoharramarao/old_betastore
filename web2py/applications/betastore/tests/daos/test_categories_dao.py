__author__ = 'manohar'


import sys
from gluon.globals import *
from gluon import *

import unittest
from daos import category_dao

if False:
    db = current.db


class TestCategoriesDao(unittest.TestCase):
    """
    To run this, from web2py root, execute this command
    python web2py.py -S betastore -M -R applications/betastore/tests/daos/test_categories_dao.py
    """
    def setUp(self):
        db(db.bis_category.id > 0).delete()
        db.bis_category.insert(name="pumps", description="pumps description", catalogs="bisineer_online", children=["Submircible Pumps", "Booster Pumps"], ancestors=[])
        db.bis_category.insert(name="Submircible Pumps", description="Submircible Pumps description", catalogs="bisineer_online", ancestors="Pumps")
        db.bis_category.insert(name="Booster Pumps", description="Booster description", catalogs="bisineer_online", ancestors="Pumps", children=["Twin Booster", "Thrine Booster"])
        db.commit()
        request = Request({})
        # self.controller = exec_environment('applications/myapp/controllers/default.py', request=request)

    def test_get_first_level_categories(self):
        categories = category_dao.get_first_level_categories()
        print str(categories)
        self.assertIsNotNone(categories)
        self.assertEquals(1, len(categories))

    def tearDown(self):
        db(db.bis_category.id>0).delete()

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestCategoriesDao))
unittest.TextTestRunner(verbosity=2).run(suite)
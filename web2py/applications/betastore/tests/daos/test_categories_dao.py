__author__ = 'manohar'


import sys
from gluon.globals import *
from gluon import *

import unittest
from daos import category_dao

if False:
    test_db = current.db

print test_db
db = test_db


class TestCategoriesDao(unittest.TestCase):
    """
    To run this, from web2py root, execute this command
    python web2py.py -S betastore -M -R applications/betastore/tests/daos/test_categories_dao.py

    """
    def setUp(self):
        db(db.bis_category.id > 0).delete()
        db.import_from_csv_file(open('./applications/betastore/tests/data/daos/test_categories_dao.csv', 'r'))
        db.commit()
        request = Request({})
        # self.controller = exec_environment('applications/myapp/controllers/default.py', request=request)

    def test_get_first_level_categories(self):
        categories = category_dao.get_first_level_categories()
        self.assertIsNotNone(categories)
        self.assertEquals(1, len(categories))

    def test_get_child_categories(self):
        categories = category_dao.get_category("Pumps")
        # print "categories are "
        # print categories
        for category in categories:
            print category
        self.assertIsNotNone(categories)
        self.assertEqual(1, len(categories))
        for category in categories:
            self.assertTrue("Booster Pumps" in category.children)
            self.assertTrue("Hydro Booster Pumps" in category.children)
            self.assertTrue("Submercible Pumps" in category.children)

    def tearDown(self):
        pass
        # db(db.bis_category.id > 0).delete()

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestCategoriesDao))
unittest.TextTestRunner(verbosity=2).run(suite)
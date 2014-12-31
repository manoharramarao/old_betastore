__author__ = 'manohar'


import sys
from gluon.globals import *
from gluon import *
from gluon.dal import DAL
from gluon.dal import Row
from gluon.dal import Rows

import unittest
from daos import category_dao

if False:
    db = current.db

# print test_db
# db = test_db


class TestCategoriesDao(unittest.TestCase):
    """
    To run this, from web2py root, execute this command
    python web2py.py -S betastore -M -R applications/betastore/tests/daos/test_negative_categories_dao.py

    """
    def setUp(self):
        db(db.bis_category.id > 0).delete()
        # db.import_from_csv_file(open('./applications/betastore/tests/data/daos/test_categories_dao.csv', 'r'))
        db.commit()
        request = Request({})
        # self.controller = exec_environment('applications/myapp/controllers/default.py', request=request)

    def test_negative_first_level_categories(self):
        categories = category_dao.get_root_categories()
        self.assertEqual(0, len(categories))
        self.assertEqual(Rows, type(categories))

    def test_negative_get_category(self):
        category = category_dao.get_category("category code that is not present in test data")
        self.assertIsNone(category)
        self.assertEqual(Row, type(category))

    def test_negative_get_child_categories(self):
        categories = category_dao.get_child_categories("category code that is not present in test data")
        self.assertEqual(0, len(categories))

    def tearDown(self):
        pass
        # db(db.bis_category.id > 0).delete()

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestCategoriesDao))
unittest.TextTestRunner(verbosity=2).run(suite)
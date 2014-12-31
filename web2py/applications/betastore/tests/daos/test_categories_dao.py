__author__ = 'manohar'


import sys
from gluon.globals import *
from gluon import *
from gluon.dal import DAL
from gluon.dal import Row

import unittest
from daos import category_dao

if False:
    db = current.db

# print test_db
# db = test_db


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

    def test_get_root_categories(self):
        categories = category_dao.get_root_categories()
        self.assertIsNotNone(categories)
        self.assertEquals(1, len(categories))

    def test_get_category(self):
        category = category_dao.get_category("Pumps")
        # print "categories are "
        # print categories
        self.assertIsNotNone(category)
        self.assertTrue("Booster Pumps" in category.children)
        self.assertTrue("Hydro Booster Pumps" in category.children)
        self.assertTrue("Submercible Pumps" in category.children)
        self.assertEqual("Pumps", category.code)
        # self.assertRaises(AttributeError, callableObj=category.__getitem__("id"))
        self.assertNotIn("id", category.keys())
        self.assertNotIn("name", category.keys())
        self.assertNotIn("catalogs", category.keys())

    def test_get_child_categories(self):
        categories = category_dao.get_child_categories("Pumps")
        self.assertIsNotNone(categories)
        self.assertEqual(3, len(categories))
        category_codes = []
        for category in categories:
            category_codes.append(category.code)
        self.assertEqual(3, len(category_codes))
        self.assertTrue("Booster Pumps" in category_codes)
        self.assertTrue("Hydro Booster Pumps" in category_codes)
        self.assertTrue("Submercible Pumps" in category_codes)

    def tearDown(self):
        pass
        # db(db.bis_category.id > 0).delete()

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestCategoriesDao))
unittest.TextTestRunner(verbosity=2).run(suite)
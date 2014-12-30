__author__ = 'manohar'


import sys
from gluon.globals import *
from gluon import *

import unittest
from daos import product_dao

if False:
    test_db = current.db

print test_db
db = test_db


class TestProductDao(unittest.TestCase):
    """
    To run this, from web2py root, execute this command
    python web2py.py -S betastore -M -R applications/betastore/tests/daos/test_product_dao.py

    """
    def setUp(self):
        db(db.bis_product.id > 0).delete()
        db.import_from_csv_file(open('./applications/betastore/tests/data/daos/test_product_dao.csv', 'r'))
        db.commit()
        request = Request({})
        # self.controller = exec_environment('applications/myapp/controllers/default.py', request=request)

    def test_get_categories(self):
        products = product_dao.get_categories("05HP")
        self.assertIsNotNone(products)
        self.assertEqual(1, len(products))
        for product in products:
            self.assertTrue("Submercible Pumps" in product.categories)

    def tearDown(self):
        db(db.bis_product.id > 0).delete()

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestProductDao))
unittest.TextTestRunner(verbosity=2).run(suite)
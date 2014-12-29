__author__ = 'manohar'

from gluon import *
from gluon.storage import Storage
from daos import category_dao
from daos import product_dao
from daos import cart_order_dao
from daos import line_item_dao
from daos import auth_membership_dao
from daos import price_dao
from daos import price_type_dao
from daos import auth_group_dao
from v1.models.cart_order import Order



if False:
    from gluon import *
    request = current.request
    response = current.response
    session = current.response
    cache = current.cache
    db = current.db
    logger = current.logger
    auth = current.auth


class CatalogServices(object):
    """
    Does everything related to catalog, category and products
    """

    def get_categories(self, product, category):
        """
        1. Returns just the names of all categories that product belong to irrespective of the depth of the category.
        2. If category parameter is passed, then it returns all child categories of depth 1
        3. If both args are none, then returns list of level 1 categories
        :param product: db.bis_product.code
        :param category: db.bis_category.code
        :return: db.bis_category.code (which is actually category name)
        """
        categories = Storage()
        if product is None and category is None:
            categories = category_dao.get_first_level_categories()
        elif category is None:
            categories = category_dao.get_child_categories(category)
        elif product is None:
            categories = product_dao.get_categories(product)
        return categories
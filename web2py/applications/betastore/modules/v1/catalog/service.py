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

    def get_root_categories(self):
        return category_dao.get_root_categories()

    def get_child_categories(self, category=None):
        return category_dao.get_child_categories(category)
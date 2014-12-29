__author__ = 'manohar'

from gluon.storage import Storage
from gluon import *
from daos import auth_user_dao
import uuid


def get_categories(product, category):
    """
    Returns categories of a product
    Returns child categories of a category. (depth = 1)
    :param product: db.bis_product.code
    :param category: db.bis_category.code
    :return: db.bis_category.code (which is same as db.bis_category.name)
    """
    pass


def get_first_level_categories():
    """
    Returns top most categories

    :return: db.bis_category.code (same as name)
    """
    return current.db(current.db.bis_category.ancestors == []).select(current.db.bis_category.id, current.db.bis_category.code).as_dict()


def get_child_categories(category_code):
    """
    Returns child categories

    :param category_code: db.bis_category.code
    :return: list of db.bis_category.code
    """
    return current.db(current.db.bis_category.code > category_code & current.db.bis_category.children != []).select(
        "children", projection=True).as_dict()
__author__ = 'manohar'

from gluon.storage import Storage
from gluon import *
from daos import auth_user_dao
import uuid

unwanted_attributes = ['name', 'catalogs']


def _clean(categories):
    """
    clean the categories dictionary and remove unwanted and secure attributes before it leaves dao layer.

    :param categories: db.bis_category array
    :return: db.bis_category array
    """
    # TODO need to optimize this
    if categories is not None:
        for category in categories:
            for key in unwanted_attributes:
                if key in category.keys():
                    del category[key]
    return categories


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

    :return: [{bis_category.display_name, bis_category.code}]
    """
    return _clean(current.db(current.db.bis_category.ancestors == []).select(current.db.bis_category.display_name,
                                                                             current.db.bis_category.code,
                                                                             current.db.bis_category.name,
                                                                             current.db.bis_category.catalogs))


def get_child_categories(category_code):
    """
    Returns child categories

    :param category_code: db.bis_category.code
    :return: [{bis_category.children, bis_category.catalogs, bis_category.code}]
    """
    return _clean(current.db(current.db.bis_category.code == category_code).select(current.db.bis_category.children,
                                                                                   current.db.bis_category.catalogs,
                                                                                   current.db.bis_category.code))
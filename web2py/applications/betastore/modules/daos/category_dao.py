__author__ = 'manohar'

from gluon.storage import Storage
from gluon import *
from gluon.dal import Row
from gluon.dal import Rows
from daos import auth_user_dao
import uuid

unwanted_attributes = ['id', 'name', 'catalogs']


def _clean(categories):
    """
    clean the categories dictionary and remove unwanted and secure attributes before it leaves dao layer.

    :param categories: db.bis_category Rows or db.bis_category Row
    :return: db.bis_category array
    """
    # TODO need to optimize this
    if categories is not None and isinstance(categories, Rows) and len(categories) > 0:
        for category in categories:
            for key in unwanted_attributes:
                if key in category.keys():
                    del category[key]
    elif categories is not None and isinstance(categories, Row):
        for key in unwanted_attributes:
            if key in categories.keys():
                del categories[key]
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


def get_root_categories():
    """
    Returns top most categories

    :return: [{bis_category}] or Rows() of length 0
    """
    return _clean(current.db(current.db.bis_category.ancestors == []).select(current.db.bis_category.ALL))


def get_child_categories(parent_category_code):
    """
    Returns details of all children

    :param parent_category_code: db.bis_category.code
    :return: [{db.bis_category}] or Rows() of length 0
    """
    parent_category_details = current.db(current.db.bis_category.code ==
                                         parent_category_code).select(current.db.bis_category.ALL).first()
    child_categories = Rows()
    if parent_category_details is not None:
        for child_category_code in parent_category_details.children:
            child_categories.records.append(_clean(current.db(current.db.bis_category.code == child_category_code).
                                                   select(current.db.bis_category.ALL).first()))
    return child_categories


def get_category(category_code):
    """
    Returns child categories

    :param category_code: db.bis_category.code
    :return: {bis_category} or None
    """
    return _clean(current.db(current.db.bis_category.code == category_code).select(current.db.bis_category.ALL).first())
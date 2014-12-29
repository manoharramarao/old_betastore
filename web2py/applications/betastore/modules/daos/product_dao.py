__author__ = 'manohar'
from gluon import *

def get_categories(product_code):
    """
    Returns list of categories that product belongs to

    :param product: db.bis_product_code
    :return: list of db.bis_product.categories
    """
    return current.db(current.db.bis_product.code == product_code).select("categories", projection=True).as_dict()
__author__ = 'manohar'
from gluon import *

unwanted_attributes = ['id', 'catalogs', 'unit_price', 'on_sale', 'tax_rate', 'volume', 'weight']


def _clean(products):
    """
    clean the categories dictionary and remove unwanted and secure attributes before it leaves dao layer.

    :param categories: db.bis_category array
    :return: db.bis_category array
    """
    # TODO need to optimize this
    if products is not None:
        for product in products:
            for key in unwanted_attributes:
                if key in product.keys():
                    del product[key]
    return products

def get_categories(product_code):
    """
    Returns list of categories that product belongs to

    :param product: db.bis_product_code
    :return: [{bis_product}]
    """
    return _clean(current.db(current.db.bis_product.code == product_code).select(current.db.bis_product.ALL))
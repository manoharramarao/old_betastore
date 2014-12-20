from gluon.storage import Storage
from gluon import *


def get_price(product_code, group_code, price_type_code):
    current.logger.debug("product_code is " + str(product_code))
    current.logger.debug("group_code is " + str(group_code))
    current.logger.debug("price_type_code is " + str(price_type_code))
    row = current.db((current.db.bis_price.product_code == product_code) & (current.db.bis_price.user_group_code == group_code) & (current.db.bis_price.price_type_code == price_type_code)).select().first()
    if row is not None:
        row = Storage(row.as_dict())
    current.logger.debug("row = " + str(row))
    return row


from gluon import *

logger = current.logger


def save_address(address):
    pass


def get_shipping_addresses(user):
    db = current.db
    logger.debug("inside get_shipping_addresses()")
    logger.debug("user id is " + str(user.id))
    return db((db.bis_address.user_id == user.id)).select()


def get_shipping_address(order_id):
    pass


def delete_address(address):
    pass


def get_address(address_id):
    pass


def get_address(address_name):
    pass
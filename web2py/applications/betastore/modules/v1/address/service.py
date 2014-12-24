__author__ = 'manohar'

from gluon import *
from gluon.storage import Storage
from daos import address_dao
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


class AddressService(object):
    """
    Does everything related to address services.
    1. gets addresses for a user
    2. save new address for a user
    3. save new shipping address for an order
    """

    def get_addresses(self, user):
        """
        Returns all shipping addresses of the user

        :param user: db.bis_auth_user - user for which shipping addresses are fetched
        :return: db.bis_address array
        """
        pass

    def save_address(self, address):
        """
        if found updates the address or else creates new one and saves it to DB for the logged in user.
        Returns the same address

        :param user: db.bis_user - user for which address is saved
        :param address: db.bis_address - address to save to DB
        :return: db.bis_address - newly created address
        """
        if auth.is_logged_in():
            address.user_code = current.session.auth.user.code
        address_dao.save_address(address)

    def save_new_shipping_address(self, address, order):
        """
        associates new address as shipping address for the order given

        :param address: db.bis_address
        :param order: db.bis_cart_order
        :return: db.bis_cart_order
        """
        pass
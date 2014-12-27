__author__ = 'manohar'

from gluon import *
from gluon.storage import Storage
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


class OrderService(object):
    """
    Does everything related to cart and order
    """

    allowed_line_item_attributes = ['id',
                                    'order_code',
                                    'product_code',
                                    'quantity',
                                    'total_amount',
                                    'discount',
                                    'tax',
                                    'created_on',
                                    'line_item',
                                    'description_short',
                                    'name']
    """ db.bis_line_item attributes that are allowed to client side"""

    def flush_cart(self, cart):
        """
        Flush server's cart from the client's cart and persists data in DB

        :param cart: db.bis_cart_order - cart from client.
        :return: cart after flushing server's cart
        """
        current.logger.debug("inside flush_cart")
        user = current.session.auth.user
        server_cart = cart_order_dao.get_cart()
        line_item_dao.delete_line_items(server_cart)
        server_cart.line_items = []
        line_items = self._merge_line_items_with_same_product(cart.line_items)
        server_cart = self._save_line_items(line_items, server_cart)
        server_cart = cart_order_dao.save(server_cart)
        return server_cart

    def save_comments(self, cart):
        """
        Saves comments of the order to bis_cart_order table in DB

        :param cart: db.bis_cart_order
        :return: cart after saving the comments
        """
        pass

    def _merge_line_items_with_same_product(self, line_items):
        """
        Line items with duplicate products are merged

        :param line_items: db.bis_line_item
        :return db.bis_line_item: array of line_items after merged
        """
        new_line_items = {}
        for line_item in line_items:
            line_item = Storage(line_item)
            if str(line_item.product_code) in new_line_items:
                new_line_items[str(line_item.product_code)].quantity += line_item.quantity
            else:
                new_line_items[str(line_item.product_code)] = line_item
        return new_line_items.values()

    def _save_line_items(self, line_items, order):
        """
        associates line_item with order and vice versa and saves it to db

        :param line_items: db.bis_line_item - array
        :param order: db.bis_cart_order
        :return order: db.bis_cart_order after the association
        """
        line_items = self._clean_line_items(line_items)
        for line_item in line_items:
            line_item = Storage(line_item)
            line_item.order_code = order.code
            line_item = line_item_dao.save(line_item)
            order.line_items.append(line_item)
        return order

    def _clean_line_items(self, line_items):
        """
        Removes unwanted attributes in db.bis_line_item before sending it to client

        :param line_items: db.bis_line_item array
        :return new_line_items: db.bis_line_item array after removing unwanted attributes from each line item
        """
        new_line_items = []
        for line_item in line_items:
            for key in line_item.keys():
                if key not in self.allowed_line_item_attributes:
                    del line_item[key]
            new_line_items.append(line_item)
        return new_line_items
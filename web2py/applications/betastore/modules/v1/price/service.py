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


class PriceService(object):
    """
    Does everything related to prices by line_item, order, product. The state of this object is maintained by these
    three.
    """

    def flush_line_item_price(self, line_item):
        """
        Returns line_item after populating prices

        :return line_item: returns db.bis_line_item after populating prices and saving it to DB
        """
        # TODO define priority decision tree to decide which price to pick when user belongs to multiple user groups
        if auth.user_groups is not None:
            for user_group in auth.user_groups:
                if user_group.lower() == "default":
                    default_user_group = user_group
        else:
            default_user_group = "default"
        price_type_code = "default"  # as of now, picking default price
        price_row = price_dao.get_price(product_code=line_item.product_code, group_code=default_user_group,
                                        price_type_code=price_type_code)
        return price_row.amount

    def flush_order_price(self, order):
        """
        Returns db.bis_cart_order after populating and saving prices to DB

        :param db.bis_cart_order: db.bis_cart_order
        :return db.bis_cart_order: returns db.bis_bis_cart_order after populating prices and saving it to DB
        """
        current.logger.debug("inside flush_order_price")
        # order = Order(order=order)
        current.logger.debug("line items are " + str(order.line_items))
        total_amount = 0
        line_item_with_prices = []
        for line_item in order.line_items:
            line_item = Storage(line_item)
            line_item = self.get_line_item_price(line_item)
            total_amount += line_item.total_amount
            line_item_dao.save(line_item)
            line_item_with_prices.append(line_item)
        order.total_amount = round(total_amount, 2)
        order.line_items = line_item_with_prices
        cart_order_dao.save(order)
        return order

    def get_product_price(self, product):
        """
        Returns net amount(without tax) of the product. This doesn't save prices to DB

        :param product: db.bis_product
        :return: returns net amount(without tax) of the product. This doesn't save prices to DB
        """
        pass

    def get_line_item_price(self, line_item):
        """
        Returns db.bis_line_item with prices in it. This doesn't save prices to DB

        :param line_item: db.bis_line_item
        :return db.bis_line_item: line item with prices (with out tax). This doesn't save prices to DB
        """
        current.logger.debug("inside get_line_item_price")
        current.logger.debug("input line item is " + str(line_item))
        if current.session.auth is not None and current.session.auth.user_groups is not None \
                and current.session.auth.user_groups:
            print "user_groups is " + str(current.session.auth.user_groups)
            for user_group in current.session.auth.user_groups:
                user_group = auth_group_dao.get_group_role(user_group)
                if user_group.lower() == "default":
                    default_user_group = user_group
        else:
            default_user_group = "default"

        price_type_code = "default"  # as of now, picking default price
        price_row = price_dao.get_price(product_code=line_item.product_code, group_code=default_user_group,
                                        price_type_code=price_type_code)
        line_item.unit_price = price_row.amount
        line_item.total_amount = round(price_row.amount * line_item.quantity, 2)
        return line_item

    def get_order_price(self, order):
        """
        Returns db.bis_cart_order after populating prices in it

        :param order: db.bis_cart_order
        :return order: db.bis_cart_order after populating prices in it.
        """
        pass
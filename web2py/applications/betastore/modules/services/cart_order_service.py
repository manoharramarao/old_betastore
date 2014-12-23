from gluon import *
from gluon.storage import Storage
from daos import cart_order_dao
from daos import line_item_dao
from daos import auth_membership_dao
from daos import price_dao
from daos import price_type_dao
from daos import auth_group_dao
from v1.price.service import PriceService

# logger = current.logger
# db = current.db
if False:
    from gluon import *
    request = current.request
    response = current.response
    session = current.response
    cache = current.cache
    db = current.db
    auth = current.auth
    logger = current.logger


def get_cart():
    pass


def flush_cart(cart):
    current.logger.debug("inside cart_order_services.flush_cart")
    current.logger.debug("cart = " + str(cart))
    # get user
    user = current.session.auth.user

    # get cart for user. If exists, make it empty
    server_cart = cart_order_dao.get_cart()
    line_item_dao.delete_line_items(server_cart)
    server_cart.line_items = []

    #TODO once the problem in line_item_dao.py is fixed, please remove the below call
    # merge duplicate line items
    line_items = _merge_line_items_with_same_product(cart.line_items)
    #line_items = cart.line_items

    server_cart = _save_line_items(line_items, server_cart)
    server_cart = cart_order_dao.save(server_cart)
    return server_cart


def _flush_cart_with_prices(cart):
    server_cart = flush_cart(cart)
    server_cart.total_amount = cart.total_amount
    cart_order_dao.save(server_cart)
    return server_cart


# def get_prices(cart):
#     current.logger.debug("inside get_prices")
#     price_type_code = price_type_dao.get_default_price_code()
#
#     # get groups for ths logged in user
#     if current.session.auth.user is not None:
#         memberships = auth_membership_dao.get_memberships(current.session.auth.user.id)
#         memberships = list(memberships.values())
#     # assuming that user belongs to only one group as of now
#     # either by the time we reach here, we should be knowing the user group for this session
#     # or just default to some user group or build a login on how to select which user group
#     # or build a mechanism which user group takes priority over which one. so that prices are pulled
#     # for that specific user group.
#     if memberships:
#         for membership in memberships:
#             membership = Storage(membership)
#             current.logger.debug("groupd id is " + str(membership.group_id))
#             cart = _get_prices(cart, membership, price_type_code)
#     current.logger.debug("cart after prices, before flushing " + str(cart))
#     _flush_cart_with_prices(cart)
#     return cart


def flush_prices(cart):
    """
    Returns cart_order + line_item filled with prices. Cart will have line_items inside it.
    :param cart: db.bis_cart_order + db.bis_line_item without prices
    :return cart: db.bis_cart_order + db.bis_line_item filled with prices
    """
    current.logger.debug("inside get_prices")
    current.logger.debug("input cart is " + str(cart))
    price_service = PriceService()
    cart = price_service.flush_order_price(cart)
    return cart


def _get_prices(cart, membership, price_type_code):
    current.logger.debug("_get_prices")
    line_items_with_price = []
    cart.total_amount = 0
    for line_item in cart.line_items:
        # right now we are keeping it to getting the default price type
        line_item = Storage(line_item)
        price = price_dao.get_price(line_item['product_code'], auth_group_dao.get_group_code(membership.group_id), price_type_code)
        if price is not None:
            line_item.unit_price = price.amount
            line_item.total_amount = line_item.quantity * price.amount
            cart.total_amount += line_item.total_amount
            current.logger.debug("line_item after populating price is " + str(line_item))
            line_items_with_price.append(line_item)
        else:
            raise HTTP('500', "couldn't fetch prices. Please try later")
    cart.line_items = line_items_with_price
    return cart


def save_order(order):
    pass


def save_line_item(line_item):
    pass


def delete_cart(cart):
    pass


def delete_order(order):
    pass


def delete_line_items(line_items):
    pass


def _save_line_items(line_items, order):
    line_items = _clean_line_items(line_items)
    for line_item in line_items:
        line_item = Storage(line_item)
        line_item.order_code = order.code
        line_item = line_item_dao.save(line_item)
        order.line_items.append(line_item.id)
    return order


def _merge_line_items_with_same_product(line_items):
    new_line_items = {}
    for line_item in line_items:
        line_item = Storage(line_item)
        if str(line_item.product_code) in new_line_items:
            new_line_items[str(line_item.product_code)].quantity += line_item.quantity
        else:
            new_line_items[str(line_item.product_code)] = line_item
    return new_line_items.values()


def _clean_line_items(line_items):
    line_item_attributes = ['id', 'order_code', 'product_code', 'quantity', 'total_amount', 'discount', 'tax', 'created_on', 'line_item', 'description_short', 'name']
    new_line_items = []
    for line_item in line_items:
        for key in line_item.keys():
            if key not in line_item_attributes:
                del line_item[key]
        new_line_items.append(line_item)
    return new_line_items
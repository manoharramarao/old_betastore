import traceback

import gluon.contrib.simplejson as json
from gluon.storage import Storage
from services import cart_order_service
from v1.order.service import OrderService

#import jsonpickle


if False:
    from gluon import *
    request = current.request
    response = current.response
    session = current.response
    cache = current.cache
    db = current.db
    auth = current.auth
    logger = current.logger


@auth.requires_login()
def flush_cart():
    """
    if cart exists, it will flush with new cart sent to this method,
    else creates new cart with the input.
    This is called everytime new item is added to the cart
    """
    order_service = OrderService()
    try:
        cart = Storage(json.loads(request.body.read()))
        logger.debug("new cart sent is " + str(cart))
        order_service.flush_cart(cart)
    except Exception, e:
        logger.error(str(e))
        traceback.print_exc()
        raise HTTP(500, 'Ouch!! something went wrong. Please try again')
    return


@auth.requires_login()
def get_cart():
    user = session.auth.user
    order = Storage()
    cart = Storage()
    order = db((db.bis_cart_order.user_code == user.code) & (db.bis_cart_order.status == "cart")).select().first()
    cart.line_items = []
    if order is not None:
        cart.line_items = db((db.bis_line_item.order_code == order.code)).select(db.bis_line_item.id, db.bis_line_item.product_code, db.bis_line_item.quantity,
            db.bis_line_item.code, db.bis_line_item.description_short, db.bis_line_item.name, projection=True)
    for line_item in cart.line_items:
        logger.debug("line_item is ====== " + str(line_item))
        #line_item.code = db.bis_line_item.code.represent(line_item.code,line_item)
        logger.debug("line_item.code is ==============" + str(line_item.code))
        logger.debug("line_item based on code is ====================" + str(db(db.bis_line_item.code == line_item.code).select().as_dict()))
    return cart


def get_prices():
    """
    returns prices for all line items
    """
    logger.debug("inside get_prices")
    cart = Storage(json.loads(request.body.read()))
    logger.debug("cart before getting prices " + str(cart))
    cart_order_service.flush_prices(cart)
    logger.debug("cart after getting prices " + str(cart))
    return cart

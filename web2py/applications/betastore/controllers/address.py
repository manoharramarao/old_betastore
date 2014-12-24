__author__ = 'manohar'

import traceback

import gluon.contrib.simplejson as json
from gluon.storage import Storage
from services import cart_order_service
from v1.order.service import OrderService
from v1.price.service import PriceService
from v1.address.service import AddressService
import traceback

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


def save_address():
    """
    insert/update the address into the DB

    :param address: db.bis_address
    :return: db.bis_address
    """
    logger.debug("inside save_address")
    try:
        input_json = request.body.read()
        address = Storage(json.loads(input_json))
        address_service = AddressService()
        if auth.is_logged_in():
            address = address_service.save_address(address, auth.user)
    except Exception, e:
        logger.error(str(e))
        traceback.print_exc()
        raise HTTP(500, "Ouch!! something went wrong. Please try again")
    return address


def get_addresses():
    """
    returns all addresses of the logged in user. If user is anonymous, then return None

    :return: db.bis_address array
    """
    logger.debug("inside get_addresses")
    try:
        address_service = AddressService()
        if auth.is_logged_in():
            addresses = address_service.get_addresses(auth.user)
        else:
            addresses = None
    except Exception, e:
        logger.error(str(e))
        traceback.print_exc()
        raise HTTP(500, "Ouch!! something went wrong. Please try again")
    logger.debug("addresses before returning " + str(addresses.as_dict()))
    return addresses.as_dict()



def save_shipping_address(address):
    pass

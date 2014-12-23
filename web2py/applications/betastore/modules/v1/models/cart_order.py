__author__ = 'manohar'

from gluon import *
import gluon.contrib.simplejson as json
import gluon.storage as storage

if False:
    from gluon import *
    request = current.request
    response = current.response
    session = current.response
    cache = current.cache
    db = current.db
    auth = current.auth
    logger = current.logger


class Order(object):

    def __init__(self, input_json=None, order=None):
        """
        constructor
        :param input_json: json input for order
        :param order: gluon.storage input for order
        :return:
        """
        if input_json is not None:
            order = storage(json.loads(input_json))
        self.id = order.id if order.id is not None else None
        self.user_code = order.user_code if order.user_code is not None else None
        self.billing_code = order.billing_code if order.billing_code is not None else None
        self.shipping_code = order.shipping_code if order.shipping_code is not None else None
        self.created_on = order.created_on if order.created_on is not None else None
        self.status = order.status if order.status is not None else None
        self.product_cost = order.product_cost if order.product_cost is not None else None
        self.total_amount = order.total_amount if order.total_amount is not None else None
        self.discount = order.discount if order.discount is not None else None
        self.tax = order.tax if order.tax is not None else None
        self.shipping_cost = order.shipping_cost if order.shipping_cost is not None else None
        self.amount_due = order.amount_due if order.amount_due is not None else None
        self.amount_paid = order.amount_paid if order.amount_paid is not None else None
        self.line_items = order.line_items if order.line_items is not None else None
        self.code = order.code if order.code is not None else None

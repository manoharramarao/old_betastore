__author__ = 'manohar'

import gluon.contrib.simplejson as json
import gluon.storage as storage


class LineItem(object):
    """
    model equal to db.bis_line_item
    """

    def __init__(self, input_json, line_item):
        """

        :param input_json:
        :param line_item:
        :return:
        """
        if input_json is not None:
            line_item = storage(json.loads(input_json))
        self.product_code = line_item.product_code
        self.quantity = line_item.quantity if line_item.quantity is not None else None
        self.unit_price = line_item.unit_price if line_item.unit_price is not None else None
        self.total_amount = line_item.total_amount if line_item.total_amount is not None else None
        self.discount = line_item.discount if line_item.discount is not None else None
        self.tax = line_item.tax if line_item.tax is not None else None
        self.created_on = line_item.created_on if line_item.created_on is not None else None
        self.description_short = line_item.description_short if line_item.description_short is not None else None
        self.name = line_item.name if line_item.name is not None else None
        self.code = line_item.code if line_item.code is not None else None

from gluon import *
from gluon.storage import Storage
from daos import cart_order_dao
from daos import line_item_dao

def get_prices(products):
	"""
	return line_items populating prices
	"""
	input_json = request.body.read()
	products = Storage(input_json)
	for product in products:
		logger.debug("product id is " + product.id)
		logger.debug("quantity is " + product.quantity)
	return
	
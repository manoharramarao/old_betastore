from gluon import *
from gluon.storage import Storage
from daos import cart_order_dao
from daos import line_item_dao

# logger = current.logger
# db = current.db

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
	# merge duplicates
	line_items = merge_line_items_with_same_product(cart.line_items)
	#line_items = cart.line_items

	for line_item in line_items:
		line_item = Storage(line_item)
		line_item.order_id = server_cart.id
		current.logger.debug("line_item before calling save " + str(line_item))
		line_item = line_item_dao.save(line_item)
		server_cart.line_items.append(line_item.id)
	server_cart = cart_order_dao.save(server_cart)
	return server_cart

def merge_line_items_with_same_product(line_items):
	new_line_items = {}
	for line_item in line_items:
		line_item = Storage(line_item)
		if str(line_item.product_id) in new_line_items:
			new_line_items[str(line_item.product_id)].quantity += line_item.quantity
		else:
			new_line_items[str(line_item.product_id)] = line_item
	return new_line_items.values()

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


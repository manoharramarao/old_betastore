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
	# merge duplicate line items
	line_items = _merge_line_items_with_same_product(cart.line_items)
	#line_items = cart.line_items

	# for line_item in line_items:
	# 	line_item = Storage(line_item)
	# 	line_item.order_id = server_cart.id
	# 	current.logger.debug("line_item before calling save " + str(line_item))
	# 	line_item = line_item_dao.save(line_item)
	# 	server_cart.line_items.append(line_item.id)
	# save line items to DB and update order.line_items array to hold IDs
	server_cart = _save_line_items(line_items, server_cart)
	server_cart = cart_order_dao.save(server_cart)
	return server_cart

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
		line_item.order_id = order.id
		line_item = line_item_dao.save(line_item)
		order.line_items.append(line_item.id)
	return order


def _merge_line_items_with_same_product(line_items):
	new_line_items = {}
	for line_item in line_items:
		line_item = Storage(line_item)
		if str(line_item.product_id) in new_line_items:
			new_line_items[str(line_item.product_id)].quantity += line_item.quantity
		else:
			new_line_items[str(line_item.product_id)] = line_item
	return new_line_items.values()

def _clean_line_items(line_items):
	line_item_attributes = ['id', 'order_id', 'product_id', 'quantity', 'total_amount', 'discount', 'tax', 'created_on', 'line_item']
	new_line_items = []
	for line_item in line_items:
		for key in line_item.keys():
			if key not in line_item_attributes:
				del line_item[key]
		new_line_items.append(line_item)
	return new_line_items
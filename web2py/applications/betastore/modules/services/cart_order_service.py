from gluon import *
from daos import cart_order_dao
from daos import line_item_dao

logger = current.logger
db = current.db

def get_cart():
	pass

def flush_cart(cart):
	# get user
	user = current.session.auth.user
	
	# get cart for user. If exists, make it empty
	server_cart = cart_order_dao.get_empty_cart()
	order_id = server_cart.id

	# delete line items from the cart
	line_item_dao.delete_line_items(server_cart)
	
	# insert line items into server_cart
	cart.line_items = line_item_dao.insert(server_cart, cart.line_items)
	
	# update new line items IDs in the order/cart
	cart_order_dao.update_line_item_ids(server_cart)

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


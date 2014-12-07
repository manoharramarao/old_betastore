from gluon import *
from gluon.storage import Storage
from daos import cart_order_dao
from daos import line_item_dao
from daos import auth_membership
from daos import price_dao
from daos import price_type_dao

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

	server_cart = _save_line_items(line_items, server_cart)
	server_cart = cart_order_dao.save(server_cart)
	return server_cart

def _flush_cart_with_prices(cart):
	server_cart = flush_cart(cart)
	server_cart.total_amount = cart.total_amount
	cart_order_dao.save(server_cart)
	return server_cart


def get_prices(cart):
	current.logger.debug("inside get_prices")
	price_type_id = price_type_dao.get_default_price_id()

	# get groups for ths logged in user
	if current.session.auth.user is not None:
		memberships = auth_membership.get_memberships(current.session.auth.user.id)
		memberships = list(memberships.values())
	# assuming that user belongs to only one group as of now
	# either by the time we reach here, we should be knowing the user group for this session
	# or just default to some user group or build a login on how to select which user group
	if memberships:
		for membership in memberships:
			membership = Storage(membership)
			current.logger.debug("groupd id is " + str(membership.group_id))
			cart = _get_prices(cart, membership, price_type_id)
	_flush_cart_with_prices(cart)
	return cart

def _get_prices(cart, membership, price_type_id):
	line_items_with_price = []
	cart.total_amount = 0
	for line_item in cart.line_items:
		# right now we are keeping it to getting the default price type
		line_item = Storage(line_item)
		price = price_dao.get_price(line_item['product_id'], membership.group_id, price_type_id)
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
	line_item_attributes = ['id', 'order_id', 'product_id', 'quantity', 'total_amount', 'discount', 'tax', 'created_on', 'line_item', 'description_short', 'name']
	new_line_items = []
	for line_item in line_items:
		for key in line_item.keys():
			if key not in line_item_attributes:
				del line_item[key]
		new_line_items.append(line_item)
	return new_line_items
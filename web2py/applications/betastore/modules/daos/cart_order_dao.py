from gluon import *

logger = current.logger
db = current.db

def save_order():
	pass

def get_empty_cart():
	"""
	if cart doesn't exist, new cart is created.
	if order.status = cart => then it is called cart
	cart is fetched based on users email and the order status
	if cart exists then it will make the existing cart empty
	"""

	order = Storage()
	order.email = current.session.auth.user.email
	order.status = "cart"
	db.bis_cart_order.update_or_insert((db.bis_cart_order.email == order.email) & (db.bis_cart_order.status == order.status), **order) 
	# in the above statement, update will return 0 or 1 and insert will return order. So below statements
	cart = db((db.bis_cart_order.email == order.email) & (db.bis_cart_order.status == order.status)).select().first()
	return cart

def update_line_item_ids(order):
	"""
	updates line_item_ids column of cart_order table from the IDs 
	of line_item table for that specific order
	"""

	line_items = db((db.bis_line_item.order_id == order.id)).select()
	line_item_ids = []
	for line_item in line_items:
		line_item_ids.append(line_item.id)
	order = db(db.bis_cart_order.id = order.id).select.first()
	order.update_record(line_items=line_item_ids)



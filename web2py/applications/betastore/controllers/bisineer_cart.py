import logging
import gluon.contrib.simplejson as json
from collections import namedtuple
import datetime
from gluon.storage import Storage
#import jsonpickle

logger = logging.getLogger("bisineer_cart")
logger.setLevel(logging.DEBUG)

# def flush_cart():
# 	json_string = request.body.read()
# 	cart = Storage(json.loads(json_string))
# 	user = session.auth.user
# 	new_line_item_ids = []
# 	modified_line_items = []

# 	for line_item in cart.line_items:
# 		print str(line_item)
# 		line_item = Storage(line_item)
# 		if not hasattr(line_item, 'id') or line_item.id is None:
# 			print "inside if"
# 			line_item.created_on = datetime.datetime.utcnow()
# 			line_item.id = db['bis_line_item'].insert(**line_item)
# 		else:
# 			print "inside else"
# 			line_item.modified_on = datetime.datetime.utcnow()
# 			db(db['bis_line_item']._id==line_item.id).update(**line_item)
# 		modified_line_items.append(line_item)
# 		new_line_item_ids.append(line_item.id)

# 	cart.line_items = modified_line_items
# 	cart.email = user.email
# 	cart.status = "cart"
# 	cart_id = db.bis_cart_order.update_or_insert((db.bis_cart_order.email == user.email) & (db.bis_cart_order.status == "cart"), **cart)
# 	cart.id = cart_id
# 	print(str(cart))
# 	return cart

# def flush_cart():
# 	json_string = request.body.read()
# 	cart = Storage(json.loads(json_string))
# 	user = session.auth.user
# 	order = Storage()
# 	order.email = user.email
# 	order.status = "cart"
# 	order_id = db.bis_cart_order.update_or_insert((db.bis_cart_order.email == order.email) & (db.bis_cart_order.status == order.status), **order)
# 	if order_id is None:
# 		order = db((db.bis_cart_order.email == order.email) & (db.bis_cart_order.status == order.status)).select().first()
# 		order_id = order.id
# 	order = db(db.bis_cart_order.id == order_id).select().first()
# 	new_line_item_ids = []
# 	modified_line_items = []
# 	for line_item in cart.line_items:
# 		line_item = Storage(line_item)
# 		line_item.order_id = order_id
# 		if not hasattr(line_item, 'id') or line_item.id is None:
# 			line_item_row = db((db.bis_line_item.order_id == order_id) & (db.bis_line_item.product_id == line_item.product_id)).select().first()
# 			if line_item_row is None:
# 				line_item.created_on = datetime.datetime.utcnow()
# 			else:
# 				line_item.quantity += line_item_row.quantity
# 				line_item.modified_on = datetime.datetime.utcnow()
# 		else:
# 			line_item.modified_on = datetime.datetime.utcnow()
# 		line_item_id = db.bis_line_item.update_or_insert((db.bis_line_item.order_id == order_id) & (db.bis_line_item.product_id == line_item.product_id), **line_item)
# 		if line_item_id is None:
# 			temp_line_item = db((db.bis_line_item.order_id == order_id) & (db.bis_line_item.product_id == line_item.product_id)).select().first()
# 			line_item_id = temp_line_item.id
# 		line_item.id = line_item_id
# 		if line_item.id not in new_line_item_ids:
# 			new_line_item_ids.append(line_item.id)
# 		modified_line_items.append(line_item)
# 	#order = db((db.bis_cart_order.email == order.email) & (db.bis_cart_order.status == order.status)).select().first() # had to call this again because of google data store. as soon as you create a row, if you try retrieving that row, you might not get it when working with GAE
# 	order.update_record(line_items=new_line_item_ids)
# 	cart.line_items = modified_line_items
# 	return cart

def flush_cart():
	# TODO removing multiple line items for same product needs to be taken care
	json_string = request.body.read()
	cart = Storage(json.loads(json_string))
	user = session.auth.user
	order = Storage()
	order.email = user.email
	order.status = "cart"
	order_id = db.bis_cart_order.update_or_insert((db.bis_cart_order.email == order.email) & (db.bis_cart_order.status == order.status), **order)
	if order_id is None:
		order = db((db.bis_cart_order.email == order.email) & (db.bis_cart_order.status == order.status)).select().first()
		order_id = order.id
	else:
		order = db(db.bis_cart_order.id == order_id).select().first()
	db(db.bis_line_item.order_id == order_id).delete()
	order.line_items = []
	new_line_item_ids = []
	for line_item in cart.line_items:
		line_item = Storage(line_item)
		line_item.order_id = order.id
		line_item_id = db.bis_line_item.update_or_insert((db.bis_line_item.order_id == order_id) & (db.bis_line_item.product_id == line_item.product_id), **line_item)
		if line_item_id is None:
			temp_line_item = db((db.bis_line_item.order_id == order_id) & (db.bis_line_item.product_id == line_item.product_id)).select().first()
			line_item_id = temp_line_item.id
		new_line_item_ids.append(line_item_id)
	order.update_record(line_items=new_line_item_ids)
	return cart
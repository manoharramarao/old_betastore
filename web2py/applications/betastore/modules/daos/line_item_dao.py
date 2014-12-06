from gluon.storage import Storage # below line could not import this. 
from gluon import *

def delete_line_items(order):
	return current.db(current.db.bis_line_item.order_id == order.id).delete() # deleting all line items for that order in DB

def save(line_item):
	"""
	Updates if record exists
	Inserts if no record found
	"""
	if line_item.id is not None:
		existing_line_item = current.db(current.db.bis_line_item.id == line_item.id).select().first()
	else:
		# TODO below statement is not working. Need to fix this. Because of this we have extra method inside cart_order_service.merge_line_items_with_same_product
		existing_line_item = current.db((current.db.bis_line_item.order_id == line_item.order_id) & (current.db.bis_line_item.product_id == line_item.product_id)).select().first()
	if existing_line_item is not None:
		line_item.id = existing_line_item.id
		line_item = current.db(current.db.bis_line_item.id == existing_line_item.id).update(**line_item)
	else:
		line_item.id = current.db.bis_line_item.insert(**line_item)
	return line_item

def get_line_item(line_item):
	"""
	Duplicate records are identified based on the follwoing priority
	1. line_item.id
	2. order_id and product_id
	"""
	if line_item.id is not None:
		return current.db(current.db.bis_line_item.id == line_item.id).select().first()
	else:
		return current.db((current.db.bis_line_item.order_id == order.id) & (current.db.bis_line_item.product_id == line_item.product_id)).select().first()
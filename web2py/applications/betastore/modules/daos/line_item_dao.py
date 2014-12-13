from gluon.storage import Storage # below line could not import this. 
from gluon import *
import uuid

def delete_line_items(order):
	return current.db(current.db.bis_line_item.order_code == order.code).delete() # deleting all line items for that order in DB

def save(line_item):
	"""
	Updates if record exists
	Inserts if no record found
	"""
	if line_item.code is not None:
		existing_line_item = current.db(current.db.bis_line_item.code == line_item.code).select().first()
	else:#try to get line item based on order code and product code
		# TODO below statement is not working. Need to fix this. Because of this we have extra method inside cart_order_service.merge_line_items_with_same_product
		existing_line_item = current.db((current.db.bis_line_item.order_code == line_item.order_code) & (current.db.bis_line_item.product_code == line_item.product_code)).select().first()
	if existing_line_item is not None:
		line_item.code = existing_line_item.code
		line_item = current.db(current.db.bis_line_item.code == existing_line_item.code).update(**line_item)
	else:
		line_item.code = str(uuid.uuid4())
		line_item.id = current.db.bis_line_item.insert(**line_item)
	return line_item

# def _prepare_code(line_item):
# 	if line_item.code is None:
# 		return str(line_item.product_code) + "-" + str(line_item.id)
# 	else:
# 		line_item.code

def get_line_item(line_item):
	"""
	Duplicate records are identified based on the follwoing priority
	1. line_item.id
	2. order_id and product_id
	"""
	if line_item.id is not None:
		return current.db(current.db.bis_line_item.id == line_item.id).select().first()
	else:
		return current.db((current.db.bis_line_item.order_code == order.code) & (current.db.bis_line_item.product_code == line_item.product_code)).select().first()
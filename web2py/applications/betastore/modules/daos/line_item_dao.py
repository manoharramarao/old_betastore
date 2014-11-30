from gluon import *

logger = current.logger
db = current.db

def delete_line_items(order):
	return db(db.bis_line_item.order_id == order_id).delete() # deleting all line items for that order in DB

def insert_line_items(order, line_items):
	new_line_items = []
	for line_item in order.line_items:
		line_item = Storage(line_item)
		line_item.order_id = order.id
		line_item = db.bis_line_item.insert((db.bis_line_item.order_id == order_id) & (db.bis_line_item.product_id == line_item.product_id), **line_item)
		new_line_items.append(line_item)
	return new_line_items

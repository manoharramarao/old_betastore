from gluon.storage import Storage
from gluon import *

def get_price(product_id, group_id, price_type_id):
	current.logger.debug("product_id is " + str(product_id))
	current.logger.debug("group_id is " + str(group_id))
	current.logger.debug("price_type_id is " + str(price_type_id))
	row = current.db((current.db.bis_price.product == product_id) & (current.db.bis_price.user_group == group_id) & (current.db.bis_price.price_type == price_type_id)).select().first()
	if row is not None:
		row = Storage(row.as_dict())
	current.logger.debug("row = " + str(row))
	return row
	

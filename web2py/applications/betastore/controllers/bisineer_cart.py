import logging
import gluon.contrib.simplejson as json
from collections import namedtuple
import datetime
from gluon.storage import Storage
#import jsonpickle

logger = logging.getLogger("bisineer_cart")
logger.setLevel(logging.DEBUG)

def add_to_cart():
	json_string = request.body.read()
	product = Storage(json.loads(json_string))
	user = session.auth.user;
	cart = {}
	queries = []
	queries.append(db.bis_cart_order.email == user.email)
	queries.append(db.bis_cart_order.status == "cart")
	query = reduce(lambda a,b:(a&b), queries)
	cart = db(query).select()
	new_order_line_item = Storage()
	if bool(cart):
		print str(cart)
	else:
		new_order_line_item.product_id = product.id
		if not hasattr(product, 'quantity') or product.quantity is None:
			new_order_line_item.quantity = 1
		else:
			new_order_line_item.quantity = product.quantity
		new_order_line_item.created_on = datetime.datetime.utcnow()
		line_item = db['bis_line_item'].insert(**new_order_line_item)
		print "line_item is " + str(line_item)
	print new_order_line_item
	return new_order_line_item

	# if cart is null, create one

	#add items to order line items and capture the ids

	# add these line items to the the cart

	# save the cart

	# return the cart
import logging
import gluon.contrib.simplejson as json
from collections import namedtuple
import datetime
from gluon.storage import Storage
#import jsonpickle

logger = logging.getLogger("bisineer_cart")
logger.setLevel(logging.DEBUG)

def flush_cart():
	json_string = request.body.read()
	cart = Storage(json.loads(json_string))
	user = session.auth.user;
	# queries = []
	# queries.append(db.bis_cart_order.email == user.email)
	# queries.append(db.bis_cart_order.status == "cart")
	# query = reduce(lambda a,b:(a&b), queries)
	# cart = db(query).select()
	# new_order_line_item = Storage()
	# if bool(cart):
		# bail out
	modified_line_items = []
	for line_item in cart.line_items:
		print str(line_item)
		line_item = Storage(line_item)
		if not hasattr(line_item, 'id') or line_item.id is None:
			print "inside if"
			line_item.created_on = datetime.datetime.utcnow()
			line_item.id = db['bis_line_item'].insert(**line_item)
		else:
			print "inside else"
			line_item.modified_on = datetime.datetime.utcnow()
			db(db['bis_line_item']._id==line_item.id).update(**line_item)
		modified_line_items.append(line_item)

	cart.line_items = modified_line_items
	print(str(cart))
	return cart

	# if cart is null, create one

	#add items to order line items and capture the ids

	# add these line items to the the cart

	# save the cart

	# return the cart
from gluon.storage import Storage
from gluon import *
from daos import auth_user_dao
import uuid


def save_order():
    pass

# def get_cart():
# 	"""
# 	if cart doesn't exist, new cart is created.
# 	if order.status = cart => then it is called cart
# 	cart is fetched based on signed in user's email and the order status
# 	"""
# 	order = Storage()
# 	order.email = current.session.auth.user.email
# 	order.status = "cart" # this is how it is differentiated between cart and order
# 	current.db.bis_cart_order.update_or_insert((current.db.bis_cart_order.email == order.email) & (current.db.bis_cart_order.status == order.status), **order) 
# 	# in the above statement, update will return the record and insert will return record id. So the below statements
# 	cart = current.db((current.db.bis_cart_order.email == order.email) & (current.db.bis_cart_order.status == order.status)).select().first()
# 	return cart


def get_cart():
    """
    gets cart for the logged in user. If not exists, creates new cart for that user
    if order.status = cart => then it is called cart
    cart is fetched based on signed in user's code and the order status
    """
    current.logger.debug("user_code for logged in user is " + str(current.session.auth.user))
    cart = current.db((current.db.bis_cart_order.user_code == current.session.auth.user.code) & (current.db.bis_cart_order.status == "cart")).select().first()
    if cart is None:
        cart = Storage()
        cart.user_code = current.session.auth.user.code
        cart.status = "cart"  # this is how it is differentiated between cart and order
        print str(cart)
        cart.code = str(uuid.uuid4())
        cart.id = current.db.bis_cart_order.insert(**cart)
        #cart.code = current.session.auth.user.code + "-" + str(cart.id) # this is cart.code
    else:
        #cart.code = current.session.auth.user.code + "-" + str(cart.id) # this is cart.code
        #cart.code = str(uuid.uuid4())
        cart = Storage(cart.as_dict())
    return cart

def save(order):
    """
    Duplicate records are identified based on the follwoing priority
    1. order.id
    """
    if order.id is not None:
        current.db(current.db.bis_cart_order.id == order.id).update(**order)
    else:
        order.id = current.db.bis_cart_order.insert(**order)
    return order





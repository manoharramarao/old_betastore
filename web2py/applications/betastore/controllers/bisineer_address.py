from collections import namedtuple
from gluon.storage import Storage
from applications.betastore.modules.daos import address_dao
from services import address_service
from bisineer_http_status_codes import HTTPStatusCodes

import gluon.contrib.simplejson as json
import datetime

#import jsonpickle

def add_address():
	pass

def delete_address():
	pass

def save_address():
	"""
	insert if it is new(decided based on address name) or else save the changes.
	"""
	json_string = request.body.read()
	print json_string
	address = Storage(json.loads(json_string))
	#user = session.auth.user
	print address.name
	print address.street_address
	print address.landmark
	print address.city
	print address.state
	address_id = db.bis_address.update_or_insert((db.bis_address.name == address.name), **address) 
	if(address_id is None or address_id==0):
		# actual http status code sent to client is 500. Need to fix that. Instead it should send the one defined in this project 540
		raise HTTP(HTTPStatusCodes.TECHNICAL_EXCEPTION, "technical exception - error saving record")
	else:
		raise HTTP(HTTPStatusCodes.TECHNICAL_EXCEPTION, "technical exception - error saving record") 
		result = {"result": "success"}
		return result

@auth.requires_login()
def get_addresses():
	print "inside get_addresses"
	addresses = []
	user = session.auth.user
	addresses = address_dao.get_shipping_addresses(user)
	cleaned_addresses = address_service.clean(addresses)
	return dict(addresses=addresses)

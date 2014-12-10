from gluon.storage import Storage
from gluon import *

def get_default_price_code():
	row = current.db(current.db.bis_price_type.name == "default").select().first().as_dict()
	return row['code']
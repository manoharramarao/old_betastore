from gluon.storage import Storage
from gluon import *

def get_default_group_id():
	row = current.db(current.db.auth_group.role == "default").select().first().as_dict()
	return row['id']